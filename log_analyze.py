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

    with open('/var/log/apache2/error.log') as file2:
        st_results = os.stat('/var/log/apache2/error.log')
        st_size = st_results[6]
        file2.seek(st_size)
        # for entry1 in parser_error1.parse_lines(fp):
        #     print(str(entry1.variables['time']))
        #     if str(entry1.variables['type']) == ':error':  # doctest: +SKIP
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
            # if "Invalid" in entry.variables['msg']:
            #     print(f"{entry_time.strftime('%H:%M:%S.%f')}: {entry.variables['msg']}")
            time.sleep(0.01)
            # print(str(entry_time))
        # for entry in parser_error.parse_lines(file2, ignore_invalid=True):
            # print(str(entry.request_time_fields["timestamp"].strftime("%H:%M:%S")),  str(entry.variables['msg']))
# error_handler()
            # if (entry.request_time_fields["timestamp"] - time).total_seconds() > 0:
                # print("hehe")
                # return 1
            # print(times[str(entry.request_time_fields["timestamp"])])
            # print(entry.request_time_fields["timestamp"].tzinfo)
            # if not last_time:
            #     last_time = str(entry.request_time_fields["timestamp"])
            #     times[last_time] = {}
            # if last_time != str(entry.request_time_fields["timestamp"]):
            #     times[str(entry.request_time_fields["timestamp"])] = {}
            # print(str(last_time))
            # if entry.remote_address in times[str(entry.request_time_fields["timestamp"])]:
            #     times[str(entry.request_time_fields["timestamp"])][entry.remote_address] += 1
            # else:
            #     times[str(entry.request_time_fields["timestamp"])][entry.remote_address] = 0
            # print(f"\t{entry.remote_address}: "+ str(times[last_time][entry.remote_address]))
            # last_time = str(entry.request_time_fields["timestamp"])
            # print(str(entry.request_time), entry.request_line)
            # time.sleep(TIME_WAIT)




# parser_error1 = LogParser('[%{%a %b %d %T %g}t] [:%{type}x] %{ahihi}x')
parser_error1 = LogParser('[%{time}x] [%{type}x] %{ahihi}x')

# [Wed Dec 14 07:58:20.948127 2022] [:error] [pid 2725:tid 140013308208704] [client 192.168.126.1:64436] 
# [client 192.168.126.1] ModSecurity: Warning. Operator GE matched 2 at IP:dos_burst_counter. 
# [file "/etc/apache2/modsecurity-crs/coreruleset-3.3.0/rules/custom-dos.conf"] [line "1426"] 
# [id "912170"] [msg "Potential Denial of Service (DoS) Attack from 192.168.126.1 - # of Request Bursts: 2"] 
# [ver "OWASP_CRS/3.3.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] 
# [tag "paranoia-level/1"] [tag "attack-dos"] [tag "OWASP_CRS"] [tag "capec/1000/210/227/469"] 
# [
# hostname "192.168.126.132"] [uri "/index.html"] [unique_id "Y5kfrCTnEYigCBujxG7_aAAAAIo"]

# parser_error = LogParser('[%{time}x] [%{type}x] [pid %{pid}P:tid %{tid}P] [client %a] '
#                         '[client %h] ModSecurity: %{error_content}x [file "%{file}x"] [line "%{line}x"] ' 
#                         '[id "%{line}x"] [msg "%{msg}x"] [ver "%{ver}x"] %{tags}x [hostname "%{hostname}x"] '
#                         '[uri "%U"] [unique_id "%{unique_id}x"]')


# access_handler()
