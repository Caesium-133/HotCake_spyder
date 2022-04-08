import json
import re
import time

import utils.gParas
from bs4 import BeautifulSoup
import requests
import json
import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = utils.gParas.itemUrl + "1769279748"
options=webdriver.ChromeOptions()
options.headless=True
webdata = requests.get(url=url, timeout=5)
redirectUrl = re.findall(r"document.location.replace\(\".*?\"\);", webdata.text)
url=redirectUrl[0].split("\"")[1]
driver=webdriver.Chrome(options=options)
wait=WebDriverWait(driver,10)

driver.get(url)
wait.until(
    EC.presence_of_all_elements_located((By.ID,"header"))
)
data=driver.page_source
# webdata = requests.get(url=url, timeout=5)
# while redirectUrl:
#     url = redirectUrl[0].split("\"")[1]
#     print(url)
#     webdata = requests.get(url=url, timeout=5)
#     redirectUrl = re.findall(r"document.location.replace\(\".*?\"\);", webdata.text)

with open("test.html","w+",encoding="utf-8") as file:
    file.write(data)

driver.quit()

