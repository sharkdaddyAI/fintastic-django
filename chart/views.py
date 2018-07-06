from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, JsonResponse
import numpy as np
import pandas as pd
import MySQLdb as db
import datetime
import requests
from io import StringIO
import json


# Create your views here.
def index(request):
    pass
    

def top20(request):
    r = requests.get('http://www.twse.com.tw/exchangeReport/MI_INDEX20?response=json&date=&_=1530700673269')
    #將JSON變成Python物件，obj變dict, array變list, String變str; 刪除所有","
    s = json.loads(r.text)
    print("=========== df: {}".format(s))
    df = pd.DataFrame(s['data'], columns=s['fields'])
    #將"排名"設為index
    df = df.set_index(["排名"])
    #並資料中的逗號刪除
    df = df.apply(lambda s: s.str.replace(',', ''))
    df.drop(columns=["成交筆數","漲跌(+/-)","漲跌價差","最後揭示買價"] , inplace=True)
    # df.drop(labels="成交筆數" , axis=1, inplace=True)
    # print("=========== df: {}".format(df))
    return HttpResponse(df.to_json(force_ascii=False), content_type="application/json")
    # 下面這行會出現許多\
    # return JsonResponse(df.to_json(force_ascii=False), content_type="application/json", safe=False)

def us(request):
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=2C8MUXABNVMED4DS')
    #將JSON變成Python物件，obj變dict, array變list, String變str; 刪除所有","
    s = json.loads(r.text)
    df = pd.DataFrame(s['Time Series (Daily)'])
    print("=========== df: {}".format(df.unstack()))
    return HttpResponse(df.to_json(force_ascii=False), content_type="application/json")