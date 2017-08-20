#!/usr/bin/python3
'''
Return codes:
0 -- all OK with CrushFTP programm,
1 -- warning (if crushftp process alive time less than 300 sec),
2 -- critical (web-interface is not available, port is not listening, authorization is not work or crushftp process is dead)
return True in function -- if something bad '''

import requests
import psutil
import time
import argparse
import  ftplib
import paramiko

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip', type=str, required=True, default=300, help='CrushFTP ip address')
parser.add_argument('-p', '--ports', type=str, required=True, help='ports which should be listened by application: http, https, ftp, sftp, etc. Order is important! If your Crushftp do not use any protocol, put 0. ')
parser.add_argument('-t', '--timeout', type=int, required=False, default=30, help='timeout for http request to web-interface (default=30)')
parser.add_argument('-u', '--username', type=str, required=True, help='crushftp account for monitoring ')
parser.add_argument('-pass', '--password', type=str, required=True, help='password crushftp account for monitoring')
parser.add_argument('-c', '--installed_dir', type=str, required=True, help='CrushFTP installed directory')
parser.add_argument('-a', '--min_alive', type=int, required=False, default=300, help='crushftp process minimum alive time in seconds (default=300)')
args = parser.parse_args()

total_message=[]
alarm_level=0
total_alarm_level=0
crit=False

targer_ports_list=args.ports.split(",")

def check_proc():
    '''search crushFTP process, return pid, listened ports by Crushftp, Crushftp timeout.
       Emergency exit if process not found
       alarm level: critical'''
    proc_tree = psutil.process_iter()
    for i in proc_tree:
        if i.name() == 'java' and i.ppid() == 1 and i.cwd() == args.installed_dir:
            pid = i.pid
#            ports = i.connections(kind='tcp')
            proc_alive_time = time.time() - i.create_time()
#            return pid, ports, proc_alive_time
            return pid, proc_alive_time
    print("Critical error: crushftp is dead!")
    exit(2)


def check_uptime(proc_uptime):
    '''check CrushFTP uptime. return Warning if uptime is too low
    alarm level: warning'''
    if proc_uptime < args.min_alive:
        return "process uptime is too low... Only " + str(round(proc_uptime)) + ' sec', 1
    else:
        return '', 0


def check_authorization(http_port, https_port):
    '''Try to authorized on crushftp and show files (check authorization + web-interface)
    alarm level: critical -- web-interface is not available, warning level -- incorrect login or can not get list of files'''
    if http_port:
        cookie_port=http_port
        authorization_protocol='http'
    else:
        cookie_port=https_port
        authorization_protocol = 'https'
    message=''
    params_for_get_cookies = {'username': args.username,
                              'password': args.password,
                              'command': 'login',
                              'skip_login': 'true',
                              'encoded': 'true'}
    try:
        if https_port:
            https_request=requests.get("https://" + str(args.ip) + ":" + str(https_port), timeout=args.timeout, verify=False)
            if https_request.status_code != requests.codes.ok:
                message+="https ptotocol is not available. Https status code: " + https_request.status_code
        if http_port:
            http_request=requests.get("http://" + str(args.ip) + ":" + str(http_port), timeout=args.timeout)
            if http_request.status_code != requests.codes.ok:
                message+="http ptotocol is not available. Http status code: " + http_request.status_code
        crash_request_get_cookie = requests.post(authorization_protocol + "://" + str(args.ip) + ":" + str(cookie_port), data=params_for_get_cookies, timeout=args.timeout, verify=False)
        try:
            params_for_check_file = {'command': 'stat',
                                 'path': '/hello',
                                 'format': 'json',
                                 'c2f': crash_request_get_cookie.cookies['CrushAuth'][-4:]}
        except KeyError:
            message+= "can not get cookies."
            return message, 2
        crash_request_get_info = requests.post(authorization_protocol + "://" + str(args.ip) + ":" + str(cookie_port), data=params_for_check_file, cookies=crash_request_get_cookie.cookies, timeout=args.timeout, verify=False)
        requests.post(authorization_protocol + "://" + str(args.ip) + ":" + str(cookie_port), data={'command' : 'logout', 'c2f' : crash_request_get_cookie.cookies['CrushAuth'][-4:]}, cookies=crash_request_get_cookie.cookies, timeout=args.timeout, verify=False)
        if crash_request_get_info.text.find("04c9433b") == -1:
            message += "can not find file with hash 04c9433b on crushftp server, check {auth} protocol".format(auth=authorization_protocol)
    except:
        return "can not get request to CrushFtp web-interface: connection troubles. ", 2
    if message:
        return message, 2
    return '', 0

def check_ports(ports):
    '''check all ports which shoul be listened by application (optino -p)
    alarm level: critical'''
    listened_ports_list=[]
    for i in ports:
        listened_ports_list.append(str(i[3][1]))
    listened_ports_set=set(listened_ports_list)
    targer_ports_set=set(targer_ports_list)
    try:
        targer_ports_set.remove('0')
    except KeyError:
        pass
    if len(listened_ports_set.intersection(targer_ports_set))!=len(targer_ports_set):
        return "port(s) are not listened: " + str(','.join(targer_ports_set-listened_ports_set)), 2
    else:
        return '', 0

def check_ftp_connection(port_ftp):
    '''try to authorized on CrushFTP via ssh and compare test file size'''
    try:
        crush_ftp_con = ftplib.FTP()
        crush_ftp_con.connect(host=args.ip, port=port_ftp, timeout=args.timeout)
        crush_ftp_con.login(user=args.username, passwd=args.password)
        if crush_ftp_con.size('/hello') != 7:
            return "test file size is wrong! Probably ftp protocol works incorrect!", 1
        crush_ftp_con.close()
    except:
        return "CrushFTP is not available via ftp protocol", 2
    return '', 0

def check_sftp_connection(port_sftp):
    '''try to authorized on CrushFTP via sftp and sownload file'''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=args.ip, port=port_sftp, username=args.username, password=args.password,timeout=args.timeout)
        sftp_con = ssh.open_sftp()
        if sftp_con.file('/hello', mode='r', bufsize=-1).read().decode().find("Hello") == -1:
            sftp_con.close()
            return "test file not found! Probably sftp protocol works incorrect!", 2
        sftp_con.close()
    except:
        return "CrushFTP is not available via sftp protocol", 2
    return '', 0


def result_processing(func_output):
    if func_output[1]:
        global total_message
        global total_alarm_level
        total_alarm_level += func_output[1]
        total_message.append(func_output[0])

#pid, ports, proc_alive_time = check_proc()
pid, proc_alive_time = check_proc()

result_processing(check_uptime(proc_alive_time))
#result_processing(check_ports(ports))
if int(targer_ports_list[2]):
    result_processing(check_ftp_connection(int(targer_ports_list[2])))
if int(targer_ports_list[3]):
    result_processing(check_sftp_connection(int(targer_ports_list[3])))
if int(targer_ports_list[0]) or int(targer_ports_list[1]):
    result_processing(check_authorization(int(targer_ports_list[0]), int(targer_ports_list[1])))

if total_alarm_level == 0:
    if proc_alive_time/60/60<1:
        uptime=str(round(proc_alive_time/60,1)) + ' min'
    elif proc_alive_time/60/60/24<1:
        uptime = str(round(proc_alive_time /60/60, 1)) + ' hours'
    else:
        uptime = str(round(proc_alive_time /60/60/24, 1)) + ' days'
    print("All OK with Crushftp. pid: {pid}, uptime: ".format(pid=pid) + uptime)
    exit(0)
else:
    if total_alarm_level>2:
        total_alarm_level=2
    message_for_print= ('Warning: ', 'Critical error: ')
    print(message_for_print[total_alarm_level-1],', '.join(total_message))
    exit(total_alarm_level)
