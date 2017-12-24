#!/usr/local/bin/bash
#you should create following cron-task (crontab -e):
#1,31 * * * * /etc/check_mk/hp_ux_check_RAID_HW.sh
#also please, copy https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/plugins/hp_ux_check_RAID_HW_plugin.sh
#to /usr/lib/check_mk_agent/plugins/ dir.
#please, send bugs\questions to https://github.com/4815162342lost/check_mk_plugins_and_checks/issues
>/tmp/check_mk_check_disk_stderr
>/tmp/check_mk_check_disk_stdout.new
timestamp=`echo "timestamp $(date +%s)"`
devices=`ls /dev/ciss*`
for device in $devices
do
    saconfig $device 1>/tmp/check_mk_check_disk_stdout.tmp 2>>/tmp/check_mk_check_disk_stderr
    sed "s:^Status:"$device"_status:" /tmp/check_mk_check_disk_stdout.tmp>>/tmp/check_mk_check_disk_stdout.new
done
if [[ `du /tmp/check_mk_check_disk_stderr | cut -c 1` -eq '0' ]]
then
    echo "$timestamp">/tmp/check_mk_check_disk_stdout
    cat /tmp/check_mk_check_disk_stdout.new | grep -E '^timestamp|^Internal|^\/dev'>>/tmp/check_mk_check_disk_stdout
fi
