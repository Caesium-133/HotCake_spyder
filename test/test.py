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
from utils.MyException import UnWantedGSException,UnableToDealException,NoRespondException,WeNeedCheckException
import csv

from utils.utility import getMostRecentlyUpdatedMeasurement
from crawler.getItemReviews import downloadItemReviews

makeDir("./testLog")
date = time.strftime("%Y-%m-%d", time.localtime())
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=f"./testLog/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

mydb = mysql.connector.connect(
        host=utils.gParas.mysqlParas["host"],
        user=utils.gParas.mysqlParas["user"],
        passwd=utils.gParas.mysqlParas["passwd"],
        database="spyder"
    )
mycursor = mydb.cursor()
querySql="SELECT goodsCode FROM itemInfo WHERE LENGTH(cat_2_code)<8"
mycursor.execute(querySql)
gcs = mycursor.fetchall()

headers = ["goodsCode"]
for i in range(0,4):
    headers.append(f"cat_{i}")
    headers.append(f"cat_{i}_code")

with open(f"./smileDelivery.csv", "w", newline='', encoding='utf-8') as file:
    if file is None:
        logging.critical("unable to open or write into review file")
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
cdl=[]
for gc in gcs:
    goodsCode = gc[0]
    print(goodsCode)
    url = utils.gParas.itemUrl + f"{goodsCode}"
    catDict={}
    catDict["goodsCode"] = goodsCode

    webData = getHtml(url)
    if webData == isTour or webData == isNoItem:
        raise UnWantedGSException
    if webData is None:
        logging.error(f"no info respond for {goodsCode}")
        raise NoRespondException("InfoPage")
    soup = BeautifulSoup(webData, 'lxml')

    navi = soup.find("div", class_="location-navi")
    if navi is None:
        logging.error(f"no navi bar for {goodsCode}")
        raise WeNeedCheckException("noNaviBar")
    cats = navi.select("li")
    i = 0
    for cat in cats:
        catName = cat.find("a")
        catDict[f"cat_{i}"] = catName.text.replace(",", "/") if catName else None
        if catName:
            catCode = ""
            try:
                if i == 1:
                    catLink = catName.get("href")
                    catCode = re.findall("\d+", catLink)[-1]
                if i > 1:
                    catLink = catName.get("href")
                    catCode = catLink.split("=")[-1]
            except:
                logging.info(f"{goodsCode} has less than 3 cats")
                break
            finally:
                catDict[f"cat_{i}_code"] = catCode
        i += 1
    # cdl.append(catDict)
    with open(f"./smileDelivery.csv", "a", newline='', encoding='utf-8') as file:
        if file is None:
            logging.error("unable to append into review file")
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(catDict)


mydb.close()



#874714969