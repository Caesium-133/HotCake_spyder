import json
import re

from bs4 import BeautifulSoup
import requests
import json

cookie="PHPSESSID=acb49sn5c259m94h7ucrg3ance;XSRF-TOKEN=eyJpdiI6IndSRm1JQVNvaWw4Mm5MamNQZXpWR3c9PSIsInZhbHVlIjoia0NncTN0MlwvMUlTUURUZmhvTVhEbDltMnE5NzNmQnBrN1hJVjk3dkNQall2Z0crY2F6eWcydnJTUEZDMm9VSzQiLCJtYWMiOiJhNDAzZGVhM2ZmNDA2Mzc3MjUyNzc4NWEzM2E3MWMyZDk5OTkyY2I4NzlmYWNkNjljZDZhYWM4NGJlYzYwY2QyIn0=; laravel_session=eyJpdiI6InhNbmdiN3c5c1BIUVprbjdXZTJObnc9PSIsInZhbHVlIjoiS3dcL2ZUSitoUTlzY0NudGpZOGVFZHNSZ0llMjh6S1U1SnJcL3NUSUdnaDlrWjViU3pIMjRrcnlJRzFpWXJpZWRCIiwibWFjIjoiYzgwNThlMzE2MTEyY2JmMWY1NzkxMzAxNmZhYmQ3YTFjM2ZjODk0OGJlZjM1YjY2YWMxZDM3OGNlOGM4OTQzYSJ9 "

apiUrl="https://www.padaili.com/proxyapi?api=zY9GDr3ZYWyBCaitLHzeWNCFF1paO0j1&num=100&type=3&order=jiance"
header={'User-Agent': "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
         'Accept': '*/*',
         'Connection': 'keep-alive',
         'Accept-Language': 'zh-CN,zh;q=0.8'}
apiData=requests.get(apiUrl,headers=header)
proxies=re.findall(r"\d+\.\d+\.\d+\.\d+:\d+",apiData.text)
for proxy in proxies:
    print(proxy)