import sys
sys.path.append("../")
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from utils.MyException import *
from utils.gParas import wait_time, mysqlParas,isDebug
import logging
import mysql.connector
import tqdm
from utils.manProxy import getHtml
from retry import retry
from utils.MyDecoration import debug

# from selenium import webdriver

debugMethod="time"

# update every hour
@retry(exceptions=UnableToDealException, tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=isDebug,method=debugMethod)
def getBestSellersByAll():
    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO BestSellersOfAll VALUES(%s,%s,%s)"
    url = "http://corners.gmarket.co.kr/Bestsellers"

    webData = getHtml(url)
    soup = BeautifulSoup(webData, "lxml")

    # driver = webdriver.Chrome()
    # driver.get(url)

    # def scrollToBottom(tillNum):
    #     times = 0
    #     while True:
    #         time.sleep(wait_time / 2)
    #         driver.execute_script("window.scrollBy(0,1000)")
    #         times += 1
    #         if times == int(tillNum / 10):
    #             return
    #
    # scrollToBottom(200)
    # content = driver.page_source.encode("utf-8")
    # soup = BeautifulSoup(content.decode(), "lxml")
    # with open("test.html","w",encoding="utf-8") as file:
    #     file.write(content.decode())
    # driver.close()
    # bestSellerDictList = []
    bestSellers = []

    # bestLists = soup.find_all("div",class_="best-list")
    # bestList=None
    # for bl in bestLists:
    #     if bl.id is None:
    #         if bl.find("li") is not None:
    #             bestList=bl
    bestList = soup.select_one("div.best-list:nth-child(3)")
    if bestList is None:
        logging.error("not found best list.")
        raise UnableToDealException("no best list")
    _list = bestList.select("li")
    date = time.strftime("%Y-%m-%d-%H", time.localtime())
    ranking = 0
    for item in _list:
        ranking += 1
        data_a = item.select_one("a", class_="itemname")["onclick"]
        data_s = re.findall("{.*}", data_a)[0].replace("\'", "\"")
        data = json.loads(data_s)
        goodsCode = data["goodsCode"]
        # bsDict={"goodsCode":goodsCode,"date":date,"rank":ranking}
        # bestSellerDictList.append(bsDict)
        bestSellers.append((goodsCode, date, ranking))

    val = bestSellers
    mycursor.executemany(sql, val)
    mydb.commit()
    logging.info("writing bsA")

    mydb.close()


# update evey 6 hours
@retry(exceptions=UnableToDealException, tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=isDebug,method=debugMethod)
def getBestSellersByEachCat():
    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()

    if isDebug:
        logging.info("connected")

    fetchSQL = "SELECT distinct largeCatCode FROM categories;"
    mycursor.execute(fetchSQL)
    lccs = mycursor.fetchall()
    if isDebug:
        logging.info(len(lccs))
    for lcc in lccs:
        time.sleep(wait_time / 2)
        url = f"http://corners.gmarket.co.kr/Bestsellers?viewType=C&largeCategoryCode={lcc[0]}"
        webData = getHtml(url)
        soup = BeautifulSoup(webData, "lxml")

        if isDebug:
            logging.info("got web data")

        bestSellers = []
        bestList = soup.select_one("div.best-list:nth-child(3)")
        if bestList is None:
            logging.error(f"not found best list of {lcc}.")
            raise UnableToDealException("no best list")
        _list = bestList.select("li")
        date = time.strftime("%Y-%m-%d-%H", time.localtime())
        for item in _list:
            data_a = item.select_one("a", class_="itemname")["onclick"]
            data_s = re.findall("{.*}", data_a)[0].replace("\'", "\"")
            data = json.loads(data_s)
            goodsCode = data["goodsCode"]
            # bsDict={"goodsCode":goodsCode,"date":date,"rank":ranking}
            # bestSellerDictList.append(bsDict)
            bestSellers.append((goodsCode, date, lcc[0]))
        insertSQL = "INSERT INTO BestSellersOfEachCat VALUES(%s,%s,%s)"
        val = bestSellers
        logging.info(f"inserting {lcc[0]}'s")
        mycursor.executemany(insertSQL, val)
        mydb.commit()
        logging.info("writing bsEC")

    mydb.close()


'''
#categoryTabC > div.cate1
#mediumCategoryListBtnBox 
#gBestWrap > div > div:nth-child(5) > div:nth-child(3)
div.best-list:nth-child(3)
'''
