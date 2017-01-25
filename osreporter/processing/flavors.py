"""
Process data for flavor usage.
"""
import sys

def process(instances, flavors):

    fmap = dict()
    fstats = dict()

    for flavor in flavors["flavors"]:
        fmap[flavor['id']] = flavor['name']
        fstats[flavor['name']] = 0

    inst = 0
    for flavor in instances["servers"]:
        uuid = flavor['flavor']['id']
        if uuid in fmap:
            fstats[fmap[uuid]] += 1

    return fstats
