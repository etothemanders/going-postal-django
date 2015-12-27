from datetime import datetime
import json

import googlemaps

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from .tracker import Tracker

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_SERVER_API_KEY)


class Shipment(models.Model):
    tracking_no = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tracking_no

    def track_activities(self):
        shipper_interface = Tracker.get_shipper_interface(self.tracking_no)
        activities = shipper_interface.track(self.tracking_no)
        return activities

    @property
    def last_activity(self):
        return Location.objects.filter(shipment=self).order_by('-timestamp').first()

    def create_geojson_feature(self):
        locations = Location.objects.filter(shipment=self).exclude(latitude__isnull=True).exclude(longitude__isnull=True)
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
    status_description = models.CharField(max_length=64)

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
        location.geocode()
        return location

    def geocode(self):
        if self.city != 'Unknown' and self.state != 'Unknown':
            geocode_results = gmaps.geocode('{city}, {state}'.format(city=self.city, state=self.state))
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
                self.save()

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
