#### crushftp.py
[Crushftp](http://www.crushftp.com/) -- proprietary  FTP-server for medium and large business. 

###### **crushftp.py is checking:**
1) CrushFTP is alive or not (search the process with description java -Ddir=/app/CrushFTP8_PC/, -Ddir can be changed via --installed_dir options).
2) Check CrushFTP process uptime. If CrushFTP process less than N (--min_alive options) minutes (if CrushFTP service has been crashed and restore automatically) -- warning will be raised 
3) Try to authrized on web-interface via http\https protocol and get list of files and check hash of test file. Check http\https status codes. If status codes not 200 (not OK) -- crit. incident will be raised
4) Try to login to server via ftp and get test file size. If size of test file wrong -- incident will be raised
5) Try to authorization via sftp protocol and check test file content  

before start: create test user, create file hello with content 'Hello?' in test user home directory  
run ./crushftp.py --help for get help  
usage example: crush_ftp /etc/check_mk/crushftp.py  -i 192.168.1.22 -p 0,443,0,2222 -t 25 -u test_account -pass 'mypassword' -c '/app/CrushFTP8_PC' -a 300  2>/dev/null  


#### check_http_status_code.py
Simple script for check http status code.  
exit codes: 0 -- al OK (httpd status code = 200), 2 -- error (connection troubles or http status code not 200)  
usage: check_http_status_code.py site timeout_in_seconds  
mrpe.cfg example:  
yandex_check /etc/check-mk-agent/check_http_status_code.py "http://yandex.ru" 10  
