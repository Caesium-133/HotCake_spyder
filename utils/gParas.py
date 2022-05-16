import random

wait_time = random.uniform(0.3,1)
wait_time_update = 0.5

retry_times = 5

use_proxy=False

isDebug = False

isMultithreading= False

max_page=20 #naver 新闻爬取页数

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    "Accept": "*/*",
    "Connection":"close"
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

mysqlParas = {
    "host": "",
    "user": "",
    "passwd": "",
    "port": ""
}

itemUrl = "http://item.gmarket.co.kr/Item?goodsCode="

influxParas = {
    "host": "",
    "user": "",
    "password": ""
}

shallowCRp = 500  # 一次取某商品一般评论数 10000
shallowPRp = 1000  # 一次取某商品高级评论数 10000

updateItemNumOnceOfInfo = 0  # 一次更新多少个商品的信息
updateItemNumOnceOfReviews = 0  # 一次更新多少个商品的评论

PremiumReviewsPP=5
CommonReviewsPP=10

outtime = 24
