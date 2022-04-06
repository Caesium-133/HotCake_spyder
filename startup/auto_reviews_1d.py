######## run every day ########
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import logging
import time
from utils.utility import makeDir
from crawler.getItemReviews import downloadItemReviews
import mysql.connector
from utils.gParas import mysqlParas, shallowCRp,shallowPRp

isDebug=False

if __name__ == "__main__":
    makeDir("./log/reviews")
    date = time.strftime("%Y-%m-%d", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/reviews/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

    logging.info("downloading reviews")

    mydb = mysql.connector.connect(
        host=mysqlParas["host"],
        user=mysqlParas["user"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    gcSql = "SELECT goodsCode FROM allGoodsCode"
    mycursor.execute(gcSql)
    gcs = mycursor.fetchall()  # gcs is a list of tuples

    for gct in gcs:
        goodsCode = gct[0]
        logging.info(f"downloading {goodsCode}'s ")
        preNumSql="SELECT COUNT(*) FROM premiumReview WHERE goodsCode=%s"
        preNumVal=(f"{goodsCode}",)
        mycursor.execute(preNumSql,preNumVal)
        prenumTL=mycursor.fetchall()
        prenum=prenumTL[0][0]
        if isDebug:
            logging.info(f"preNUM={prenum}")

        comNumSql = "SELECT COUNT(*) FROM commonReview WHERE goodsCode=%s"
        comNumVal = (f"{goodsCode}",)
        mycursor.execute(comNumSql, comNumVal)
        comnumTL = mycursor.fetchall()
        comnum = comnumTL[0][0]
        if isDebug:
            logging.info(f"comNUM={comnum}")
        
        try:
            downloadItemReviews(goodsCode=goodsCode, needCommon=True, needPremium=True,alreadyPre=prenum,
                                alreadyCom=comnum,hmCRp=shallowCRp,hmPRp=shallowPRp)
        except:
            logging.error("error:")
            continue
        logging.info("ok")
        
    mydb.close()