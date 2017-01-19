"""
Enable asyncronous HTTP requests.
"""
import time

from concurrent.futures import ThreadPoolExecutor

from requests_futures.sessions import FuturesSession

from osreporter.http import headers
from osreporter.openstack import authentication


def main():
    # Authenticate against OpenStack
    auth = authentication.Authenticate().do()

    session = FuturesSession(executor=ThreadPoolExecutor, max_workers=8, session=None)
    session.headers.update(headers.common_headers(token))

    start_time = time.time()

    req_a = session.get("http://127.0.0.1:8774/v2/%s/servers/detail?all_tenants=1".format(tenant))
    req_b = session.get("http://127.0.0.1:8774/v2/%s/flavors/detail".format(tenant))
    req_c = session.get("http://127.0.0.1:35357/v2.0/tenants")
    req_d = session.get("http://127.0.0.1:35357/v2.0/users")
    req_e = session.get("http://127.0.0.1:8776/v1/%s/volumes/detail?all_tenants=1" % tenant)

    res_a = req_a.result(timeout=None)
    res_b = req_b.result(timeout=None)
    res_c = req_c.result(timeout=None)
    res_d = req_d.result(timeout=None)
    res_e = req_e.result(timeout=None)

    


if __name__ == "__main__":
    main()
