import json
import re
import utils.gParas
from bs4 import BeautifulSoup
import requests
import json
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="temp"
    )

mycursor = mydb.cursor()
gccursor=mydb.cursor()
limitsql=f" limit {utils.gParas.updateItemNumOnceOfInfo}" if utils.gParas.updateItemNumOnceOfInfo!=0 else ""
querySql="select val from fetchone order by id desc "+limitsql

gccursor.execute(querySql)
val=gccursor.fetchone()     # tuple
while(val):
    print(val[0])
    mycursor.execute("select * from pk_test limit 1")
    pk=mycursor.fetchone()
    print(pk[0])
    val = gccursor.fetchone()


