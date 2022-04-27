######## run every hour#########
# -*- coding: utf-8 -*
import sys
sys.path.append("../")
import logging
import time
from utils.utility import makeDir
from crawler.getBestSellers import getBestSellersByAll
from utils.MyDecoration import debug
from utils.gParas import isDebug
from utils.MyException import UnWantedGSException


if __name__ == "__main__":
    makeDir("./log/bs")
    date = time.strftime("%Y-%m-%d@%H:%M:%S", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    #logging.basicConfig(filename=f"./log/bs/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)
    logging.basicConfig(filename=f"./log/bs/logging.log", format=LOG_FORMAT, level=logging.INFO)

    # try:
    #     getBestSellersByAll()
    # except Exception as e:
    #     logging.error("error: ")
    #     raise e
    try:
        getBestSellersByAll()
    except UnWantedGSException:
        pass



