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
import time
from utils.manProxy import postHtml

from utils.utility import getMostRecentlyUpdatedMeasurement

premiumPage = postHtml(url="http://item.gmarket.co.kr/Review", data={"goodsCode": "2268968816"},
                           headers=utils.gParas.headers)
with open("test.html","w+",encoding="utf-8") as file:
    file.write(premiumPage)