"""
Process the data received from the OpenStack API's
and prep for writing into RethinkDB.
"""

def process(tenants, users, instances, flavors, volumes):

    tenant_list = list()
    for tenant in tenants["tenants"]:
        ins = 0
        cpu = 0
        ram = 0
        dsk = 0
        vol = 0

        active = 0
        suspend = 0
        shutdown = 0
        error = 0
        uncat = 0

        intorext = None

        if "1-" in tenant["description"]:
            intorext = "External"

        if "1-" not in tenant["description"]:
            intorext = "Internal"

        user_list = list()
        for user in users["users"]:
            if tenant["id"] in user["tenantId"]:
                user_list.append(user["username"])
        for state in instances["servers"]:
            if tenant["id"] in state["tenant_id"]:
                if state["status"] in "ACTIVE":
                    active += 1
                elif state["status"] in "ERROR":
                    error += 1
                elif state["status"] in "PAUSED":
                    suspend += 1
                elif state["status"] in "STOPPED":
                    shutdown += 1
                elif state["status"] in "SHUTOFF":
                    shutdown += 1
                elif state["status"] in "SUSPENDED":
                    suspend += 1
                else:
                    uncat += 1
        for server in instances["servers"]:
            if tenant["id"] in server["tenant_id"]:
                ins +=1
                for flavor in flavors["flavors"]:
                    if server["flavor"]["id"] in flavor["id"]:
                        cpu += int(flavor["vcpus"])
                        ram += int(flavor["ram"] / 1024)
                        dsk += int(flavor["disk"])
        for volume in volumes["volumes"]:
            if tenant["id"] in volume["os-vol-tenant-attr:tenant_id"]:
                vol += int(volume["size"])
        tenant_list.append([tenant["name"], intorext, user_list, ins, cpu, ram, dsk, vol, active, suspend, shutdown, error, uncat])

    return tenant_list
