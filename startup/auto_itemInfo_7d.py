######## run 7 days ########
# -*- coding: utf-8 -*-
import mysql.connector
from utils.gParas import mysqlParas
import logging
import time
from utils.utility import makeDir
from crawler.getItemInfo import getItemInfo
from utils.itemsDict import itemInfoDict
#from utils.MyException import NoRespondException, UnableToDealException, WeNeedCheckException, RetryMayWorkException

if __name__ == "__main__":
    makeDir("./log/itemInfo")
    date = time.strftime("%Y-%m", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/itemInfo/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)
    
    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    querySql="SELECT DISTINCT goodsCode FROM allGoodsCode ORDER BY id desc"

    mycursor.execute(querySql)
    gcs=mycursor.fetchall()

    insertSql = "INSERT INTO itemInfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s)"
    for gct in gcs:
        goodsCode=gct[0]
        itemInfo=itemInfoDict.copy()
        try:
            getItemInfo(goodsCode=goodsCode,itemInfo=itemInfo)
        except Exception as e:
            print(goodsCode+ "meets error:")
            raise e

        val=tuple(itemInfo.values())

        logging.info(f"inserting {goodsCode}'s")
        mycursor.execute(insertSql,val)
        mydb.commit()
    mydb.close()

    
# https://gtour.gmarket.co.kr/TourV2/Item?GoodsCode=1769279748
