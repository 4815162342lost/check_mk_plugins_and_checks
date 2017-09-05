#!/usr/local/bin/bash
echo '<<<hp_ux_physical_disks>>>'
devices=`ls /dev/ciss*`
for device in $devices
do
saconfig $device | grep '^Internal'
done
echo '<<<hp_ux_physical_disks_total>>>'
for device in $devices
do
dev=`echo "$device" | sed  "s/.*\///"`
saconfig $device | grep '^Status' | sed "s/Status/Status_$dev/"
done
