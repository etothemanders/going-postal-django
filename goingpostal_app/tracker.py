import re
import urllib

from django.conf import settings
from .xml_dict import dict_to_xml, xml_to_dict


class UPSInterface(object):
    def __init__(self):
        self.api_url = 'https://wwwcie.ups.com/ups.app/xml/Track'
        self.attrs = {'xml:lang': 'en-US'}

    def matches(self, tracking_no):
        return tracking_no.startswith('1Z') and len(tracking_no) == 18

    def build_access_request(self):
        d = {
            'AccessRequest': {
                'AccessLicenseNumber': settings.UPS_LICENSE_NUMBER,
                'UserId': settings.UPS_USER_ID,
                'Password': settings.UPS_PASSWORD
            }
        }
        return dict_to_xml(d, self.attrs)

    def build_track_request(self, tracking_no):
        req = {'RequestOption': '1',
               'TransactionReference': {'RequestAction': 'Track'}}
        d = {'TrackRequest': {'TrackingNumber': tracking_no,
                              'Request': req}}
        return dict_to_xml(d)

    def build_request(self, tracking_no):
        request = self.build_access_request() + self.build_track_request(tracking_no)
        return request

    def send_request(self, tracking_no):
        body = self.build_request(tracking_no)
        webf = urllib.urlopen(self.api_url, body)
        resp = webf.read()
        webf.close()
        return resp

    def preprocess_response(self, raw):
        """
        Remove unpaired XML tags from raw response.
        """
        pattern = re.compile(r'<[a-zA-z]+/>')
        new_raw = pattern.sub('Unknown', raw)
        return new_raw

    def parse_response(self, raw):
        pattern = re.compile(r'<Activity>.*?</Activity>')
        activity_list = re.findall(pattern, raw)
        activities = []
        for activity in activity_list:
            thing = xml_to_dict(activity)['Activity']
            activities.append(thing)
        return activities

    def track(self, tracking_no):
        resp = self.send_request(tracking_no)
        resp = self.preprocess_response(resp)
        return self.parse_response(resp)


class Tracker(object):
    def __init__(self):
        self.interfaces = [
            UPSInterface()
        ]

    def get_shipper_interface(self, tracking_no):
        for interface in self.interfaces:
            if interface.matches(tracking_no):
                return interface

Tracker = Tracker()
