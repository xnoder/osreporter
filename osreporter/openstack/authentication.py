"""
Authenticate against OpenStack's API's.
"""

import json
import os
import sys

from osreporter import headers


class Authenicate(object):

    def __init__(self):
        self.username = os.getenv("OS_USERNAME", default=None)
        self.password = os.getenv("OS_PASSWORD", default=None)
        self.tenant = os.getenv("OS_TENANT_NAME", default=None)
        self.url = os.getenv("OS_AUTH_URL", default=None)

    @staticmethod
    def v2_payload():
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

    @staticmethod
    def v3_payload():
        raise NotImplementedError

    def do(self, version=None):
        if version == 2:
            payload = v2_payload()

        if version == 3:
            payload = v3_payload()

        if not version:
            raise AttributeError

        start_time = time.time()

        headers = headers.auth_headers()
        requests = requests.post(url, data=json.dumps(payload), headers=headers.)

        if requests.status_code != requests.codes.ok:
            print("Error: %s", % str(requests.raise_for_status()),sep=' ', end='n', file=sys.stdout, flush=False)
            sys.exit(status=1)

        return request.json()
