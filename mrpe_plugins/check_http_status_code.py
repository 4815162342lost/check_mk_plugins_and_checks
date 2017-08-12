#!/usr/bin/python3
'''Simple script for check http status code.
exit codes: 0 -- al OK (httpd status code = 200), 2 -- error (connection troubles or http status code not 200)
using: check_http_status_code.py site timeout_in_seconds
mrpe.cfg example:
yandex_check /etc/check-mk-agent/check_http_status_code.py "http://yandex.ru" 10'''

import requests
import os
import sys

web_site=sys.argv[1]
timeout=float(sys.argv[2])

try:
    r=requests.get(web_site, timeout=timeout)
except:
    print("Critical error: connection troubles")
    exit(2)

if r.status_code == requests.codes.ok:
    print("OK: all OK. Http status code: 200")
    exit(0)
else:
    print("Critical error! Http status code: {status_code}".format(status_code = r.status_code))
exit(2)
