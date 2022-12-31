import requests

url = "http://192.168.126.132/index.html"
r=requests.get(url, 
    headers={
        "User-Agent":"text"})