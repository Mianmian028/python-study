#python爬去北京贝壳数据模仿保胜的代码
import pprint

import requests
from requests import RequestException
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os
proxy=False
frequency = 5
#代理工具和请求工具(req,get_proxy)
def req(url):
    headers = {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    while True:
        try:
            webdata  = requests.get(url,headers=headers,proxies=get_proxy(),timeout = 5)
            time.sleep(frequency)
            if webdata.status_code == 200:
                return webdata
            else:
                pass
        except RequestException as e:
            
            print(e.args)


def get_proxy():
    """
    返回None或形如{"https":"https://127.0.0.1"}的代理
    :return:
    """
    if not proxy:
        return None
    else:
        url = 'http://api.ip.data5u.com/dynamic/get.html?order=44b365bd1275e9f6a0d15b720526f4d4&sep=3'
        while True:
            try:
                webdata = requests.get(url)
                time.sleep(1)
                if webdata.status_code == 200:
                    return {"https":"https://{}".format(webdata.text.strip())}
                else:
                    pass
            except RequestException:
                pass
#抓取区域信息(get_area,get_area_1)
def get_area():
	"""
    抓取区域列表
    :return: list
    """
    res=[]
    url = 'https://bj.ke.com/xiaoqu/'
    domain = 'https://bj.ke.com'
     webdata = req(url)#请求到网页
    soup = BeautifulSoup(webdata.text,'lxml')#获取全部网页内容
    areas = soup.select('div.position dl dd div a')#
    for area,url_ in  [[i.get_text(),domain+i.get('href')] for i in areas]:
            print(url_)#打印出所有区域的网址
    		res.extend(get_area_1(url_))#
    return res#返回到列表

def get_area_1(url):
    #得到某个大区下面各个小区域
    domain = 'https://bj.ke.com'
    webdata = req(url)#请求到网页
    soup = BeautifulSoup(webdata.text, 'lxml')
    areas = soup.select('div.position dl dd div div a')#:nth-of-type(n) 选择器匹配属于父元素的特定类型的第 N 个子元素的每个元素.也就是子区域
    res = [[i.get_text(), domain + i.get('href')] for i in areas]
    pprint.pprint(res)#把区域与网页一一对应
    return res

def get_xiaoqu(areas):
    """
    抓取小区
    :param areas:dict()
    :return:dict()
    """
    res = []#在上个部分res时子区域+URL的列表，此处为空吗？
    for area,url in areas:
        #得到某个子区域下面的所有小区
        webdata = req(url)
        soup = BeautifulSoup(webdata.text,'lxml')
        total = soup.select('h2.total span')[0].get_text()#共找到小区的数量，即提取h2 total中第一个有span的文字
        pages = round((int(total)-1)/30)+1
        for pageno in range(1,pages+1):#range(start, stop[, step])start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;stop: 计数到 stop 结束，但不包括 stop。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1)
            tmp=[]
            url_=url+'pg{}/'.format(pageno)# <模板字符串>.format(<逗号分隔的参数>){}是自变量的替换处
            webdata_ = req(url_)#获取对应网页数据
            soup_ = BeautifulSoup(webdata_.text,'lxml')#用`.text`提取 HTTP 体，即 HTML 文档，lxml HTML解析库   BeautifulSoup(html,’lxml’)  速度快；容错能力强   需要安装，需要C语言库
            xiaoqus = soup_.select('div.content ul.listContent li')#选择小区所在区域网页内容并解析
         	for xiaoqu in xiaoqus:
                title = xiaoqu.select('div.info div.title')[0].get_text().strip()#名称
                xiaoquurl = xiaoqu.select('div.info div.title a')[0].get('href')#网页
                houseInfo = xiaoqu.select('div.info div.houseInfo')[0].get_text()#成交
                positionInfo = xiaoqu.select('div.info div.positionInfo')[0].get_text()#地址
                positionInfo = "".join(positionInfo.split())
                transformInfo =xiaoqu.select('div.info div.taglist span')[0]#地铁
                price = xiaoqu.select('div.xiaoquListItemPrice span')[0].get_text()#价格
                sellCount = xiaoqu.select('div.xiaoquListItemSellCount a span')[0].get_text()#成交
                data = {'title':title,
                        'url':xiaoquurl,
                        'houseInfo':houseInfo,
                        'positionInfo':positionInfo,
                        'tagList':tagList,
                        'price':price,
                        'sellCount':sellCount}
                print(data)
                tmp.append(data)#append() 方法用于在列表末尾添加新的对象。
            res.extend(tmp)#list.extend(seq)，函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
        print(area,'finished!')
        return res#——

