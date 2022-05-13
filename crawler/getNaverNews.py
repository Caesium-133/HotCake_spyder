import requests
from bs4 import BeautifulSoup
from typing import List
import time
import mysql.connector
import utils.gParas

'''

100 정치 政治
101 경제 经济
102 사회 社会
103 생활/문화 生活/文化
105 IT/과학 IT/科学
104 세계 世界

'''

cats={
"100":"정치", #政治
"101":"경제",  #经济
"102":"사회",  #社会
"103":"생활/문화", #生活/文化
"105":"IT/과학", #IT/科学
"104":"세계" #世界
}

class News:
    def __init__(self):
        self.category=''
        self.press=''
        self.date=''
        self.title=''
        self.content=''
        self.url=''


def getSummaries(category,max_page,date) -> List[News]:
    newsList=[]
    for page in range(max_page):
        time.sleep(utils.gParas.wait_time)
        webData=requests.get(url=f"https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1={category}&page={page}&date={date}",timeout=5,headers=utils.gParas.headers)
        soup=BeautifulSoup(webData.text,'lxml')
        mainContent=soup.find("div",id="main_content")
        if mainContent:
            contents=mainContent.findAll("li")
            for content in contents:
                news=News()
                dts=content.findAll("dt")
                if dts:
                    dt=dts[-1]
                    if dt:
                        url=dt.a["href"]
                        news.url=url
                        news.title=dt.get_text()
                dd=content.find("dd")
                if dd:
                    summary=dd.find("span",class_="lede")
                    if summary:
                        news.content=summary.get_text()
                    writing=dd.find("span",class_="writing")
                    if writing:
                        news.press=writing.get_text()
                news.date=date
                news.category=cats[str(category)]
                newsList.append(news)
    return newsList

def put(nl):
    # headers=["category","press","date","title","content","url"]
    mydb = mysql.connector.connect(
        host=utils.gParas.mysqlParas["host"],
        user=utils.gParas.mysqlParas["user"],
        port=utils.gParas.mysqlParas["port"],
        passwd=utils.gParas.mysqlParas["password"],
        database="spyder"
    )
    mycursor = mydb.cursor()
    SQL = "INSERT INTO navernews values(%s,%s,%s,%s,%s,%s)"
    for n in nl:
        val=(n.category,n.press,n.date,n.title,n.content,n.url)
        mycursor.execute(SQL,val)

    mydb.commit()
    mydb.close()


if __name__=='__main__':
    nl=getSummaries(category=103,max_page=10,date=20220401)
    put(nl)





