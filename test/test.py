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

url = utils.gParas.itemUrl + "2187712609"
webdata=requests.get(url)
with open("test.html","w+",encoding="utf-8") as file:
    file.write(webdata.text)

