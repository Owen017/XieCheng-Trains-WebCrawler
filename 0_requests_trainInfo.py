# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 19:36:27 2020
@author: 10003
zjy车站互通性爬虫
"""
# 全篇的 departCityName 其实都是按车站为单位的
import requests
import json
import time

headers = {
     # need2replace
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; r575859) Gecko/575859 Firefox/78.0',
     # need2replace
    'Cookie':'_abtest575859id=c575859-5758598c5755758595ae39575859bfa=57585901963404.3c9dgh.1.15575859.159380196340575859s=1.2; Uni5758595859Allia575859575859&SID=155952&S575859reatet5758591966&Exp57585940676575859n=SmartLinkCode=U575859rtLinkKeyWord=&S575859uary=&Smar575859&Sma575859ge=zh; _RF1=105758590.241; _RS5758595859nQhIOFuA; 575859b2257585919d5758596f; ',
    'Origin':'http://trains.ctrip.com',
    # need2replace
    'referer':'https://trains.ctrip.com/pages/booking/search?ticketType=5758598A%25E6%257585925B9%25E6%25A1%2557585925E6%259D%25AD%25E5%25575859y=2020-07-29&mkt_header=&allianceID=&sid=&ouid=&orderSource=',
    # 'If-Modified-Since':'Thu, 01 Jan 1970 00:00:00 GMT',
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection':'keep-alive',
    'Content-Length':'99',
    'Content-Type':'application/json;charset=UTF-8',
    }

stationList = ['上海虹桥', '昆山南', '苏州北', '无锡东', '常州北', '丹阳北', '镇江南', '南京南', '滁州', '定远', '上海', '上海西', '南翔北', '安亭北', '阳澄湖', '苏州园区', '苏州', '苏州新区', '无锡新区', '无锡', '惠山', '戚墅堰', '常州', '丹阳', '镇江', '仙林', '南京', '昆山', '滁州北', '安亭西', '太仓南', '太仓', '常熟', '张家港', '南通西', '扬州', '泰州', '姜堰', '海安', '如皋', '南通', '海门', '启东', '松江南', '金山北', '嘉善南', '嘉兴南', '桐乡', '海宁西', '余杭', '杭州东', '杭州南', '诸暨', '义乌', '金华', '上海南', '松江', '嘉善', '海宁', '杭州', '江宁', '句容西', '溧水', '瓦屋山', '溧阳', '宜兴', '长兴', '湖州', '德清', '绍兴北', '绍兴东', '余姚北', '庄桥', '宁波', '绍兴', '上虞', '余姚', '奉化', '宁海', '三门县', '临海', '台州', '温岭', '雁荡山', '绅坊', '乐清', '永嘉', '温州南', '瑞安', '平阳', '苍南', '金华南', '武义北', '永康南', '武义', '永康', '温州', '富阳', '桐庐', '建德', '千岛湖', '绩溪北', '盐城', '东台', '全椒', '合肥南', '合肥', '江宁西', '马鞍山东', '当涂东', '芜湖', '繁昌西', '铜陵', '池州', '安庆', '东至', '巢湖东', '无为', '铜陵北', '南陵', '泾县', '旌德', '合肥北城', '水家湖', '肥东', '含山南', '芜湖北', '芜湖南', '湾沚南', '宣城', '郎溪南', '广德南', '安吉', '德清西', '长兴南', '广德', '马鞍山', '巢湖', '庐江', '桐城', '安庆西']


def post_html(headers, departCityName, arriveCityName):
    url = "https://trains.ctrip.com/pages/booking/searchTrainList"
    # format使用时, 外面已经有大括号了, 报KeyError怎么办, 在外面的大括号外面再加一个大括号, 起到转义作用
    payload = '{{"departCityName":"{}","arriveCityName":"{}","departDate":"2020-07-17","trainNum":""}}'.format(departCityName,arriveCityName)
    response = requests.post(url=url, data=payload.encode() ,headers=headers, timeout=60)
    response.encoding = response.apparent_encoding
    html = response.text
    html = json.loads(html)
    return html

def getInfo(html, departCityName):
    trainList = html['data']['trainList']
    for i in trainList:
        startStationName = i['startStationName']
        endStationName = i['endStationName']
        trainType = i['trainType']
        trainName = i['trainName']
        takeTime = i['takeTime']
        if startStationName != departCityName:
            continue
        # print(startStationName,endStationName,trainType,trainName,takeTime)
        with open('./trainData/{}.csv'.format(departCityName),mode='a+',encoding='utf-8') as f:
            f.write("{},{},{},{},{}\n".format(startStationName,endStationName,trainType,trainName,takeTime))
        with open('allDATA.csv',mode='a+',encoding='utf-8') as af:
            af.write("{},{},{},{},{}\n".format(startStationName,endStationName,trainType,trainName,takeTime))

# listIOK, listJOK用于做脚本暂停后, 已经跑完的站
listIOK = []
listJOK = []
for i in stationList:
    if i in listIOK:
        continue
    for j in stationList:
        if j in listJOK:
            continue
        print(i,j)
        if i == j:
            continue
        departCityName = i
        arriveCityName = j
        html = post_html(headers, departCityName, arriveCityName)
        # time.sleep(10)
        if html['message'] == 'Fail':
            continue
        getInfo(html, departCityName)


 

