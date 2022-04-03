# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
from time import sleep
import sys
sys.path.append("../")

from util.webRequest import WebRequest
import requests


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        米扑代理 https://proxy.mimvp.com/
        :return:
        """
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
        ]
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html_tree = WebRequest().get(url).tree
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        :return:
        """
        url = "http://www.66ip.cn/mo.php"

        resp = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
        for proxy in proxies:
            yield proxy

    @staticmethod
    def freeProxy03():
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy04():
        """ 蝶鸟IP """
        url = "https://www.dieniao.com/FreeProxy.html"
        tree = WebRequest().get(url, verify=False).tree
        for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
            ip = "".join(li.xpath('./span[1]/text()')).strip()
            port = "".join(li.xpath('./span[2]/text()')).strip()
            yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """ PROXY11 https://proxy11.com """
        url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
        try:
            resp_json = WebRequest().get(url).json
            for each in resp_json.get("data", []):
                yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理 """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10():
        """ 89免费代理 """
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

    @staticmethod
    def freeProxy11():
        """ 爬代理 """
        cookie="Cookie: PHPSESSID=vhjcc0l2gplaoalgdtpe25pj1c; XSRF-TOKEN=eyJpdiI6IkozbSt3YkZIXC9rRmFMN05MelU2VEV3PT0iL" \
               "CJ2YWx1ZSI6InJmTG9yVjRFdVdGa0dkcDh2M1wvK0x3cXpBdm05eDB2UEtIQ0xxOXdWQ2hpSlRZMnVTTFwvZW1pSXpFUjBkWFl1RiIs" \
               "Im1hYyI6ImMxMTRkZGRjZmRhOTc5OGEyMWJkYTE3ODgxNDg4ZmFkOGVmN2M0YzY3N2Q0ZTc3OWY1MTlhZGQ2ZWRkN2E1MTkifQ%3D%3" \
               "D; laravel_session=eyJpdiI6InlZUXRhazY2NDJGWER1NnczMnoyMXc9PSIsInZhbHVlIjoiZ3pCQlRsZlJSbEtLXC80WVZUOGZy" \
               "SFwvM1wvZnB1UGpLQkJxUFwvUlN3aUdCSVVKVXg3aDVPRkxZNjhxSmVNb1F1Z1ciLCJtYWMiOiI4ODE0NWE4NjU2NjU1ZjBkMjk3MGI" \
               "xYTczM2YwMTc0NmM0MGNkMWU3ZTIwNjJjNzJkOGNkZGI0YjhmN2JhMzQ4In0%3D; user=eyJpdiI6InBcL0k5Ujg0M2pjbUg5OHFlW" \
               "UkxUmxRPT0iLCJ2YWx1ZSI6IllOc3d0azlSOVdZRnRKMkpsYTJJd1E9PSIsIm1hYyI6IjAyYTE4MzE2ZjU5MDM4MDM3NmJiYjRhYWI3" \
               "ZWY4MjllNTg2NjBlZTVjYWIxMWRkZDQ1Mzg5ZTQyZWNhYzY4MzcifQ%3D%3D; loginuser=eyJpdiI6ImdiRGJ0QkE5NXB0QUhZZUN" \
               "HTXZYS2c9PSIsInZhbHVlIjoiNUNaaEI2aXQwRzlQaEVuRVc3RkMrQT09IiwibWFjIjoiMTc2NTczNWZlYzIwZDJlMTc5ZTIyYWNkYz" \
               "U4MDI4ODljOThkMWRkNTIxYWU4ZTFjMDk5MDZkNzAxMzczNTQzMSJ9; loginpass=eyJpdiI6Ill5QzVcL3FLM0pBempucEFuY25Eb" \
               "G1nPT0iLCJ2YWx1ZSI6Im0zZGZCK2FEQUVwWDM0UnVydmpuMWc9PSIsIm1hYyI6IjgyNzI3MzZkM2ZkNzdjMGI3YzBkMGM5NjJlNTM4" \
               "ZDUzZjg3YmU1YWZiZmNhYjdlYzZiMjg4ZjAxMDc5NjBiMTIifQ%3D%3D; qq=eyJpdiI6IlcyWnRRR0c5TVFsOVhhTEZRMW5DTEE9P" \
               "SIsInZhbHVlIjoiZWdxRDBFXC9CdVdpUWJLZ1VFV2c5Q0E9PSIsIm1hYyI6IjM1NzEwYzFlY2Q0MmVkNWQwNDU1YzQ0NzBhNjgwZDdh" \
               "OGQ0ZDU1ZmFmZTI2Yjg1ZWZmYTIzOGI2NGQzOGM3MTYifQ%3D%3D; mail=eyJpdiI6IkFWMXBTTnUyR3J4MkpBSmRTN3B6OHc9PSIs" \
               "InZhbHVlIjoiWnRydTVycnU4NFRvcTRcL2NEZTQ4ZlwvSnhjc2p2UlRndHE3RFpkdDNRaGNvPSIsIm1hYyI6IjVkOGMxZTA0MDNiZmJm" \
               "OTQ2MWI4NmFiYzdhMmM0ODY1ZTRiYmU4NzQxZmYxY2Q5MjI2NDU0ZDhlODQzNmNkZWUifQ%3D%3D; sid=eyJpdiI6InRMTTg3OHQ4Qz" \
               "VUOVljeHkybjlEaVE9PSIsInZhbHVlIjoiWXV6WDc2Q0gyYlwvR0xNVWtmRXpQVEx6TG02TlU0VXYxUTVCNWd3dE1EYWJoaTdWMnVHY0" \
               "N4TDUxSVYwd245eUkiLCJtYWMiOiIzMDRhYTVhYjg4MDllMTU5NTVjNGM3NDJjZjBiNTAxZmUwMWRiNDIxMmNkZWE2NjUxYzVkMWIzYz" \
               "hkYWFlMWE4In0%3D"
        header={'User-Agent': "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cookie':cookie}
        APIkey="zY9GDr3ZYWyBCaitLHzeWNCFF1paO0j1"
        fetchNum=1000
        apiUrl=f"https://www.padaili.com/proxyapi?api={APIkey}&num={fetchNum}&type=3&order=jiance"
        apiData = requests.get(apiUrl, headers=header)
        proxies = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", apiData.text)
        for proxy in proxies:
            yield proxy
        # for proxy in proxies:
        #     yield ':'.join(proxy)

    # @staticmethod
    # def wallProxy01():
    #     """
    #     PzzQz https://pzzqz.com/
    #     """
    #     from requests import Session
    #     from lxml import etree
    #     session = Session()
    #     try:
    #         index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
    #         x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
    #         if x_csrf_token:
    #             data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
    #             proxy_resp = session.post("https://pzzqz.com/", verify=False,
    #                                       headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
    #             tree = etree.HTML(proxy_resp["proxy_html"])
    #             for tr in tree.xpath("//tr"):
    #                 ip = "".join(tr.xpath("./td[1]/text()"))
    #                 port = "".join(tr.xpath("./td[2]/text()"))
    #                 yield "%s:%s" % (ip, port)
    #     except Exception as e:
    #         print(e)

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy11():
        print(_)

# http://nntime.com/proxy-list-01.htm
