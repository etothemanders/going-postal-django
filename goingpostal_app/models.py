from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from .tracker import Tracker


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
        pass


class Location(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)
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
        return location
