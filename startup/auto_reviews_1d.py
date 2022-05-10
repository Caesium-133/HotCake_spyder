######## run every day ########
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import logging
import time
from utils.utility import makeDir,findNextGC
from crawler.getItemReviews import downloadItemReviews
import mysql.connector
from utils.gParas import mysqlParas, shallowCRp,shallowPRp,updateItemNumOnceOfReviews,PremiumReviewsPP,CommonReviewsPP
from utils.MyException import UnWantedGSException
from tqdm import tqdm
from requests.exceptions import ConnectionError,ReadTimeout
from utils.itemsDict import itemReviewInfo


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
        port=mysqlParas["port"],
        passwd=mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    interuptGC = "776582823"
    #interuptGC = findNextGC("2237043715",mycursor)
    # limitsql = f" limit {updateItemNumOnceOfReviews}" if updateItemNumOnceOfReviews != 0 else ""
    # startSql = f" where id <= (select id from allGoodsCode where goodsCode = {interuptGC} limit 1) " if interuptGC else ""
    # orderBySql = " ORDER BY id asc "
    # querySql = "SELECT DISTINCT goodsCode FROM allGoodsCode" + startSql + orderBySql + limitsql
    querySql=f"SELECT DISTINCT goodsCode FROM allGoodsCode where id>=(SELECT id FROM allGoodsCode WHERE goodsCode={interuptGC})  ORDER BY id"
    mycursor.execute(querySql)
    gcs = mycursor.fetchall()  # gcs is a list of tuples

    pbar=tqdm(total=len(gcs))
    gcn=0
    while(gcn<len(gcs)):
        ret=0
        goodsCode = gcs[gcn][0]
        gcn+=1
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
        reviewsSummary=itemReviewInfo.copy()
        reviewsSummary["hmCRLastTime"]=0
        reviewsSummary["hmPRLastTime"]=0

        if isDebug:
            pass
        try:
            #print(goodsCode)
            reviewsSummary=downloadItemReviews(goodsCode=goodsCode, needCommon=True, needPremium=True,alreadyPre=prenum,
                                alreadyCom=comnum,hmCRp=shallowCRp,hmPRp=shallowPRp)
            pbar.update(1)
        except UnWantedGSException:
            logging.info(f"{goodsCode} is unwanted")
            mycursor.execute("delete from allGoodsCode where goodsCode=%s", (goodsCode,))
            mydb.commit()
            continue
        except (ConnectionError,ReadTimeout):
            logging.warning(f"{goodsCode} reviews connect error")
            if ret==3:
                logging.warning(f"{goodsCode}' reviews connect error, retry meets max")
                continue
            PASS=True
            if reviewsSummary["hmCRLastTime"]<shallowCRp*0.75*CommonReviewsPP + comnum:
                mycursor.execute("DELETE FROM commonreview WHERE goodsCode=%s",(goodsCode,))
                mydb.commit()
                PASS=False
                ret+=1
            if reviewsSummary["hmPRLastTime"]<shallowPRp*0.75*PremiumReviewsPP + prenum:
                mycursor.execute("DELETE FROM premiumreview WHERE goodsCode=%s",(goodsCode,))
                mydb.commit()
                PASS=False
                ret+=1
            if not PASS:
                gcn-=1
            continue
        except mysql.connector.errors.OperationalError:
            logging.error("lost connection")
            continue
        except Exception as e:
            print(f"{goodsCode} meets error:\n")
            raise e

        logging.info("ok")
    pbar.close()
    mydb.close()
