import re
import influxdb
from utils.gParas import influxParas
import json
import time
from tqdm import tqdm


##### words #####
isTour = "this is a tourism product"
isNoItem = "this is a blank page"
isGetReviewsSummary = "get reviews summary"


##### functions #####

def getReviewGrade(reviewGrade):
    goodsGrade = "d"
    if reviewGrade.find("span", class_="rec_a"):
        goodsGrade = "a"
    elif reviewGrade.find("span", class_="rec_b"):
        goodsGrade = "b"
    elif reviewGrade.find("span", class_="rec_c"):
        goodsGrade = "c"
    elif reviewGrade.find("span", class_="rec_d"):
        goodsGrade = "d"

    deliveryGrade = "d"
    if reviewGrade.find("span", class_="dev_a"):
        deliveryGrade = "a"
    elif reviewGrade.find("span", class_="dev_b"):
        deliveryGrade = "b"
    elif reviewGrade.find("span", class_="dev_c"):
        deliveryGrade = "c"
    elif reviewGrade.find("span", class_="dev_d"):
        deliveryGrade = "d"

    return {"goodsGrade": goodsGrade,
            "deliveryGrade": deliveryGrade}


def getItemInfoString(s):
    if s is None:
        return None
    if s == "상세설명참고" or s == "상세페이지참조":
        return None
    s = s.replace(",", " ")
    s = re.sub("\(.*\)", "", s)
    return s


def makeDir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")

    try:
        os.makedirs(path)
        return True
    except:
        return False


def getMostRecentlyUpdatedMeasurement():
    influxClient = influxdb.InfluxDBClient(
        host=influxParas["host"],
        username=influxParas["user"],
        password=influxParas["password"],
        database="ItemSummaries"
    )
    gcms = influxClient.get_list_measurements()
    foundLastTime = ""
    foundLastGC = ""
    for gcm in gcms:
        measurement = gcm["name"]
        goodsCode = measurement.split("c")[-1]
        lastTime = influxClient.query(f"select last(goodsCode), time from {measurement}")
        lastTimeRaw = lastTime.raw
        lt = lastTimeRaw["series"][0]["values"][0][0]
        if lt > foundLastTime:
            foundLastTime = lt
            foundLastGC = goodsCode
    return foundLastGC


def writeToFile(filename: str, content: str):
    with open(filename, "w+", encoding='utf-8') as file:
        file.write(content)


def appendToFile(filename: str, content: str):
    with open(filename, "a+", encoding='utf-8') as file:
        file.write(content)


def filter_emoji(desstr, restr=''):
    res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res.sub(restr, desstr)

def findNextGC(currentGC,cursor):
    cursor.execute("select goodsCode from allgoodscode where id < (select id from allgoodscode where goodsCode=%s) order by id desc limit 1;",(currentGC,))
    gcl=cursor.fetchall()
    gc=gcl[0][0]
    return gc

def getLastGCbyremaining(cursor,hmrm=-1):
    if hmrm==-1:
        return ""
    SQL=f"select goodsCode from allgoodscode order by id asc limit {hmrm},1 "
    cursor.execute(SQL)
    lastGC=cursor.fetchall() #list of tuple
    lastGC=lastGC[0][0]
    return lastGC