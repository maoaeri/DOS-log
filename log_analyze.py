from apachelogs import LogParser
import time, os
from datetime import datetime

TIME_WAIT = 5
times = {}
MAX = 0
errors = []
#192.168.126.1 - - [25/Dec/2022:12:13:36 +0700] "GET /icons/ubuntu-logo.png HTTP/1.1" 200 3607 
# "http://192.168.126.132/index.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
# Chrome/108.0.0.0 Safari/537.36"

def read_file_line(file):
    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            # print('Waiting...')
            time.sleep(1)
            file.seek(where)
        else:
            return line

def access_handler():
    global times, MAX
    parser_access = LogParser("%a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
    last_time = None
    # while True:
    #     times = {}
    with open('/var/log/apache2/access.log') as file1:
        st_results = os.stat('/var/log/apache2/access.log')
        st_size = st_results[6]
        file1.seek(st_size)
        while True:  # doctest: +SKIP
            entry = parser_access.parse(read_file_line(file1))
            field = entry.request_time_fields["timestamp"].strftime("%H:%M:%S")
            if str(field) in times:
                times[str(field)] += 1
            else:
                times[str(field)] = 1
            if times[str(field)] > MAX:
                MAX = times[str(field)]

#[Wed Dec 14 07:58:20.919155 2022] [:error] [pid 2754:tid 140013417801280] [client 192.168.126.1:64635] 
# [client 192.168.126.1] ModSecurity: Warning. Operator GE matched 2 at IP:dos_burst_counter. 
# [file "/etc/apache2/modsecurity-crs/coreruleset-3.3.0/rules/custom-dos.conf"] [line "1426"] 
# [id "912170"] [msg "Potential Denial of Service (DoS) Attack from 192.168.126.1 - # of Request Bursts: 2"] 
# [ver "OWASP_CRS/3.3.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] 
# [tag "paranoia-level/1"] [tag "attack-dos"] [tag "OWASP_CRS"] [tag "capec/1000/210/227/469"] 
# [hostname "192.168.126.132"] [uri "/index.html"] [unique_id "Y5kfrCuIlX__lXF0SSnuOgAAAQU"]
def error_handler(): #%a %b %d %H:%M:%S.%f %Y
    parser_error = LogParser('[%{strtime}x] [%{type}x] [pid %{pid}P:tid %{tid}P] [client %h] '
                            '[client %a] ModSecurity: %{error_content}x [file "%{file}x"] [line "%{line}x"] '
                            '[id "%{line}x"] [msg "%{msg}x"] [ver "%{ver}x"] %{tags}x [hostname "%{hostname}x"] '
                            '[uri "%U"] [unique_id "%{unique_id}x"]')

    time_format = "%a %b %d %H:%M:%S.%f %Y"
    global errors

    # [Mon Mar 20 07:50:30.174796 2023] [:error] [pid 7814:tid 140046486836800] [client 192.168.126.1:58285] [client 192.168.126.1] ModSecurity: Warning. Operator EQ matched 0 at IP.
    #  [file "/home/ngoctv/custom-dos/custom-dos.conf"] [line "123"] [id "100303"] [msg "Denial of Service (DoS) attack identified from 192.168.126.1 (1 hits since last alert)"
    # ] [tag "attack-dos"] [hostname "192.168.126.132"] [uri "/index.html"] [unique_id "ZBet1ZiaQsdfaW-aDi1tagAAAMc"]

    with open('/var/log/apache2/error.log') as file2:
        st_results = os.stat('/var/log/apache2/error.log')
        st_size = st_results[6]
        file2.seek(st_size)
        while True:
            try:
                entry = parser_error.parse(read_file_line(file2))
            except Exception as e:
                continue
            entry_time = datetime.strptime(entry.variables["strtime"], time_format)
            if len(errors) < 5:
                errors.append(f"{entry_time.strftime('%H:%M:%S.%f')}: {entry.variables['msg']}")
            else:
                errors.pop(0)
                errors.append(f"{entry_time.strftime('%H:%M:%S.%f')}: {entry.variables['msg']}")
            time.sleep(0.01)