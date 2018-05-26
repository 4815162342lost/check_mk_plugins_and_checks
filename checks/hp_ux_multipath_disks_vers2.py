#!/usr/bin/python
#output example
#<<<hp_ux_multipath>>>
#disk      1  14000/0x8800/0x2   online
#disk    1003  14000/0x8800/0x2   online
#disk    1002  14000/0x8800/0x8   online

restricted_states=('offline', 'unusable')

def inventory_hp_ux_multipath_offline_only(info):
    inventory = []
    for line in info:
        inventory.append((line[2], None))
    return inventory

def check_hp_ux_multipath_offline_only(item, params, info):
    for line in info:
        if line[2] == item:
            if line[3] not in restricted_states:
            #if line[3] != 'offline':
                return 0, 'disk is not offline'
            else:
                #return 2, 'disk is offline!'
                return 2, 'disk status: {status}'.format(status=line[3])
    return 3, 'disk disappeared'

def inventory_hp_ux_multipath(info):
    inventory = []
    for line in info:
        inventory.append((line[2], None))
    return inventory

def check_hp_ux_multipath(item, params, info):
    for line in info:
        if line[2] == item:
            if line[3] == 'online':
                return 0, 'disk is online'
            else:
                return 2, 'disk status: {status}'.format(status=line[3])
    return 3, 'disk disappeared'

check_info["hp_ux_multipath"] = {
    'check_function':          check_hp_ux_multipath,
    'inventory_function':      inventory_hp_ux_multipath,
    'service_description':     'Multipath disk %s',
}

check_info["hp_ux_multipath.offfline_only"] = {
    'check_function':          check_hp_ux_multipath_offline_only,
    'inventory_function':      inventory_hp_ux_multipath,
    'service_description':     'Multipath disk %s check_offline_only',
}
