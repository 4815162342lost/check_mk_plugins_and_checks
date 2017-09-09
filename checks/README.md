#### mounts_ro_detect
Generate critical error only if disk change current mount options to ro (read-only) or stale state. Because filesystem availability checks with 'df'check_mk/checks/df, so, 'unknown' state is mindless. If you not agree with it -- change  **return 0, "Filesystem not mounted, but it is OK"** to  **return 1, "Filesystem is not mounted"**.


#### hp_ux_check_disks
Check physical disk status (disk is OK or not). The check is analyze output of the saconfig $device command. Tested only on HP-UX 11.31. Requires [hp_ux_check_disk.sh](https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/plugins/hp_ux_check_disk.sh) plugin.


#### hp_ux_check_disks_total_status
Check RAID total status (OK or not). Tested only on HP UX 11.31. Requires [hp_ux_check_disk.sh](https://github.com/4815162342lost/check_mk_plugins_and_checks/blob/master/plugins/hp_ux_check_disk.sh) plugin.
