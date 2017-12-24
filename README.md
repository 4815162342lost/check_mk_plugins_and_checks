# check_mk_plugins_and_checks
#Nagios, monitoring RAID Health on HP-UX

The main idea:
We have cron-task on HP-UX server which check Raid HW every 30 min. and save output to /tmp//tmp/check_mk_check_disk_stdout file.
Check_mk_agent raise check_disks plugin which displays /tmp//tmp/check_mk_check_disk_stdout file and embed it to 'check_mk_agent' output.
After that output analyzing on Nagios-server side.

A: Why so complex? Why did you create cron-task?
Q: We can not raise saconfig utility too often, because sometimes we can receive this error:
Tue Oct  3 19:14:00 METDST 2017
crw-rw-rw-   1 bin        bin          6 0x000000 Jan 31  2001 /dev/ciss0
Cannot open /tmp/saconfig.lock
Make sure no other users are currently running saconfig

So, we will raise saconfig 2 times per hours.


1) Create following cron-task on HP-UX (crontab -e):
#raid monitoring
1,31 * * * * /etc/check_mk/hp_ux_check_RAID_HW.sh

2) Create /usr/lib/check_mk_agent/plugins/hp_ux_check_RAID_HW_plugin.sh file on HP-UX:
echo '<<<hp_ux_raid_check>>>'
cat /tmp/check_mk_check_disk_stdout

