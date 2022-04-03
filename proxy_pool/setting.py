# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setting.py
   Description :   配置文件
   Author :        JHao
   date：          2019/2/15
-------------------------------------------------
   Change Activity:
                   2019/2/15:
-------------------------------------------------
"""

BANNER = r"""
******************************
**********proxy_pool**********
******************************
"""

VERSION = "2.4.0"

# ############### server config ###############
HOST = "127.0.0.1"

PORT = 5010

# ############### database config ###################
# db connection uri
# example:
#      Redis: redis://:password@ip:port/db
#      Ssdb:  ssdb://:password@ip:port
DB_CONN = 'redis://:123456@127.0.0.1:6379/5'

# proxy table name
TABLE_NAME = 'use_proxy'

# ###### config the proxy fetch function ######
PROXY_FETCHER = [
    "freeProxy01",
    "freeProxy02",
    "freeProxy03",
    "freeProxy04",
    "freeProxy05",
    "freeProxy06",
    "freeProxy07",
    # "freeProxy08",
    "freeProxy09",
    "freeProxy10",
    "freeProxy11"
]

# ############# proxy validator #################
# 代理验证目标网站
#HTTP_URL = "http://httpbin.org"
HTTP_URL = "http://corners.gmarket.co.kr/BestSellers"

HTTPS_URL = "https://www.qq.com"

# 代理验证时超时时间
VERIFY_TIMEOUT = 10

# 近PROXY_CHECK_COUNT次校验中允许的最大失败次数,超过则剔除代理
MAX_FAIL_COUNT = 0

# 近PROXY_CHECK_COUNT次校验中允许的最大失败率,超过则剔除代理
# MAX_FAIL_RATE = 0.1

# proxyCheck时代理数量少于POOL_SIZE_MIN触发抓取
POOL_SIZE_MIN = 20

# ############# scheduler config #################

# Set the timezone for the scheduler forcely (optional)
# If it is running on a VM, and
#   "ValueError: Timezone offset does not match system offset"
#   was raised during scheduling.
# Please uncomment the following line and set a timezone for the scheduler.
# Otherwise it will detect the timezone from the system automatically.

TIMEZONE = "Asia/Shanghai"
