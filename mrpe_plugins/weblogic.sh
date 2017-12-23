#!/bin/bash
WL_HOME=/home/vodka/Oracle/Middleware/wlserver_10.3
warn=90
crit=95

$WL_HOME/common/bin/wlst.sh /etc/check-mk-agent/check_weblogic.py 2>/dev/null 1>/dev/null
if [ -f '/tmp/AdminServer' ]
    then 
    heapusedpercent=`cat /tmp/AdminServer`
    rm -f /tmp/AdminServer
    if ((heapusedpercent>crit))
        then
        echo "CRIT - heap memory is using on $heapusedpercent% |used_memory=$heapusedpercent;$warn;$crit;0;100"
        exit 2 

    elif ((heapusedpercent>warn))
        then
        echo "WARN - heap memory is using on $heapusedpercent% |used_memory=$heapusedpercent;$warn;$crit;0;100"
        exit 1

    else
        echo "OK - heap memory is using on $heapusedpercent% |used_memory=$heapusedpercent;$warn;$crit;0;100"
        exit 0
    fi
else
    echo "UNKNOWN - there are problem with Weblogic"
    exit 3
fi
