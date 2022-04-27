######## run every day ########
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import logging
from crawler.getItemInfo import getItemSummary
import time
import mysql.connector
from utils.utility import makeDir, getMostRecentlyUpdatedMeasurement
from utils.gParas import mysqlParas, influxParas
from influxdb import InfluxDBClient
from utils.itemsDict import itemInfoSummaryDict
from utils.MyException import UnWantedGSException
from tqdm import tqdm
import utils.gParas

if __name__ == "__main__":
    makeDir("./log/itemSummary")
    date = time.strftime("%Y-%m", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/itemSummary/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)


    influxClient = InfluxDBClient(
        host=influxParas["host"],
        username=influxParas["user"],
        password=influxParas["password"],
        database="itemSummary"
    )

    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        port="35687",
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    #interuptGC = getMostRecentlyUpdatedMeasurement()
    interuptGC = ""
    limitsql = f" limit {utils.gParas.updateItemNumOnceOfInfo}" if utils.gParas.updateItemNumOnceOfInfo != 0 else ""
    startSql = f" where id <= (select id from allGoodsCode where goodsCode = {interuptGC} limit 1) " if interuptGC else ""
    orderBySql = " ORDER BY id desc "
    querySql = "SELECT DISTINCT goodsCode FROM allGoodsCode" + startSql + orderBySql + limitsql
    mycursor.execute(querySql)
    gcs = mycursor.fetchall()  # gcs is a list of tuples

    for gct in tqdm(gcs):
        goodsCode = gct[0]
        itemInfoSummary=itemInfoSummaryDict.copy()
        try:
            getItemSummary(goodsCode, itemInfoSummary)
        except UnWantedGSException:
            logging.info(f"{goodsCode} is unwanted")
            mycursor.execute("delete from allGoodsCode where goodsCode=%s",(goodsCode,))
            mydb.commit()
            continue
        except Exception as e:
            print(f"{goodsCode} meets error:")
            raise e
        json_itemSummary=[
            {
                "measurement":f"gc{goodsCode}",
                "tags":{"test":1},
                "fields":{
                    'goodsCode': f"{itemInfoSummary['goodsCode']}",
                    'price': f"{itemInfoSummary['price']}",
                    'coupon': f"{itemInfoSummary['coupon']}",
                    'reviewsNum': f"{itemInfoSummary['reviewsNum']}",
                    'premiumReviewsNum': f"{itemInfoSummary['premiumReviewsNum']}",
                    'commonReviewsNum': f"{itemInfoSummary['commonReviewsNum']}",
                    'isSoldOut': f"{itemInfoSummary['isSoldOut']}"
                },
            }
        ]
        logging.info(f"writing {goodsCode}'s")
        influxClient.write_points(json_itemSummary)
    
    influxClient.close()
    mydb.close()

##

    