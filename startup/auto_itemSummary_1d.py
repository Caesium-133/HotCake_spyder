######## run every day ########
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import logging
from crawler.getItemInfo import getItemSummary
import time
import mysql.connector
from utils.utility import makeDir
from utils.gParas import mysqlParas, influxParas
from influxdb import InfluxDBClient
from utils.itemsDict import itemInfoSummaryDict

if __name__ == "__main__":
    makeDir("./log/itemSummary")
    date = time.strftime("%Y-%m", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/itemSummary/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)


    influxClient = InfluxDBClient(
        host=influxParas["host"],
        username=influxParas["user"],
        password=influxParas["password"],
        database="ItemSummaries"
    )

    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    sql = "SELECT goodsCode FROM allGoodsCode"
    mycursor.execute(sql)
    gcs = mycursor.fetchall()  # gcs is a list of tuples
    mydb.close()

    for gct in gcs:
        goodsCode = gct[0]
        itemInfoSummary=itemInfoSummaryDict.copy()
        try:
            getItemSummary(goodsCode, itemInfoSummary)
        except:
            logging.warning(f"skipping {goodsCode}")
            continue
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

    