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
from utils.manProxy import postHtml,getHtml
import logging
from utils.utility import makeDir
from utils.gParas import isTour,isNoItem
from utils.MyException import UnWantedGSException,UnableToDealException
import csv

from utils.utility import getMostRecentlyUpdatedMeasurement
from crawler.getItemReviews import downloadItemReviews

makeDir("./testLog")
date = time.strftime("%Y-%m-%d", time.localtime())
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=f"./testLog/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

url = "http://corners.gmarket.co.kr/BestSellers?viewType=C"
webData = getHtml(url)
if webData==isTour or webData==isNoItem:
    raise UnWantedGSException
soup = BeautifulSoup(webData, 'lxml')

cateTab = soup.select_one("#categoryTabC")
if cateTab is None:
    logging.error("no cat tab for best sellers")
    raise UnableToDealException("NoCatTab")
cates = cateTab.select("div")

headers=["variety","largeCatCode","largeCatTitle"]
with open(f"./variety-largeCat.csv", "w", newline='', encoding='utf-8') as file:
    if file is None:
        logging.critical("unable to open or write into review file")
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
dl=[]
for cate in cates:
    try:
        variety = cate.find("p", class_="top").get_text()
    except:
        raise UnableToDealException("NoTopName")
    lis = cate.select("li")
    for li in lis:
        if li:
            href = li.a["href"]
            categoryCode = href.split("=")[-1] if href else None
            catName = li.get_text()
            catDict = {"variety": variety, "largeCatCode": categoryCode, "largeCatTitle": catName}
            dl.append(catDict)

with open(f"./variety-largeCat.csv", "a", newline='', encoding='utf-8') as file:
    if file is None:
        logging.error("unable to append into review file")
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writerows(dl)



#874714969