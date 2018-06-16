#!/usr/bin/python3
"""
example: need determine the opened files by telegram program.
firstly, need find programm via ps command:
vodka@vodka-PC:/tmp$ ps -Af | grep -i telegram
vodka     7382  2917  1 11:51 tty2     00:00:31 telegram-desktop --
We can see thet telegram runs under vodka user. Let's chrck CMD options:
vodka@vodka-PC:/tmp$ ps -p 7382 -f
UID        PID  PPID  C STIME TTY          TIME CMD
vodka     7382  2917  1 11:51 tty2     00:00:31 telegram-desktop --
CMD in our case is telegram-desktop --. We should put any part of cmd to cmd option.
Example:
vodka@vodka-PC:/tmp$ ./1.py --username vodka --process_name telegram-desktop --cmd 'telegram' --warning 70 --critical 90
Current opened files: 39 by process with pid=7382. Warn/crit: 2867/3686 |opened_files=39;2867;3686
Warn\crit -- you shoul set it in percentage. Also you can set limit (maximum opened files by process manualy if your kernel doesn not support (psutil.RLIMIT_NOFILE) features)
"""
import glob
import psutil
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", type=str, required=True, help="process owner")
parser.add_argument("-n", "--process_name", type=str, required=True, help="process name")
parser.add_argument("-cmd", "--cmd",type=str, required=True, help="any part of cmdline. Searck function will be used")
parser.add_argument("-w", "--warning", type=float, required=True, help="warning level in percentage")
parser.add_argument("-c", "--critical", type=float, required=True, help="critical level in percentage")
parser.add_argument("-l", "--limit", type=int, required=False, help="current limit for maximum opened files", default=4096)
args=parser.parse_args()
for proc in psutil.process_iter():
    if proc.username()==args.username and proc.name()==args.process_name and str(proc.cmdline()).find(args.cmd)!=-1:
        try:
            max_limit=int(proc.rlimit(psutil.RLIMIT_NOFILE))
        except:
            max_limit=args.limit
        warn=int(max_limit*(args.warning/100))
        crit=int(max_limit*(args.critical/100))
        files_count=len(glob.glob("/proc/" + str(proc.pid) + "/fd/*"))
        if int(files_count)>crit:
            print("Current opened files: {files_count} by process with pid={pid}. Warn/crit: {warn}/{crit} |opened_files={files_count};{warn};{crit}".format(files_count=files_count, pid=proc.pid, warn=warn, cri$
            exit(2)
        elif int(files_count)>warn:
            print("Current opened files: {files_count} by process with pid={pid}. Warn/crit: {warn}/{crit} |opened_files={files_count};{warn};{crit}".format(files_count=files_count, pid=proc.pid, warn=warn, cri$
            exit(1)
        else:
            print("Current opened files: {files_count} by process with pid={pid}. Warn/crit: {warn}/{crit} |opened_files={files_count};{warn};{crit}".format(files_count=files_count, pid=proc.pid, warn=warn, cri$
            exit(0)
print("Process is not running")
exit(3)
