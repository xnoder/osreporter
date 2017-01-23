"""
Write data to Elasticsearch.
"""
import datetime
import json
import sys

import requests

from osreporter.config import yaml


def writer(data):
    """Write data to Elasticsearch."""
    result_sets = 0

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
        result_sets += 1

        # Read in config
        config = yaml.read('/etc/osreporter.yaml')
        server = config['elastic']['server']
        port = config['elastic']['port']
        index = config['elastic']['index']
        index_type = config['elastic']['type']

        request = requests.post("http://{0}:{1}/{2}/{3}/".format(server, port, index, index_type), data=json.dumps(doc))
        print("Wrote {0} stats to Elastic [{1}]".format(point[0], request.status_code), sep=' ', end='\n', file=sys.stdout, flush=False)
        if request.status_code != 201:
            print("Error communicating with Elastic. Code was [{0}]".format(request.status_code), sep='\n')
            sys.exit(1)
    print("Wrote {0} accounts to the Elastic database.".format(result_sets), sep=' ', end='\n', file=sys.stdout, flush=False)
