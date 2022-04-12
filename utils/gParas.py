wait_time = 1
wait_time_update = 0.5

retry_times = 5

isDebug = False

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    "Accept": "*/*",
    #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

mysqlParas = {
    "host": "8.142.74.245",
    "user": "root",
    "passwd": "123456"
}

itemUrl = "http://item.gmarket.co.kr/Item?goodsCode="

influxParas = {
    "host": "8.142.74.245",
    "user": "root",
    "password": "123456"
}

shallowCRp = 1200  # 一次取某商品一般评论数
shallowPRp = 1200  # 一次取某商品高级评论数

updateItemNumOnceOfInfo = 0  # 一次更新多少个商品的信息
updateItemNumOnceOfReviews = 0  # 一次更新多少个商品的评论

isTour="this is a tourism product"
isNoItem="this is a blank page"

outtime=24
