#!/usr/bin/python
from java.util import *
from javax.management import *
import javax.management.Attribute

warning_threshold=90; critical_threshold=95

connect('weblogic','11111111','t3://192.168.1.41:7001')
domainRuntime()
servers = domainRuntimeService.getServerRuntimes()
for server in servers:
    heapusedpercent = 100-int(server.getJVMRuntime().getHeapFreePercent())
    server_file=open('/tmp/'+server.getName(), 'w')
    server_file.write(str(heapusedpercent))
disconnect()
exit()
