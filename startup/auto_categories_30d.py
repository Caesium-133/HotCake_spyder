######## update 30 days ########
# -*- coding: utf-8 -*-
import logging
import time
import sys
sys.path.append("../")
from utils.utility import makeDir
from crawler.getCategories import getAllCategories

if __name__ == "__main__":
    makeDir("./log/cat")
    date = time.strftime("%Y-%m-%d", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=f"./log/cat/logging.log", format=LOG_FORMAT, level=logging.INFO)

    logging.info("updating all cats")
    
    getAllCategories()
        
