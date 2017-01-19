"""
Process the data received from the OpenStack API's
and prep for writing into RethinkDB.
"""

def processor(*args):

    gins = 0    # Global instance count
    gcpu = 0    # Global vCPU count
    gram = 0    # Global RAM count
    gdsk = 0    # Global disk usage count
    gvol = 0    # Global volume count
    gint = 0    # Global internal user count
    gext = 0    # Global external user count

    gactive = 0         # Global active instances count
    gsuspend = 0        # Global suspended instances count
    gshutdown = 0       # Global shutdown instances count
    gerror = 0          # Global error instances count
    guncat = 0          # Global uncategorized instances count

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
            gext += 1

        if "1-" not in tenant["description"]:
            intorext = "Internal"
            gint += 1

        user_list = list()
        for user in users["users"]:
            if tenant["id"] in user["tenantId"]:
                user_list.append(user["username"])
        for state in instances["servers"]:
            if tenant["id"] in state["tenant_id"]:
                if state["status"] in "ACTIVE":
                    active += 1
                    gactive += 1
                elif state["status"] in "ERROR":
                    error += 1
                    gerror += 1
                elif state["status"] in "PAUSED":
                    suspend += 1
                    gsuspend += 1
                elif state["status"] in "STOPPED":
                    shutdown += 1
                    gshutdown += 1
                elif state["status"] in "SHUTOFF":
                    shutdown += 1
                    gshutdown += 1
                elif state["status"] in "SUSPENDED":
                    suspend += 1
                    gsuspend += 1
                else:
                    uncat += 1
                    guncat += 1
        for server in instances["servers"]:
            if tenant["id"] in server["tenant_id"]:
                ins +=1
                gins += 1
                for flavor in flavors["flavors"]:
                    if server["flavor"]["id"] in flavor["id"]:
                        cpu += int(flavor["vcpus"])
                        gcpu += int(flavor["vcpus"])
                        ram += int(flavor["ram"] / 1024)
                        gram += int(flavor["ram"] / 1024)
                        dsk += int(flavor["disk"])
                        gdsk += int(flavor["disk"])
        for volume in volumes["volumes"]:
            if tenant["id"] in volume["os-vol-tenant-attr:tenant_id"]:
                vol += int(volume["size"])
                gvol += int(volume["size"])
        tenant_list.append([tenant["name"], intorext, user_list, ins, cpu, ram, dsk, vol, active, suspend, shutdown, error, uncat])

        return tenant_list, gins, gcpu, gram, gdsk, gvol, gactive, gsuspend, gshutdown, gerror, guncat
