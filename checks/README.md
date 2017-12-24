### Several custom checks for check_mk 
This page provides short description and link to  full description for each script.

#### hp_ux_check_disks
Check hardware RAID status on HP-UX. The check is analyze output of the saconfig $device command. Tested only on HP-UX 11.31.
[Full descriptions and instruction](https://github.com/4815162342lost/check_mk_plugins_and_checks#monitoring-raid-health-on-hp-ux-working-only-with-hardware-raid)

#### mounts_ro_detect
Generate critical error only if disk change current mount options to *ro* (read-only) or stale state.
[Full descriptions and instruction](https://github.com/4815162342lost/check_mk_plugins_and_checks#mounts_ro_detect)
