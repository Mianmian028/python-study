#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__ = "Brady Hu"
# __date__ = "20180326"
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
    url = 'https://bj.lianjia.com/xiaoqu/'
    domain = 'https://bj.lianjia.com'
    webdata = req(url)#请求到网页
    soup = BeautifulSoup(webdata.text,'lxml')#获取全部网页内容
    areas = soup.select('div.position dl dd div a')#抓区小区信息路径，不同级的加空格
    for area,url_ in  [[i.get_text(),domain+i.get('href')] for i in areas]:#get_text只获得文本内容，get()获得对应属性标签，因此domin+i.get(‘href')则进入对应区域网页
        print(url_)#打印出所有区域的网址
        res.extend(get_area_1(url_))#
    return res#返回到列表

def get_area_1(url):
    #得到某个大区下面各个小区域
    domain = 'https://bj.lianjia.com'
    webdata = req(url)#请求到网页
    soup = BeautifulSoup(webdata.text, 'lxml')
    areas = soup.select('div.position dl dd > div > div:nth-of-type(2) a')#:nth-of-type(n) 选择器匹配属于父元素的特定类型的第 N 个子元素的每个元素.也就是子区域
    res = [[i.get_text(), domain + i.get('href')] for i in areas]
    pprint.pprint(res)#把区域与网页一一对应
    return res
#抓取小区列表
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
                #语法：  'sep'.join(seq)参数说明，sep：分隔符。可以为空，seq：要连接的元素序列、字符串、元组、字典，上面的语法即：以sep作为分隔符，将seq所有的元素合并成一个新的字符串
                # split() 通过指定分隔符对字符串进行切片，str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。num -- 分割次数。
                tagList = [i.get_text() for i in xiaoqu.select('div.info div.tagList span')]#交通地铁
                price = xiaoqu.select('div.xiaoquListItemPrice span')[0].get_text()#价格
                sellCount = xiaoqu.select('div.xiaoquListItemSellCount a span')[0].get_text()#成交量
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
    return res

def crawl_xiaoqu():
    print("LOG: {} start crawl xiaoqu!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))#作用是格式化时间戳为本地的时间。In [13]: time.localtime();Out[13]: time.struct_time(tm_year=2018, tm_mon=1, tm_mday=12, tm_hour=23, tm_min=6, tm_sec=14, tm_wday=4, tm_yday=12, tm_isdst=0)
    areas=get_area()#区域等于区域1
    xiaoqulist  = get_xiaoqu(areas)#对应的区域小区列表
    print(xiaoqulist)
    # df = pd.DataFrame(xiaoqulist)#把小区列表转换为数据结构
    # df.to_excel('小区信息.xlsx')#储存为excel
    # print("LOG: {} finish crawl xiaoqu!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))#抓取结束标注#抓取各小区详细信息
def crawl_xiaoqu_info():
    xiaoqu = pd.read_excel('小区信息.xlsx')#把上述的小区列表转为数据结构
    for index, item in xiaoqu.iterrows():#历遍上述数据结构的内容，输出为元组
        if os.path.exists("xiaoqu/{}.xlsx".format(item['title'])):#如果以小区的名字命名的文件存在，则继续
            continue
        else:
            print("LOG: {} xiaoqu {} start!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item['title']))#time.strftime(format[, t])，format -- 格式字符串，t -- 可选的参数t是一个struct_time对象。%y 两位数的年份表示（00-99）；%Y 四位数的年份表示（000-9999）；%m 月份（01-12）；%d 月内中的一天（0-31）
#%H 24小时制小时数（0-23）；%I 12小时制小时数（01-12）；%M 分钟数（00=59）；%S 秒（00-59）；
            crawl_one_xiaoqu(item)
            print("LOG: {} xiaoqu {} finished!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item['title']))

def crawl_one_xiaoqu(xiaoquinfo):
    """
    分别对：
    https://sz.lianjia.com/xiaoqu/2411048738974/
    https://sz.lianjia.com/ershoufang/c2411048738974/
    https://sz.lianjia.com/chengjiao/c2411048738974/
    https://sz.lianjia.com/zufang/c2411048738974/
    进行抓取，并保存到同一个excel中
    """
    Writer = pd.ExcelWriter('xiaoqu/{}.xlsx'.format(xiaoquinfo['title']))

    basic = {}
    url_basic = xiaoquinfo['url']
    webdata = req(url_basic)
    soup= BeautifulSoup(webdata.text,'lxml')
    if soup.select('div.xiaoquPrice span.xiaoquUnitPrice'):
        price = soup.select('div.xiaoquPrice span.xiaoquUnitPrice')[0].get_text()
    else:
        price = None
    basic['price']=price
    for item in soup.select('div.xiaoquInfoItem'):
        basic[item.select('span.xiaoquInfoLabel')[0].get_text()]=item.select('span.xiaoquInfoContent')[0].get_text()
    bdlnglat = re.compile("resblockPosition:'(.*?),(.*?)'").findall(webdata.text)[0]
    basic['bdlnglat']=bdlnglat
    print(basic)
    pd.DataFrame([basic]).to_excel(Writer,'basic')

    #二手房
    url_ershoufang = xiaoquinfo['url'].replace('xiaoqu/','ershoufang/c')
    ershoufang = []
    webdata = req(url_ershoufang)
    soup = BeautifulSoup(webdata.text, 'lxml')
    total = soup.select('.total span')[0].get_text()
    pages = round((int(total) - 1) / 30) + 1
    for pageno in range(1,pages+1):
        url= url_ershoufang.replace('ershoufang/c','ershoufang/pg{}c'.format(pageno))
        webdata = req(url)
        soup = BeautifulSoup(webdata.text, 'lxml')
        for item in soup.select('ul.sellListContent li div.info'):
            title= item.select('div.title')[0].get_text()
            url = item.select('div.title')[0].get('href')
            address = item.select('div.address')[0].get_text()
            flood = item.select('div.flood')[0].get_text()
            followInfo = item.select('div.followInfo')[0].get_text()
            tag = [i.get_text() for i in item.select('div.tag span')]
            priceInfo =[item.select('div.totalPrice span')[0].get_text(),
                        item.select('div.unitPrice span')[0].get_text()]
            data = {'title':title,
                    'url':url,
                    'address':address,
                    'flood':flood,
                    'followInfo':followInfo,
                    'tag':tag,
                    'priceInfo':priceInfo}
            ershoufang.append(data)
    pprint.pprint(ershoufang)
    pd.DataFrame(ershoufang).to_excel(Writer,'ershoufang')

    #成交
    url_chengjiao = xiaoquinfo['url'].replace('xiaoqu/', 'chengjiao/c')
    chengjiao=[]
    webdata = req(url_chengjiao)
    soup = BeautifulSoup(webdata.text, 'lxml')
    total = soup.select('.total span')[0].get_text()
    pages = round((int(total) - 1) / 30) + 1
    for pageno in range(1, pages + 1):
        url = url_chengjiao.replace('chengjiao/c', 'chengjiao/pg{}c'.format(pageno))
        webdata = req(url)
        soup = BeautifulSoup(webdata.text, 'lxml')
        for item in soup.select('ul.listContent li div.info'):
            title = item.select('div.title')[0].get_text()
            url = item.select('div.title')[0].get('href')
            houseInfo = item.select('div.address div.houseInfo')[0].get_text()
            dealDate = item.select('div.address div.dealDate')[0].get_text()
            totalPrice = item.select('div.address div.totalPrice')[0].get_text()

            positionInfo = item.select('div.flood div.positionInfo')[0].get_text()
            source = item.select('div.flood div.source')[0].get_text()
            unitPrice = item.select('div.flood div.unitPrice')[0].get_text()
            dealHouseInfo =[i.get_text() for i in item.select('div.dealHouseInfo span.dealHouseTxt span')]
            dealCycleInfo = [i.get_text() for i in item.select('span.dealCycleTxt span')]
            data = {'title': title,
                    'url':url,
                    'houseInfo':houseInfo,
                    'dealDate':dealDate,
                    'totalPrice':totalPrice,
                    'positionInfo':positionInfo,
                    'source':source,
                    'unitPrice':unitPrice,
                    'dealHouseInfo':dealHouseInfo,
                    'dealCycleInfo':dealCycleInfo}
            chengjiao.append(data)
    pprint.pprint(chengjiao)
    pd.DataFrame(chengjiao).to_excel(Writer, 'chengjiao')

    #租房
    url_zufang = xiaoquinfo['url'].replace('xiaoqu/', 'zufang/c')
    zufang =[]
    webdata = req(url_zufang)
    soup = BeautifulSoup(webdata.text, 'lxml')
    total = soup.select('h2 > span')[0].get_text()
    pages = round((int(total) - 1) / 30) + 1
    for pageno in range(1,pages+1):
        url = url_zufang+'pg{}/'.format(pageno)
        webdata = req(url)
        soup = BeautifulSoup(webdata.text,'lxml')
        for item in soup.select('ul.house-lst li div.info-panel'):
            title = item.select('h2 a')[0].get_text()
            url = item.select('h2 a')[0].get('href')
            where =item.select('div.where')[0].get_text()
            other = item.select('div.other')[0].get_text()
            chanquan = [i.get_text() for i in item.select('div.chanquan div span span')]
            price = item.select('div.price span')[0].get_text()
            price_pre = item.select('div.price-pre')[0].get_text()
            square = item.select('div.square div span')[0].get_text()
            data = {'title':title,
                    'url':url,
                    'where':where,
                    'other':other,
                    'chanquan':chanquan,
                    'price':price,
                    'price_pre':price_pre,
                    'square':square}
            zufang.append(data)
    pprint.pprint(zufang)
    pd.DataFrame(zufang).to_excel(Writer,'zufang')

    Writer.close()
#合并得到完整数据
def merge_data():
    sheets = ['basic', 'ershoufang', 'chengjiao', 'zufang']
    for sheet in sheets:
        dfs = []
        for item in os.listdir('xiaoqu'):
            dfs.append(pd.read_excel('xiaoqu/' + item, sheetname=sheet))
        res = pd.concat(dfs)
        res.to_excel(sheet + '.xlsx',index=False)

if __name__=='__main__':#此部分为运行脚本的条件，当此脚本被单独运行时，执行下列程序
    crawl_xiaoqu()
    # crawl_xiaoqu_info()
    # merge_data()