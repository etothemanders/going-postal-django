import json
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    Creates a client_secrets.json file for use by the Google oauth2client library.
    https://developers.google.com/api-client-library/python/auth/web-app
    """

    def handle(self, *args, **options):
        data = {
            "web": {
                "client_id": os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'),
                "client_secret": os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET'),
                "redirect_uris": [],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token"
            }
        }
        with open('client_secrets.json', 'w') as fd:
            json.dump(data, fd)
        self.stdout.write('done!')
