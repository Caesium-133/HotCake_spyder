######## update 1 day ########
# -*- coding: utf-8 -*-
import datetime
import logging
import time
import sys
sys.path.append("../")
from utils.utility import makeDir
from crawler.getNaverNews import getSummaries
from utils.gParas import max_page

if __name__ == "__main__":
    makeDir("./log/naver")
    date = time.strftime("%Y%m%d", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/naver/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

    logging.info("downloading naver news")
    cats = {
        "100": "정치",  # 政治
        "101": "경제",  # 经济
        "102": "사회",  # 社会
        "103": "생활/문화",  # 生活/文化
        "105": "IT/과학",  # IT/科学
        "104": "세계"  # 世界
    }

    try:
        for cat in cats.keys():
            yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
            getSummaries(category=cat,max_page=max_page,date=yesterday)
    except Exception as e:
        logging.error(e)
