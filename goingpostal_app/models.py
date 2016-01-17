import base64
from datetime import datetime
import json
import logging
import re

from apiclient import errors, discovery
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import googlemaps
import httplib2
from oauth2client.django_orm import FlowField, CredentialsField

from .exceptions import UntrackableException, DuplicateShipmentException
from .tracker import Tracker

GMAPS = googlemaps.Client(key=settings.GOOGLE_MAPS_SERVER_API_KEY)


class Shipment(models.Model):
    tracking_no = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tracking_no

    @classmethod
    def add_shipment(cls, user=None, tracking_number=None):
        if not cls.objects.filter(tracking_no=tracking_number, user=user):
            s = cls(tracking_no=tracking_number, user=user)
            try:
                s.track_activities()
            except Exception:
                raise UntrackableException(tracking_number)
        else:
            raise DuplicateShipmentException(tracking_number)

    def track_activities(self):
        shipper_interface = Tracker.get_shipper_interface(self.tracking_no)
        activities = shipper_interface.track(self.tracking_no)

        # If the UPS API does not return any activity data, don't save the shipment
        if not activities:
            raise Exception

        self.save()
        map(lambda activity_dict: Location.create(activity_dict=activity_dict, shipment=self).geocode().save(), activities)

    def check_for_new_activity(self):
        activities = self.track_activities()
        locations = map(lambda activity_dict: Location.create(activity_dict=activity_dict, shipment=self), activities)
        for loc in locations:
            try:
                previous_location = Location.objects.get(shipment=self,
                                                         city=loc.city,
                                                         state=loc.state,
                                                         country=loc.country,
                                                         timestamp=loc.timestamp,
                                                         status_description=loc.status_description)
            except Location.DoesNotExist:
                loc.geocode()
                loc.save()

    @property
    def last_activity(self):
        return Location.objects.filter(shipment=self).order_by('-timestamp').first()

    def create_geojson_feature(self):
        locations = Location.objects.filter(shipment=self).exclude(latitude__isnull=True).exclude(longitude__isnull=True).order_by('timestamp')
        if len(locations) == 1:
            location = locations.first()
            point_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [location.longitude, location.latitude]
                },
                "properties": {
                    "shipmentID": self.id
                }
            }
            return point_feature
        else:
            line_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": map(lambda l: [l.longitude, l.latitude], locations)
                },
                "properties": {
                    "shipmentID": self.id,
                }
            }
            return line_feature


class Location(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    latitude = models.FloatField(max_length=64, blank=True, null=True)
    longitude = models.FloatField(max_length=64, blank=True, null=True)
    timestamp = models.DateTimeField()
    status_description = models.CharField(max_length=128)

    @classmethod
    def create(cls, activity_dict=None, shipment=None):
        if activity_dict['ActivityLocation'] != 'Unknown':
            address = activity_dict['ActivityLocation']['Address']
            try:
                city = address['City']
            except KeyError:
                city = 'Unknown'
            try:
                state = address['StateProvinceCode']
            except KeyError:
                state = 'Unknown'
            try:
                country = address['CountryCode']
            except KeyError:
                country = 'Unknown'
        else:
            city = 'Unknown'
            state = 'Unknown'
            country = 'Unknown'
        timestamp = datetime.strptime('{date} {time}'.format(date=activity_dict['Date'], time=activity_dict['Time']), '%Y%m%d %H%M%S')
        status_description = activity_dict['Status']['StatusType']['Description']
        location = cls(shipment=shipment,
                       city=city,
                       state=state,
                       country=country,
                       timestamp=timestamp,
                       status_description=status_description)
        return location

    def geocode(self):
        if self.city != 'Unknown' and self.state != 'Unknown':
            geocode_results = GMAPS.geocode('{city}, {state}'.format(city=self.city, state=self.state))
            if len(geocode_results) > 0:
                best_match = geocode_results[0]
                try:
                    self.latitude = json.dumps(best_match['geometry']['location']['lat'])
                except KeyError:
                    pass
                try:
                    self.longitude = json.dumps(best_match['geometry']['location']['lng'])
                except KeyError:
                    pass
        return self

    @property
    def placename(self):
        places = []
        if self.city != 'Unknown':
            places.append(self.city)
        if self.state != 'Unknown':
            places.append(self.state)
        if self.country != 'Unknown':
            places.append(self.country)

        if places:
            return ' '.join(places)
        else:
            return 'Unknown'


class FlowModel(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    flow = FlowField()


class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=254)
    credential = CredentialsField()

    def get_shipment_emails(self):
        credentials = self.credential
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        query = 'shipped tracking number newer_than:30d'

        try:
            response = (service
                        .users()
                        .messages()
                        .list(userId=self.email_address, q=query)
                        .execute())
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = (service
                            .users()
                            .messages()
                            .list(userId=self.email_address,
                                  q=query,
                                  pageToken=page_token)
                            .execute())
                messages.extend(response['messages'])

            self.create_emails(messages)
        except errors.HttpError, error:
            logging.error('An error occurred: %s', error)

    def create_emails(self, email_dicts):
        emails = map(lambda email_dict: (Email
                                         .objects
                                         .get_or_create(email_account=self,
                                                        gmail_id=email_dict.get('id'))
                                         ), email_dicts)
        new_emails = [obj_tup[0] for obj_tup in emails if obj_tup[1] is True]

        if new_emails:
            for new_email in new_emails:
                new_email.parse_tracking_number()


class Email(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    gmail_id = models.CharField(max_length=64)

    def parse_tracking_number(self):
        credentials = self.email_account.credential
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        try:
            message = (service
                       .users()
                       .messages()
                       .get(userId=self.email_account.email_address,
                            id=self.gmail_id,
                            format='raw')
                       .execute())
            msg_body = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            pattern = r'1Z[A-Z0-9]{16}'
            results = re.findall(pattern, msg_body)

            if results:
                # In case there is more than one legitimate tracking number...
                tracking_numbers = set(results)

                # ...try to add all of them
                for tracking_number in tracking_numbers:
                    try:
                        Shipment.add_shipment(user=self.email_account.user,
                                              tracking_number=tracking_number)
                    except DuplicateShipmentException, exception:
                        logging.info('An exception occured: %s', exception.message)
                    except UntrackableException, exception:
                        logging.warning('An exception occurred: %s', exception.message)

        except errors.HttpError, error:
            logging.error('An error occurred: %s', error)
