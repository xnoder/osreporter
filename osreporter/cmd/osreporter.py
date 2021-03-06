"""
Enable asyncronous HTTP requests.
"""
import argparse
import os
import sys
import time

import requests

from concurrent.futures import ThreadPoolExecutor

from requests_futures.sessions import FuturesSession

from osreporter.config import yaml
from osreporter.db import elasticsearch
from osreporter.db import excel
from osreporter.http import headers
from osreporter.openstack import authentication
from osreporter.processing import flavors
from osreporter.processing import usage


def main():
    # Read config
    config = yaml.read(os.getenv("OSREPORTER_CONFIG", default=os.path.join(os.path.expanduser('~'), ".osreporter.yaml")))
    schema = config['openstack']['schema']
    address = config['openstack']['address']

    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help="Select the backend to write to.")
    args = parser.parse_args()

    # Authenticate against OpenStack
    auth = authentication.Authenticate().do(version=2)
    tenant = auth["access"]["token"]["tenant"]["id"]
    token = auth["access"]["token"]["id"]

    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=8))
    session.headers.update(headers.common_headers(token))

    start_time = time.time()

    # Asyncronous requests to the OpenStack API's.
    print("Calling API's...", sep='', end='', file=sys.stdout, flush=True)
    req_a = session.get("{0}://{1}:8774/v2/{2}/servers/detail?all_tenants=1".format(schema, address, tenant))
    req_b = session.get("{0}://{1}:8774/v2/{2}/flavors/detail?is_public=None".format(schema, address, tenant))
    req_c = session.get("{0}://{1}:35357/v2.0/tenants".format(schema, address))
    req_d = session.get("{0}://{1}:35357/v2.0/users".format(schema, address))
    req_e = session.get("{0}://{1}:8776/v1/{2}/volumes/detail?all_tenants=1".format(schema, address, tenant))
    req_f = session.get("{0}://{1}:8774/v2/{2}/images/detail".format(schema, address, tenant))

    # Save the results.
    res_a = req_a.result(timeout=None)
    if res_a.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    res_b = req_b.result(timeout=None)
    if res_b.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    res_c = req_c.result(timeout=None)
    if res_c.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    res_d = req_d.result(timeout=None)
    if res_d.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    res_e = req_e.result(timeout=None)
    if res_e.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    res_f = req_f.result(timeout=None)
    if res_f.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=True)
        sys.exit(1)

    end_time = (time.time() - start_time)
    print("[DONE]. [{:.2f} seconds]".format(end_time), sep='', end='\n', file=sys.stdout, flush=True)

    # Process the data into a nested list()
    print("Processing data...", sep=' ', end='', file=sys.stdout, flush=True)
    start_time = time.time()
    usage_processor = usage.process(res_c.json(), res_d.json(), res_a.json(), res_b.json(), res_e.json())
    flavor_processor = flavors.process(res_a.json(), res_b.json())
    end_time = (time.time() - start_time)
    print("[DONE]. [{:.2f} seconds]".format(end_time), sep='', end='\n', file=sys.stdout, flush=True)

    # Write the data to the database
    if 'elastic' in args.db:
        start_time = time.time()
        print("Writing data to Elasticsearch...", sep=' ', end='', file=sys.stdout, flush=True)
        elasticsearch.usage(usage_processor)
        elasticsearch.flavors(flavor_processor)
        end_time = (time.time() - start_time)
        print("[DONE]. [{:.2f} seconds]".format(end_time), sep='', end='\n', file=sys.stdout, flush=True)

    if 'excel' in args.db:
        start_time = time.time()
        print("Writing data to Excel...", sep=' ', end='', file=sys.stdout, flush=True)
        excel.usage(usage_processor)
        excel.flavors(flavor_processor)
        end_time = (time.time() - start_time)
        print("[DONE]. [{:.2f} seconds]".format(end_time), sep='', end='\n', file=sys.stdout, flush=True)

    if 'test' in args.db:
        pass

if __name__ == "__main__":
    main()
