import requests
import utils.gParas
from utils.MyException import NoRespondException
import logging
import time


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get?type=http").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getHtml(url):
    retry_count = utils.gParas.retry_times
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)},headers=utils.gParas.headers,timeout=5)
            if html is None:
                raise NoRespondException
            else:
                return html
        except:
            retry_count -= 1
            delete_proxy(proxy)
            proxy = get_proxy().get("proxy")
    if retry_count==0:
        logging.warning("no proxy valid")
    return requests.get(url)


def postHtml(url, data, headers=None):
    retry_count = utils.gParas.retry_times
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.post(url=url, data=data, headers=headers, proxies={"http": "http://{}".format(proxy),"https": "https://{}".format(proxy)},
            timeout=5)
            if html is None:
                raise NoRespondException
            else:
                return html
        except:
            retry_count -= 1
            delete_proxy(proxy)
            proxy = get_proxy().get("proxy")
    if retry_count==0:
        logging.warning("no proxy valid")
    return requests.post(url=url, data=data, headers=headers)


# def getHtml(url):
#     return requests.get(url, headers=utils.gParas.headers, timeout=5)
#
#
# def postHtml(url, data, headers=None):
#     return requests.post(url=url, data=data, headers=headers, timeout=5)
