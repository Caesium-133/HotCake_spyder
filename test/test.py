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
from utils.utility import isTour,isNoItem
from utils.MyException import UnWantedGSException,UnableToDealException,NoRespondException,WeNeedCheckException
import csv
from utils.itemsDict import itemInfoDict

from utils.utility import getMostRecentlyUpdatedMeasurement,findNextGC
from crawler.getItemReviews import downloadItemReviews,downloadCommonReviews

makeDir("./testLog")
date = time.strftime("%Y-%m-%d", time.localtime())
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=f"./testLog/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

def addd(b):
    b[0]=b[0]+5

if __name__=="__main__":
    webData=requests.get(url="https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1=100&page=2",timeout=5,headers=utils.gParas.headers)
    soup=BeautifulSoup(webData.text,'lxml')
    mainContent=soup.find("div",id="main_content")
    contentUrls=[]
    if mainContent:
        contents=mainContent.findAll("li")
        for content in contents:
            dt=content.find("dt")
            if dt:
                url=dt.a["href"]
                contentUrls.append(url)

    print(contentUrls)
    print(len(contentUrls))


#874714969