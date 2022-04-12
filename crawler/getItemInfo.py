import re
import time
from bs4 import BeautifulSoup
import requests
import logging
from utils.MyException import NoRespondException, RetryMayWorkException, WeNeedCheckException, UnWantedGSException
from utils.utility import getItemInfoString
import json
from utils.gParas import wait_time, itemUrl, wait_time_update, isDebug, isTour, isNoItem
from crawler.getItemReviews import downloadItemReviews
from utils.manProxy import getHtml, postHtml
from utils.MyDecoration import debug
from retry import retry


debugMethod = "time"


@debug(isDebug=isDebug, method=debugMethod)
def getItemSummary(goodsCode, itemInfoSDict):
    itemInfo = itemInfoSDict
    logging.info(f"getting {goodsCode}'s info")
    url = itemUrl + f"{goodsCode}"
    itemInfo["goodsCode"] = goodsCode

    webData = getHtml(url)
    if webData == isTour or webData == isNoItem:
        raise UnWantedGSException
    if webData is None:
        logging.error(f"no info respond for {goodsCode}")
        raise NoRespondException("InfoPage")
    soup = BeautifulSoup(webData, 'lxml')

    realPrice = soup.select_one("strong.price_real")
    if realPrice:
        rpNum = re.findall("\d+", realPrice.get_text().replace(",", ""))
        itemInfo["price"] = int(rpNum[0]) if len(rpNum) else None

    if itemInfo["price"] is None:
        itemInfo["isSoldOut"] = True
    else:
        itemInfo["isSoldOut"] = False

    try:
        cp = soup.select_one("div.box__coupon-wrap")
        coupon = cp.select_one("span.text__emphasis")
        coupon = coupon.get_text().split("%")[0]
    except:
        coupon = 0

    p_coupon = None
    try:
        p_coupon = float(float(coupon) / 100)
    except:
        n_coupon = coupon.split("원")[0].replace(",", "")
        try:
            p_coupon = float(float(n_coupon) / float(itemInfo["price"])) if itemInfo["price"] else float(
                n_coupon)
        except:
            wan = n_coupon.find("만")
            if wan > -1:
                p_coupon = float(n_coupon.split("만")[0]) * 10000
                p_coupon = float(p_coupon / float(itemInfo["price"])) if itemInfo["price"] else float(p_coupon)
            else:
                logging.warning(f"{goodsCode}'s coupon not the format")
    finally:
        itemInfo["coupon"] = p_coupon

    try:
        reviewInfo = downloadItemReviews(goodsCode=goodsCode, needCommon=False, needPremium=False)
        itemInfo["reviewsNum"] = reviewInfo["totalCount"]
        itemInfo["premiumReviewsNum"] = reviewInfo["premiumReviewNum"]
        itemInfo["commonReviewsNum"] = reviewInfo["commonReviewNum"]
    except:
        logging.warning(f"unfulfilled item summary of {goodsCode}")


@debug(isDebug=isDebug, method=debugMethod)
@retry(exceptions=(NoRespondException, RetryMayWorkException), tries=3, delay=2, jitter=(3, 4))
def getItemInfo(goodsCode, itemInfo):
    time.sleep(wait_time / 2)
    logging.info(f"getting {goodsCode}'s info")
    url = itemUrl + f"{goodsCode}"

    itemInfo["goodsCode"] = goodsCode
    itemInfo["updateDate"] = time.strftime("%Y-%m-%d", time.localtime())

    webData = getHtml(url)
    if webData == isTour or webData == isNoItem:
        raise UnWantedGSException
    if webData is None:
        logging.error(f"no info respond for {goodsCode}")
        raise NoRespondException("InfoPage")
    soup = BeautifulSoup(webData, 'lxml')

    title = soup.select_one("div.box__item-title")
    itemInfo["title"] = title.h1.text.replace(",", " ") if title else None

    navi = soup.find("div", class_="location-navi")
    if navi is None:
        logging.error(f"no navi bar for {goodsCode}")
        raise WeNeedCheckException("noNaviBar")
    cats = navi.select("li")
    i = 0
    for cat in cats:
        catName = cat.find("a")
        itemInfo[f"cat_{i}"] = catName.text.replace(",", "/") if catName else None
        if catName and i > 1:
            catLink = catName.get("href")
            catCode = catLink.split("=")[-1]
            itemInfo[f"cat_{i}_code"] = catCode
        i += 1

    isBest = True if soup.select_one("span.box__category-best") else False
    itemInfo["isBest"] = isBest

    isOfficial = True if soup.select_one("span.text__official") else False
    itemInfo["isOfficial"] = isOfficial

    realPrice = soup.select_one("strong.price_real")
    if realPrice:
        rpNum = re.findall("\d+", realPrice.get_text().replace(",", ""))
        itemInfo["realPrice"] = int(rpNum[0]) if len(rpNum) else None

    if itemInfo["realPrice"] is None:
        itemInfo["isSoldOut"] = True
    else:
        itemInfo["isSoldOut"] = False

    originalPrice = soup.select_one("span.price_original")
    if originalPrice:
        opNum = re.findall("\d+", originalPrice.get_text().replace(",", ""))
        itemInfo["originalPrice"] = int(opNum[0])
    else:
        itemInfo["originalPrice"] = itemInfo["realPrice"]

    try:
        cp = soup.select_one("div.box__coupon-wrap")
        coupon = cp.select_one("span.text__emphasis")
        coupon = coupon.get_text().split("%")[0]
    except:
        coupon = 0

    p_coupon = None
    try:
        p_coupon = float(float(coupon) / 100)
    except:
        n_coupon = coupon.split("원")[0].replace(",", "")
        try:
            p_coupon = float(float(n_coupon) / float(itemInfo["realPrice"])) if itemInfo["realPrice"] else float(
                n_coupon)
        except:
            wan = n_coupon.find("만")
            if wan > -1:
                p_coupon = float(n_coupon.split("만")[0]) * 10000
                p_coupon = float(p_coupon / float(itemInfo["realPrice"])) if itemInfo["realPrice"] else float(p_coupon)
            else:
                float(n_coupon)  # TODO shandiao
    finally:
        itemInfo["coupon"] = p_coupon

    getShopInfoJS = soup.select_one("div.vip-tabcontentwrap > script")
    getShopInfoJS = getShopInfoJS.text
    getSIpayload = re.findall("{.*}", getShopInfoJS)[0]
    getSIpayload = json.loads(getSIpayload)
    sib = postHtml(url="http://item.gmarket.co.kr/Shop/ShopInfo", data=getSIpayload)
    # sib = requests.post(url="http://item.gmarket.co.kr/Shop/ShopInfo", data=getSIpayload)
    # with open("test.html","w",encoding="utf-8") as file:
    #     file.write(sib.text)
    if sib == isTour or sib == isNoItem:
        raise UnWantedGSException
    sibSoup = BeautifulSoup(sib, 'lxml')

    shopInfoBox = sibSoup.select_one("div.shop-infobox")
    if shopInfoBox is None:
        logging.warning(f"no response for {goodsCode}'s shop info box")
        itemInfo["shopTitle"] = None
        itemInfo["isPowerDealer"] = False
        itemInfo["isInterestShop"] = False
    else:
        shopTitle = shopInfoBox.strong.a
        itemInfo["shopTitle"] = shopTitle.get_text() if shopTitle else None
        sellerAwards = shopInfoBox.select_one("p.seller-awards")
        if sellerAwards is None:
            itemInfo["isPowerDealer"] = False
            itemInfo["isInterestShop"] = False
        else:
            isPD = sellerAwards.find("span", class_="power-dealer")
            itemInfo["isPowerDealer"] = True if isPD else False
            isIS = sellerAwards.find("span", href="#tooltip_bestseller")
            itemInfo["isInterestShop"] = True if isIS else False

    productInfoBox = soup.select_one("div.box__product-notice-list")
    if productInfoBox is None:
        logging.warning(f"no response for {goodsCode}'s product infobox")
        raise NoRespondException("ProductInfoBox")
    lists = productInfoBox.select("table.table_productinfo")
    for li in lists:
        trs = li.find_all("tr")
        for tr in trs:
            if tr.th:
                rowText = tr.th.get_text()
                if tr.td:
                    if rowText == "상품상태":
                        itemInfo["productStatus"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "사업자구분":
                        itemInfo["businessClassification"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "브랜드":
                        itemInfo["brand"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "원산지":
                        itemInfo["source"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "품명 및 모델명":
                        itemInfo["productAndModelName"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "크기/중량":
                        if tr.td.get_text():
                            s = tr.td.get_text()
                            slash = tr.td.get_text().find("/")
                            if slash != -1 and slash < len(tr.td.get_text()):
                                if s.find("m") < slash < s.find("g"):
                                    itemInfo["size"] = tr.td.get_text().split("/")[0].strip(" ")
                                    itemInfo["weight"] = tr.td.get_text().split("/")[1].strip(" ")
                    elif rowText == "색상":
                        itemInfo["colour"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "재질" or rowText == "제품소재":
                        itemInfo["material"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "제조자/수입자":
                        itemInfo["ManufacturerNImporter"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "제조국":
                        itemInfo["countryOfManufacture"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "도서명":
                        itemInfo["bookName"] = getItemInfoString(tr.td.get_text())
                    elif rowText == "저자/출판사":
                        itemInfo["author"] = tr.td.get_text().split("/")[0]
                        if len(tr.td.get_text().split("/")) > 1:
                            itemInfo["publisher"] = tr.td.get_text().split("/")[-1]
