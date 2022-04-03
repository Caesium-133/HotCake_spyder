'''
    update every 10 days
'''
import sys
sys.path.append("../")
import requests
from bs4 import BeautifulSoup
import time
from utils.MyException import *
from utils.gParas import wait_time, mysqlParas,isDebug
import logging
import mysql.connector
from utils.manProxy import getHtml
from retry import retry
from utils.MyDecoration import debug

debugMethod="time"

@retry(exceptions=UnableToDealException, tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=isDebug,method=debugMethod)
def getAllCategories():
    url = "http://corners.gmarket.co.kr/BestSellers?viewType=C"
    webData = getHtml(url)
    soup = BeautifulSoup(webData.text, 'lxml')

    cateTab = soup.select_one("#categoryTabC")
    if cateTab is None:
        logging.error("no cat tab for best sellers")
        raise UnableToDealException("NoCatTab")
    cates = cateTab.select("div")
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
                getMediumCategories(data=catDict)


def getMediumCategories(data):
    time.sleep(wait_time / 2)
    largeCatCode = data["largeCatCode"]
    url = f"http://corners.gmarket.co.kr/BestSellers?viewType=C&largeCategoryCode={largeCatCode}"
    webData = getHtml(url)
    soup = BeautifulSoup(webData.text, 'lxml')
    catList = soup.select_one("#mediumCategoryListBtnBox")
    if catList is None:
        logging.warning(f"no medium cat list for {largeCatCode}")
        return
    lis = catList.select("li")
    for li in lis:
        if li:
            href = li.a["href"]
            catCode = href.split("=")[-1] if href else None
            catName = li.get_text()
            data["mediumCatCode"] = catCode
            data["mediumCatTitle"] = catName
            getSmallCategories(data)


def getSmallCategories(data):
    # TODO 有数据库操纵
    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()

    time.sleep(wait_time / 2)
    largeCatCode = data["largeCatCode"]
    mediumCatCode = data["mediumCatCode"]
    sql = "INSERT INTO categories VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    url = f"http://corners.gmarket.co.kr/Bestsellers?viewType=C&largeCategoryCode={largeCatCode}&mediumCategoryCode={mediumCatCode}"
    webData = getHtml(url)
    soup = BeautifulSoup(webData.text, 'lxml')
    catList = soup.select_one("#largeCategoryListBtnBox")
    if catList is None:
        logging.warning(f"no small cat list for {mediumCatCode}")
        return
    lis = catList.select("li")
    valList = []
    for li in lis:
        if li:
            href = li.a["href"]
            catCode = href.split("=")[-1] if href else None
            catName = li.get_text()
            data["smallCatCode"] = catCode
            data["smallCatTitle"] = catName
            data["updateDate"] = time.strftime("%Y-%m-%d", time.localtime())
            valList.append(tuple(data.values()))
    val = valList
    try:
        mycursor.executemany(sql, val)
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        pass
    mydb.close()
