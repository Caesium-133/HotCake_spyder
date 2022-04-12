import requests
import utils.gParas
from utils.MyException import NoRespondException
import logging
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def get_proxy():
    return requests.get("http://127.0.0.1:5010/get?type=http").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# def getHtml(url):
#     retry_count = utils.gParas.retry_times
#     proxy = get_proxy().get("proxy")
#     while retry_count > 0:
#         try:
#             html = requests.get(url, proxies={"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)},headers=utils.gParas.headers,timeout=5)
#             if html is None:
#                 raise NoRespondException
#             else:
#                 return html
#         except:
#             retry_count -= 1
#             delete_proxy(proxy)
#             proxy = get_proxy().get("proxy")
#     if retry_count==0:
#         logging.warning("no proxy valid")
#     return requests.get(url)


# def postHtml(url, data, headers=None):
#     retry_count = utils.gParas.retry_times
#     proxy = get_proxy().get("proxy")
#     while retry_count > 0:
#         try:
#             html = requests.post(url=url, data=data, headers=headers, proxies={"http": "http://{}".format(proxy),"https": "https://{}".format(proxy)},
#             timeout=5)
#             if html is None:
#                 raise NoRespondException
#             else:
#                 return html
#         except:
#             retry_count -= 1
#             delete_proxy(proxy)
#             proxy = get_proxy().get("proxy")
#     if retry_count==0:
#         logging.warning("no proxy valid")
#     return requests.post(url=url, data=data, headers=headers)

def checkHtml(webdata:str):
    index=webdata.find("document.location.replace")
    if index>-1:
        return utils.gParas.isNoItem
    return webdata

def getHtml(url):
    time.sleep(utils.gParas.wait_time)
    webdata = requests.get(url=url,headers=utils.gParas.headers, timeout=utils.gParas.outtime)
    redirectUrl = re.findall(r"document.location.replace\(\".*?\"\);", webdata.text)
    if redirectUrl:
        url=redirectUrl[0].split("\"")[1]
        istour=url.find("gtour")
        if istour>-1:
            return utils.gParas.isTour
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        wait.until(
            EC.presence_of_all_elements_located((By.ID, "header"))
        )
        data = driver.page_source
        return checkHtml(data)
    return checkHtml(webdata.text) if webdata else None


def postHtml(url, data, headers=None):
    time.sleep(utils.gParas.wait_time)
    webdata = requests.post(url=url,data=data, headers=headers, timeout=utils.gParas.outtime)
    redirectUrl = re.findall(r"document.location.replace\(\".*?\"\);", webdata.text)
    if redirectUrl:
        url = redirectUrl[0].split("\"")[1]
    istour = url.find("gtour")
    if istour > -1:
        return utils.gParas.isTour
    webdata = requests.post(url=url, data=data, headers=headers, timeout=utils.gParas.outtime)
    return checkHtml(webdata.text) if webdata else None
