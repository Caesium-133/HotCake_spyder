######## run 7 days ########
# -*- coding: utf-8 -*-
import sys

sys.path.append("../")
import mysql.connector
from utils.gParas import mysqlParas
import logging
import time
from utils.utility import makeDir
from crawler.getItemInfo import getItemInfo
from utils.itemsDict import itemInfoDict
import utils.gParas
from utils.MyException import UnWantedGSException
from tqdm import tqdm

if __name__ == "__main__":
    makeDir("./log/itemInfo")
    date = time.strftime("%Y-%m", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/itemInfo/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        port="35687",
        passwd=mysqlParas["passwd"],
        database="spyder",
        auth_plugin = 'mysql_native_password'
    )
    mycursor = mydb.cursor()
    interuptGC = "1668465307"
    limitsql = f" limit {utils.gParas.updateItemNumOnceOfInfo}" if utils.gParas.updateItemNumOnceOfInfo != 0 else ""
    startSql = f" where id <= (select id from allGoodsCode where goodsCode = {interuptGC} limit 1) " if interuptGC else ""
    orderBySql = " ORDER BY id desc "
    querySql = "SELECT DISTINCT goodsCode FROM allGoodsCode" + startSql + orderBySql + limitsql
    insertSql = "INSERT INTO itemInfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                "%s,%s,%s,%s,%s,%s,%s,%s)"

    mycursor.execute(querySql)
    gcs = mycursor.fetchall()
    for gc in gcs:
        goodsCode = gc[0]
        print(goodsCode)
        itemInfo = itemInfoDict.copy()
        try:
            getItemInfo(goodsCode=goodsCode, itemInfo=itemInfo)
        except UnWantedGSException:
            logging.info(f"{goodsCode} is unwanted.")
            mycursor.execute("delete from allGoodsCode where goodsCode=%s", (goodsCode,))
            mydb.commit()
            continue
        except Exception as e:
            print(goodsCode + "meets error:")
            raise e

        val = tuple(itemInfo.values())



        logging.info(f"inserting {goodsCode}'s")
        mycursor.execute(insertSql, val)
        mydb.commit()

    mydb.close()

# https://gtour.gmarket.co.kr/TourV2/Item?GoodsCode=1769279748
