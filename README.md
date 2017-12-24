# Custom various check_mk\Nagios plugins and checks

### Monitoring RAID Health on HP-UX, working only with hardware RAID

**The main idea:**
We have cron-task on HP-UX server which check Raid HW every 30 min. and save output to */tmp//tmp/check_mk_check_disk_stdout* file.
Check_mk_agent raise check_disks plugin which displays */tmp//tmp/check_mk_check_disk_stdout* file and embed it to 'check_mk_agent' output.
After that, output analyzing on Nagios-server side.

**A:** Why so complex? Why did you create cron-task?

**Q:** We can not raise saconfig utility too often, because sometimes we can receive this error:
```Tue Oct  3 19:14:00 METDST 2017
crw-rw-rw-   1 bin        bin          6 0x000000 Jan 31  2001 /dev/ciss0
Cannot open /tmp/saconfig.lock
Make sure no other users are currently running saconfig
```

So, we will raise saconfig 2 times per hours.

**Instruction**
1) Create following cron-task on HP-UX (crontab -e):
```#raid monitoring
1,31 * * * * /etc/check_mk/hp_ux_check_RAID_HW.sh
```
2) Create executable file [/etc/check_mk/hp_ux_check_RAID_HW.sh](https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/plugins/hp_ux_check_RAID_HW.sh)

3) Create [/usr/lib/check_mk_agent/plugins/hp_ux_check_RAID_HW_plugin.sh](https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/plugins/hp_ux_check_RAID_HW_plugin.sh) file on HP-UX and make it executable

4) Install [hp_ux_check_disks](https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/checks/hp_ux_check_disks) on Nagios-server (for example, copy it to /opt/omd/versions/1.2.8p25.cre/share/check_mk/checks directory)

### Mounts_ro_detect
Generate critical error only if disk change current mount options to ro (read-only) or stale state. Standart 'mount options' check generate alerts if any mount options is changed, and it is not good, for example, mount options is changed after SELinux change status. And it is OK fot us, we want to control only 'ro' option.
**Instruction**



#### Crushftp_check
[Crushftp](http://www.crushftp.com/) -- proprietary  FTP-server for medium and large business. 

**crushftp.py is checking:**
1) CrushFTP is alive or not (search the process with description java -Ddir=/app/CrushFTP8_PC/, -Ddir can be changed via --installed_dir options).
2) Check CrushFTP process uptime. If CrushFTP process less than N (--min_alive options) minutes (if CrushFTP service has been crashed and restore automatically) -- warning will be raised 
3) Try to authrized on web-interface via http\https protocol and get list of files and check hash of test file. Check http\https status codes. If status codes not 200 (not OK) -- crit. incident will be raised
4) Try to login to server via ftp and get test file size. If size of test file wrong -- incident will be raised
5) Try to authorization via sftp protocol and check test file content  

**Instruction**
**before start:**  create test user (--username option) on CrushFTP, create file hello with content 'Hello?' in test user home directory  
run ./crushftp.py --help for get help  
**usage example:**  crush_ftp /etc/check_mk/crushftp.py  -i 192.168.1.22 -p 0,443,0,2222 -t 25 -u test_account -pass 'mypassword' -c '/app/CrushFTP8_PC' -a 300  2>/dev/null  
