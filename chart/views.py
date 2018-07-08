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
import matplotlib.pyplot as plt


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
    #取得網址上GET傳過來的資料
    ticker = request.GET["ticker"]
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=2C8MUXABNVMED4DS'.format(ticker))
    #將JSON變成Python物件，obj變dict, array變list, String變str; 刪除所有","
    s = json.loads(r.text)
    #只取出價格
    df = pd.DataFrame(s['Time Series (Daily)'])  
    # column & row互換
    df = df.T
    # 更改column 名稱
    df.columns = ['open', 'high', 'low', 'close', 'volumn']
    # 選出前13行，重新排序，改成float
    df = df.head(13).sort_index().astype(float)
    print("*** padas dataframe ***\n{}".format(df))
    # pyplot畫圖
    plt.plot('close', data=df, marker='o')
    plt.title('{} (Daily)'.format(ticker.upper()))
    plt.grid(True)
    # Get the current Axes instance on the current figure
    ax = plt.gca()
    # Setting X axis tick
    ax.xaxis.set_major_locator(plt.IndexLocator(4,0))
    plt.savefig("chart/static/images/{}.png".format(ticker))
    url = "http://localhost:8000/static/images/{}.png".format(ticker)
    # 清除圖片
    plt.clf()
    # return圖片
    return HttpResponse(url)
    # return Json
    # return HttpResponse(df.to_json(force_ascii=False), content_type="application/json")