"""
Write data to Elasticsearch.
"""
import datetime
import json
import sys

import requests

from osreporter.config import yaml


def usage(data):
    """Write data to Elastic."""

    for point in data:
        doc = {
            "created_at": datetime.datetime.now().isoformat(sep='T'),
            "name": point[0],
            "type": point[1],
            "instances": point[3],
            "vcpus": point[4],
            "ram": point[5],
            "storage_local": point[6],
            "storage_shared": point[7],
            "instance_states": {
                "active": point[8],
                "suspended": point[9],
                "shutdown": point[10],
                "error": point[11],
                "other": point[12]
            }
        }

        # Read in config
        self.config = yaml.read(os.getenv("OSREPORTER_CONFIG", default=os.path.join(os.path.expanduser('~'), "trellominer.yaml")))
        server = config['elastic']['server']
        port = config['elastic']['port']
        index = config['elastic']['index']
        index_type = config['elastic']['type']

        request = requests.post("http://{0}:{1}/{2}/{3}/".format(server, port, index, index_type), data=json.dumps(doc))
        if request.status_code != 201:
            print("Error communicating with Elastic. Code was [{0}]".format(request.status_code), sep='\n')
            sys.exit(1)


def flavors(data):
    """Write flavor data to Elastic."""
    for key, value in data.items():
        doc = {
            "created_at": datetime.datetime.now().isoformat(sep='T'),
            "flavor": key,
            "total": value
        }

        # Read in config
        config = yaml.read('/etc/osreporter.yaml')
        server = config['elastic']['server']
        port = config['elastic']['port']
        index = config['elastic']['index']
        index_type = "flavors"

        request = requests.post("http://{0}:{1}/{2}/{3}/".format(server, port, index, index_type), data=json.dumps(doc))
        if request.status_code != 201:
            print("Error communicating with Elastic. Code was [{0}]".format(request.status_code), sep='\n')
            sys.exit(1)
