"""
    UNUSED
"""
# -*- coding: utf-8 -*-
import csv
from bs4 import BeautifulSoup
import requests
import time


# start=399814051,end=399815060

def getGoodsCode(start=1000000000, end=9999999999):
    now = start
    while (now < end):
        yield now
        now += 1


def findAvailableGoodCodes(start, end):
    g = getGoodsCode(start=start, end=end)

    while (True):
        try:
            goodsCode = next(g)
            goodsUrl = f'http://global.gmarket.co.kr/item?goodscode={goodsCode}'
            time.sleep(1)
            goodsWebData = requests.get(goodsUrl)
            soup = BeautifulSoup(goodsWebData.text, 'lxml')
            if soup.find("div") is not None:
                print(goodsCode)
        except:
            break

    print("end")


'''
399814075
399814287
399814698
399814976
399815051
'''
