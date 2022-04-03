######## run 7 days ########
# -*- coding: utf-8 -*-
import mysql.connector
from utils.gParas import mysqlParas
import logging
import time
from utils.utility import makeDir
from crawler.getItemInfo import getItemInfo
from utils.itemsDict import itemInfoDict

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
    querySql="SELECT DISTINCT goodsCode FROM allGoodsCode"

    mycursor.execute(querySql)
    gcs=mycursor.fetchall()

    insertSql = "INSERT INTO itemInfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                            "%s,%s,%s,%s,%s)"
    for gct in gcs:
        goodsCode=gct[0]
        itemInfo=itemInfoDict.copy()
        getItemInfo(goodsCode=goodsCode,itemInfo=itemInfo)

        val=tuple(itemInfo.values())

        logging.info(f"inserting {goodsCode}'s")
        mycursor.execute(insertSql,val)
        mydb.commit()
    mydb.close()

    

