######## run every 6 hours #########
# -*- coding: utf-8 -*
import sys
sys.path.append("../")
import logging
import time
from utils.utility import makeDir
from crawler.getBestSellers import getBestSellersByEachCat
from utils.MyDecoration import debug
from utils.gParas import isDebug
from utils.MyException import UnWantedGSException

if __name__ == "__main__":
    makeDir("./log/bs")
    date = time.strftime("%Y-%m-%d@%H:%M:%S", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/bs/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)

    # try:
    #     getBestSellersByEachCat()
    # except:
    #     logging.error("error")
    try:
        getBestSellersByEachCat()
    except UnWantedGSException:
        pass

        
        
        
        