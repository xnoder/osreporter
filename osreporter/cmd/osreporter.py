"""
Enable asyncronous HTTP requests.
"""
import sys
import time

import requests

from concurrent.futures import ThreadPoolExecutor

from requests_futures.sessions import FuturesSession

from osreporter.db import data
from osreporter.db import writer
from osreporter.http import headers
from osreporter.openstack import authentication


def main():
    print("Collecting data from OpenStack: ", sep=' ', end='', file=sys.stdout, flush=False)
    # Authenticate against OpenStack
    auth = authentication.Authenticate().do(version=2)
    tenant = auth["access"]["token"]["tenant"]["id"]
    token = auth["access"]["token"]["id"]

    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=8))
    session.headers.update(headers.common_headers(token))

    start_time = time.time()
    print(start_time, sep=' ', end='\n', file=sys.stdout, flush=False)
    print("Got a token [{0}] for tenant ID {1}".format(token, tenant), sep=' ', end='\n', file=sys.stdout, flush=False)

    # Asyncronous requests to the OpenStack API's.
    print("Starting API request sequence...", sep=' ', end='\n', file=sys.stdout, flush=False)
    req_a = session.get("http://127.0.0.1:8774/v2/{0}/servers/detail?all_tenants=1".format(tenant))
    req_b = session.get("http://127.0.0.1:8774/v2/{0}/flavors/detail".format(tenant))
    req_c = session.get("http://127.0.0.1:35357/v2.0/tenants")
    req_d = session.get("http://127.0.0.1:35357/v2.0/users")
    req_e = session.get("http://127.0.0.1:8776/v1/{0}/volumes/detail?all_tenants=1".format(tenant))

    # Save the results.
    res_a = req_a.result(timeout=None)
    print("\t[CALL] Servers HTTP/1.1 {0}: ".format(res_a.status_code), sep=' ', end='', file=sys.stdout, flush=False)
    if res_a.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=False)
        sys.exit(1)
    else:
        print("[DONE]", sep=' ', end='\n', file=sys.stdout, flush=False)

    res_b = req_b.result(timeout=None)
    print("\t[CALL] Flavours HTTP/1.1 {0}: ".format(res_a.status_code), sep=' ', end='', file=sys.stdout, flush=False)
    if res_b.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=False)
        sys.exit(1)
    else:
        print("[DONE]", sep=' ', end='\n', file=sys.stdout, flush=False)

    res_c = req_c.result(timeout=None)
    print("\t[CALL] Tenants HTTP/1.1 {0}: ".format(res_a.status_code), sep=' ', end='', file=sys.stdout, flush=False)
    if res_c.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=False)
        sys.exit(1)
    else:
        print("[DONE]", sep=' ', end='\n', file=sys.stdout, flush=False)

    res_d = req_d.result(timeout=None)
    print("\t[CALL] Users HTTP/1.1 {0}: ".format(res_a.status_code), sep=' ', end='', file=sys.stdout, flush=False)
    if res_d.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=False)
        sys.exit(1)
    else:
        print("[DONE]", sep=' ', end='\n', file=sys.stdout, flush=False)

    res_e = req_e.result(timeout=None)
    print("\t[CALL] Volumes HTTP/1.1 {0}: ".format(res_a.status_code), sep=' ', end='', file=sys.stdout, flush=False)
    if res_e.status_code != requests.codes.ok:
        print("Cannot get to API.", sep=' ', end='\n', file=sys.stdout, flush=False)
        sys.exit(1)
    else:
        print("[DONE]", sep=' ', end='\n', file=sys.stdout, flush=False)

    end_time = (time.time() - start_time)

    # Process the data into a nested list()
    process = data.processor(res_c.json(), res_d.json(), res_a.json(), res_b.json(), res_e.json())

    # Write the data to the database
    store = writer.writer(process)


if __name__ == "__main__":
    main()
