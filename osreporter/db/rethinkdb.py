"""
Write data to RethinkDB.
"""
import datetime

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


def usage(data):
    """Write data to RethinkDB."""

    try:
        conn = r.connect(host="localhost", port=28015, db="osreporter", auth_key=None, user='admin', password=None, timeout=20, ssl=dict(), _handshake_version=10)
        for point in data:
            r.table("usage").insert({
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
            }).run(c=conn)
        except RqlRuntimeError as error:
            print("Error: {}".format(err), sep=' ', end='\n', file=sys.stdout, flush=True)
        finally:
            conn.close()


def flavors(data):
    """Write flavor data to RethinkDB."""

    try:
        conn = r.connect(host="localhost", port=28015, db="osreporter", auth_key=None, user='admin', password=None, timeout=20, ssl=dict(), _handshake_version=10)

        for key, value in data.items():
            r.table("flavors").insert({
                "created_at": datetime.datetime.now().isoformat(sep='T'),
                "flavor": key,
                "total": value
            }).run(c=conn)
    except RqlRuntimeError as error:
        print("Error: {0}".format(error), sep=' ', end='\n', file=sys.stdout, flush=False)
    finally:
        conn.close()
