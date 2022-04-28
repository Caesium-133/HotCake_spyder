import json
import re
import time
import utils.gParas
from bs4 import BeautifulSoup
import requests
import json
import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utils.manProxy import postHtml,getHtml
import logging
from utils.utility import makeDir
from utils.gParas import isTour,isNoItem
from utils.MyException import UnWantedGSException,UnableToDealException,NoRespondException,WeNeedCheckException
import csv
from utils.itemsDict import itemInfoDict

from utils.utility import getMostRecentlyUpdatedMeasurement
from crawler.getItemReviews import downloadItemReviews

makeDir("./testLog")
date = time.strftime("%Y-%m-%d", time.localtime())
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=f"./testLog/logging{date}.log", format=LOG_FORMAT, level=logging.INFO)


print(len(itemInfoDict.keys()))



#874714969