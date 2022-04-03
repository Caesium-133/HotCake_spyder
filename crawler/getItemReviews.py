import sys
sys.path.append("../")
from bs4 import BeautifulSoup
import time
from utils.utility import getReviewGrade
import logging
from utils.MyException import *
from retry import retry
from utils.itemsDict import itemReviewInfo, premiumReview, commonReview
import threading
import mysql.connector
import utils.gParas
from utils.manProxy import getHtml, postHtml
from utils.MyDecoration import debug

page_interval = 1

debugMethod="time"


@retry(exceptions=(NoRespondException, RetryMayWorkException), tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=utils.gParas.isDebug,method=debugMethod)
def downloadItemReviews(goodsCode, needPremium=True, needCommon=True, alreadyPre=0, alreadyCom=0, hmCRp=-1,
                        hmPRp=-1):
    logging.info(f"downloading {goodsCode}'s reviews")

    itemReviews = itemReviewInfo.copy()
    itemReviews["goodsCode"] = goodsCode

    getReviewsPayload = {"goodsCode": f"{goodsCode}"}

    reviewRespond = postHtml(url="http://item.gmarket.co.kr/Review", data=getReviewsPayload, headers=utils.gParas.headers)
    # reviewRespond = requests.post(url="http://item.gmarket.co.kr/Review", data=getReviewsPayload,headers=gParas.headers)
    if reviewRespond is None:
        logging.error(f"no review respond for {goodsCode}")
        raise NoRespondException("reviewRespond")

    soup = BeautifulSoup(reviewRespond.text, 'lxml')

    totalCount = soup.find_all("script", type="text/javascript")
    totalCount = int(totalCount[-1].text.split("=")[-1].replace(" ", "").replace(";", "")) if totalCount else 0
    itemReviews["totalCount"] = totalCount

    if totalCount == 0:
        logging.warning(f"{goodsCode} has no reviews")
        return

    reviewNums = soup.find_all("span", class_="num")
    try:
        premiumReview = reviewNums[0]
        commonReview = reviewNums[1]
    except:
        logging.error(f"{goodsCode} has only one kind of review")
        raise UnableToDealException("no distinction between reviews")

    premiumReviewNum = int(premiumReview.text.replace(",", "")) if premiumReview else 0
    commonReviewNum = int(commonReview.text.replace(",", "")) if commonReview else 0
    itemReviews["premiumReviewNum"] = premiumReviewNum
    itemReviews["commonReviewNum"] = commonReviewNum

    ps = soup.find_all("p", class_="comment-tit")
    if ps is None:
        logging.error(f"found no premium review per page for {goodsCode}")
        raise RetryMayWorkException("noPReviewPerPage")
    tds = soup.find_all("td", class_="comment-grade")
    if tds is None:
        logging.error(f"found no common review per page for {goodsCode}")
        raise RetryMayWorkException("noCReviewPerPage")

    PremiumReviewsPerPage = len(ps)
    CommonReviewsPerPage = len(tds)

    if needPremium:
        try:
            pt = threading.Thread(target=downloadPremiumReview, args=(
                goodsCode, premiumReviewNum, PremiumReviewsPerPage, int(premiumReviewNum - alreadyPre) + 1, hmPRp))
            # downloadPremiumReview(goodsCode=goodsCode, totalNum=premiumReviewNum, numPerPage=PremiumReviewsPerPage,update=int(premiumReviewNum-alreadyPre)+1)
            pt.start()
        except UnableToDealException:
            logging.warning(f"unable to deal something when downloading {goodsCode}'s premium reviews")
        except NoRespondException:
            raise UnableToDealException("NoRespond4PremiumReviews")
        except IOError:
            raise WeNeedCheckException("writePremiumReviews")
        except threading.ThreadError:
            raise WeNeedCheckException("thread error")
        except:
            print("error")
    if needCommon:
        try:
            ct = threading.Thread(target=downloadCommonReviews, args=(
                goodsCode, commonReviewNum, CommonReviewsPerPage, int(commonReviewNum - alreadyCom) + 1, hmCRp))
            # downloadCommonReviews(goodsCode=goodsCode,totalNum=commonReviewNum,numPerPage=CommonReviewsPerPage,update=int(commonReviewNum-alreadyCom)+1)
            ct.start()
        except UnableToDealException:
            logging.warning(f"unable to deal something when downloading {goodsCode}'s common reviews")
        except NoRespondException:
            raise UnableToDealException("NoRespond4CommonReviews")
        except IOError:
            raise WeNeedCheckException("writeCommonReviews")
        except threading.ThreadError:
            raise WeNeedCheckException("thread error")

    return itemReviews


@retry(exceptions=NoRespondException, tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=utils.gParas.isDebug,method=debugMethod)
def downloadPremiumReview(goodsCode, totalNum, numPerPage, update, hmPRp):
    global page_interval
    logging.info(f"downloading {goodsCode}'s premium reviews")
    if totalNum == 0:
        logging.info("no reviews, return")
        return
    totalPage = int(totalNum / numPerPage) + 1
    if hmPRp == -1:
        hmPRp = totalPage

    # TODO 有数据库操纵语言
    mydb = mysql.connector.connect(
        host=utils.gParas.mysqlParas["host"],
        user=utils.gParas.mysqlParas["user"],
        passwd=utils.gParas.mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO preniumReview VALUES (%s,%s,%s,%s,%s,%s,%s)"

    # headers = ['reviewTitle', 'reviewGoodsChoice', 'reviewContent', 'reviewerName', 'reviewDate', 'reviewerExp']

    # if update == 0:
    #     with open(f"./reviews/{goodsCode}_premium.csv", "w", newline='', encoding='utf-8') as file:
    #         if file is None:
    #             logging.critical("unable to open or write into review file")
    #         writer = csv.DictWriter(file, fieldnames=headers)
    #         writer.writeheader()

    page = 1
    premiumPage = postHtml(url="http://item.gmarket.co.kr/Review", data={"goodsCode": f"{goodsCode}"},
                           headers=utils.gParas.headers)

    if premiumPage is None:
        logging.error(f"no respond for {goodsCode}'s premium page")
        raise NoRespondException("premiumPage")

    numThisTime = 0

    while premiumPage:
        soup = BeautifulSoup(premiumPage.text, 'lxml')
        reviewsDictList = []
        ReviewTable = soup.find("table", class_="tb_premium")

        if ReviewTable is None:
            logging.error(f"no review table for {goodsCode}‘s premium review")
            raise NoRespondException("PremiumReviewTable")

        reviews = ReviewTable.select("tr")
        for review in reviews:
            reviewDict = premiumReview.copy()
            reviewDetails = review.find("td", class_="comment-content")
            reviewDict["goodsCode"] = goodsCode
            reviewDict["reviewTitle"] = reviewDetails.find("p", class_="comment-tit").text.replace(",", " ")
            reviewDict["reviewGoodsChoice"] = reviewDetails.find("p", class_="pd-tit").text.replace(",", " ")
            reviewDict["reviewContent"] = reviewDetails.find("p", class_="con").text.replace(",", " ").replace("\n",
                                                                                                               " ")
            writerInfo = review.find("dl", class_="writer-info")

            reviewerName = writerInfo.select_one("dd:nth-child(2)")
            reviewDict["reviewerName"] = reviewerName.text if reviewerName else None
            reviewDate = writerInfo.select_one("dd:nth-child(4)")
            reviewDict["reviewDate"] = reviewDate.text if reviewDate else None
            reviewerExp = writerInfo.select_one("dd:nth-child(6)")
            reviewDict["reviewerExp"] = reviewerExp.text if reviewerExp else None
            reviewsDictList.append(tuple(reviewDict.values()))

            numThisTime += len(reviewsDictList)

        val = reviewsDictList
        try:
            mycursor.execute(sql, val)
        except:
            mydb.rollback()
            logging.info("mysql error")
        mydb.commit()

        # with open(f"./reviews/{goodsCode}_premium.csv", "a", newline='', encoding='utf-8') as file:
        #     if file is None:
        #         logging.error("unable to append into review file")
        #     writer = csv.DictWriter(file, fieldnames=gParas.headers)
        #     writer.writerows(reviewsDictList)

        page += page_interval
        nextPagePayload = {
            "goodsCode": f"{goodsCode}",
            "pageNo": f"{page}",
            "sort": "0",
            "totalPage": f"{totalPage}"
        }
        time.sleep(utils.gParas.wait_time)
        premiumPage = postHtml(url="http://item.gmarket.co.kr/Review/Premium", data=nextPagePayload,
                               headers=utils.gParas.headers)

        if premiumPage is None and page < totalPage:
            logging.warning(f"get NONE {goodsCode}'s premium page before pages end")

        if numThisTime > update:
            break

        if page > hmPRp:
            break

        if utils.gParas.isDebug:
            if page == 4:
                break
    mydb.close()


@retry(exceptions=NoRespondException, tries=3, delay=2, jitter=(3, 4))
@debug(isDebug=utils.gParas.isDebug,method=debugMethod)
def downloadCommonReviews(goodsCode, totalNum, numPerPage, update, hmCRp):
    global page_interval

    logging.info(f"downloading {goodsCode}'s common reviews")
    if totalNum == 0:
        logging.info("no reviews, return")
        return
    totalPage = int(totalNum / numPerPage) + 1
    if hmCRp == -1:
        hmCRp = totalPage

    headers = ['goodsGrade', 'deliveryGrade', 'reviewGoodsChoice', 'reviewContent', 'reviewerName', 'reviewDate']

    # if update==0:
    #     with open(f"./reviews/{goodsCode}_common.csv", "w", newline='', encoding='utf-8') as file:
    #         if file is None:
    #             logging.error("unable to open or write into review file")
    #         writer = csv.DictWriter(file, fieldnames=headers)
    #         writer.writeheader()

    # TODO 有数据库操纵语言
    mydb = mysql.connector.connect(
        host=utils.gParas.mysqlParas["host"],
        user=utils.gParas.mysqlParas["user"],
        passwd=utils.gParas.mysqlParas["passwd"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO preniumReview VALUES (%s,%s,%s,%s,%s,%s,%s)"

    page = 1
    commonPage = postHtml(url="http://item.gmarket.co.kr/Review", data={"goodsCode": f"{goodsCode}"},
                          headers=utils.gParas.headers)
    if commonPage is None:
        logging.error(f"no respond for {goodsCode}'s common page")
        raise NoRespondException("commonPage")
    numThisTime = 0

    while commonPage:
        soup = BeautifulSoup(commonPage.text, 'lxml')
        reviewsDictList = []
        ReviewTable = soup.find("table", class_="tb_comment_common")

        if ReviewTable is None:
            logging.error(f"no review table for {goodsCode}‘s common review, HALT")
            raise NoRespondException("CommonReviewTable")

        reviews = ReviewTable.select("tr")
        for review in reviews:
            reviewDict = commonReview.copy()
            reviewGrade = review.find("td", class_="comment-grade")

            reviewDict["goodsCode"] = goodsCode
            grades = getReviewGrade(reviewGrade)
            reviewDict["goodsGrade"] = grades["goodsGrade"]
            reviewDict["deliveryGrade"] = grades["deliveryGrade"]

            reviewDetails = review.find("td", class_="comment-content")
            reviewGoodsChoice = reviewDetails.find("p", class_="pd-tit")
            reviewDict["reviewGoodsChoice"] = reviewGoodsChoice.text.replace(",", "").replace("\n", "").replace("\r",
                                                                                                                "").replace(
                "\t", "") if reviewGoodsChoice else None
            reviewContent = reviewDetails.find("p", class_="con")
            reviewDict["reviewContent"] = reviewContent.text.replace(",", "").replace("\n", "").replace("\r",
                                                                                                        "").replace(
                "\t", "") if reviewContent else None

            writerInfo = review.find("dl", class_="writer-info")
            reviewerName = writerInfo.select_one("dd:nth-child(2)")
            reviewDict["reviewerName"] = reviewerName.text.replace(",", "").replace("\n", "") if reviewerName else None
            reviewDate = writerInfo.select_one("dd:nth-child(4)")
            reviewDict["reviewDate"] = reviewDate.text.replace(",", "").replace("\n", "") if reviewDate else None

            reviewsDictList.append(tuple(reviewDict.values()))

            numThisTime += len(reviewsDictList)

        val = reviewsDictList
        try:
            mycursor.execute(sql, val)
        except:
            mydb.rollback()
            logging.info("mysql error")
        mydb.commit()

        # with open(f"./reviews/{goodsCode}_common.csv", "a", newline='', encoding='utf-8') as file:
        #     if file is None:
        #         logging.error("unable to append into review file")
        #     writer = csv.DictWriter(file, fieldnames=headers)
        #     writer.writerows(reviewsDictList)

        page += page_interval
        payload = {"goodsCode": f"{goodsCode}",
                   "pageNo": f"{page}",
                   "totalPage": f"{totalPage}"
                   }
        time.sleep(utils.gParas.wait_time)
        commonPage = postHtml(url="http://item.gmarket.co.kr/Review/Text", data=payload, headers=utils.gParas.headers)

        if commonPage is None and page < totalPage:
            logging.warning(f"get NONE {goodsCode}'s common page before pages end")

        if numThisTime > update:
            break

        if page > hmCRp:
            break

        if utils.gParas.isDebug:
            if page == 4:
                break
    mydb.close()
