**crushftp.py is checking:**
1) CrushFTP is alive or not (search the process with description java -Ddir=/app/CrushFTP8_PC/).
2) Check CrushFTP process uptime. If CrushFTP process less than 5 minutes (if CrushFTP service has been crashed and restore automatically) -- incident with warning level will be generated
3) Try to authrized on web-interface via http protocol and get list of files and check hash of test file. Check http\https status codes. If status codes not 200 (not OK) -- crit. incident will be raised
4) Try to login to server via ftp and get test file size. If size of test file wrong -- incident will be raised
5) Try to authorization via sftp protocol and check test file content

#### check_http_status_code.py
Simple script for check http status code.
exit codes: 0 -- al OK (httpd status code = 200), 2 -- error (connection troubles or http status code not 200)
using: check_http_status_code.py site timeout_in_seconds
mrpe.cfg example:
yandex_check /etc/check-mk-agent/check_http_status_code.py "http://yandex.ru" 10
