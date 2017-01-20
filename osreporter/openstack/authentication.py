"""
Authenticate against OpenStack's API's.
"""

import json
import os
import sys
import time

import requests

from osreporter.http import headers


class Authenticate(object):

    def __init__(self):
        self.username = os.getenv("OS_USERNAME", default=None)
        self.password = os.getenv("OS_PASSWORD", default=None)
        self.tenant = os.getenv("OS_TENANT_NAME", default=None)
        self.url = os.getenv("OS_AUTH_URL", default=None)

    def v2_payload(self):
        payload = {
            "auth": {
                "tenantName": self.tenant,
                "passwordCredentials": {
                    "username": self.username,
                    "password": self.password,
                }
            }
        }
        return payload

    def v3_payload(self):
        raise NotImplementedError

    def do(self, version=None):
        if version == 2:
            payload = self.v2_payload()

        if version == 3:
            payload = self.v3_payload()

        if not version:
            raise AttributeError

        start_time = time.time()

        head = headers.auth_headers()
        url = "{0}/tokens".format(self.url)
        request = requests.post(url, data=json.dumps(payload), headers=head)

        if request.status_code != requests.codes.ok:
            print("Error: {0}".format(str(requests.raise_for_status())),sep=' ', end='n', file=sys.stdout, flush=False)
            sys.exit(status=1)

        return request.json()
