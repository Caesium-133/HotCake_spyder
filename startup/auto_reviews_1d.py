######## run every day ########
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import logging
import time
from utils.utility import makeDir
from crawler.getItemReviews import downloadItemReviews
import mysql.connector
from utils.gParas import mysqlParas, shallowCRp,shallowPRp,updateItemNumOnceOfReviews
from utils.MyException import UnWantedGSException
from tqdm import tqdm


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
    interuptGC = "417899299"
    limitsql = f" limit {updateItemNumOnceOfReviews}" if updateItemNumOnceOfReviews != 0 else ""
    startSql = f" where id <= (select id from allGoodsCode where goodsCode = {interuptGC} limit 1) " if interuptGC else ""
    orderBySql = " ORDER BY id desc "
    querySql = "SELECT DISTINCT goodsCode FROM allGoodsCode" + startSql + orderBySql + limitsql
    mycursor.execute(querySql)
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
            pass
        
        try:
            print(goodsCode)
            downloadItemReviews(goodsCode=goodsCode, needCommon=True, needPremium=True,alreadyPre=prenum,
                                alreadyCom=comnum,hmCRp=shallowCRp,hmPRp=shallowPRp)
        except UnWantedGSException:
            logging.info(f"{goodsCode} is unwanted")
            mycursor.execute("delete from allGoodsCode where goodsCode=%s", (goodsCode,))
            mydb.commit()
            continue
        except Exception as e:
            print(f"{goodsCode} meets error:\n")
            raise e

        logging.info("ok")
        
    mydb.close()