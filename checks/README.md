##### mounts_ro_detect
Generate critical error only if disk change current mount options to ro (read-only) or stale state. Because filesystem availability checks with 'df'check_mk/checks/df, so, 'unknown' state is mindless. If you not agree with it -- change  **return 0, "Filesystem not mounted, but it is OK"** to  **return 1, "Filesystem is not mounted"**.
