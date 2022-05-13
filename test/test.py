import datetime
import json
import random
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
from influxdb import InfluxDBClient

from utils.utility import getMostRecentlyUpdatedMeasurement,findNextGC
from crawler.getItemReviews import downloadItemReviews,downloadCommonReviews

makeDir("./testLog")
date = time.strftime("%Y-%m-%d", time.localtime())
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=f"./testLog/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

if __name__=="__main__":

    influxClient = InfluxDBClient(
        host=utils.gParas.influxParas["host"],
        username=utils.gParas.influxParas["user"],
        password=utils.gParas.influxParas["password"],
        database="itemSummary"
    )

    # print(random.uniform(0.2, 0.6))
    # 0.2945531285167854
    # print(random.randint(2, 6))
    def rand(price):
        r=random.random()
        if r<0.1:
            price+=1
        elif r<0.2:
            price-=1
        else:
            pass
        return price

    for i in range(30):
        goodsCode="2004450830"
        price=rand(5000)
        coupon=""

        json_itemSummary = [
            {
                "measurement": f"gc{goodsCode}",
                "tags": {"test": 1},
                "time":datetime.datetime.now()-datetime.timedelta(days=(30-i)),
                "fields": {
                    'goodsCode': f"{goodsCode}",
                    'price': f"{price}",
                    'coupon': f"{coupon}",
                    'reviewsNum': f"{reviewsNum}",
                    'premiumReviewsNum': f"{premiumReviewsNum}",
                    'commonReviewsNum': f"{commonReviewsNum}",
                    'isSoldOut': f"{isSoldOut}",
                    'score':"88",
                    'payCount':"137",
                },
            }
        ]
        influxClient.write_points(json_itemSummary)

    influxClient.close()


#874714969