# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 19:36:27 2020
@author: 10003
长三角城市铁路站点通达度分析————数据准备
(1)携程爬虫, 得到分出发站点的trainData文件夹和汇总数据allDATA.csv
"""
# 全篇的 departCityName 其实都是按车站为单位的
import requests
import json
import time

# 反爬虫, 不过携程对爬虫管控并不算很严, 在被间断性打断爬虫运行之后使用相同的U-A还可以继续爬
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

# 141个站点的stationList
stationList = ['上海虹桥', '昆山南', '苏州北', '无锡东', '常州北', '丹阳北', '镇江南', '南京南', '滁州', '定远', '上海', '上海西', '南翔北', '安亭北', '阳澄湖', '苏州园区', '苏州', '苏州新区', '无锡新区', '无锡', '惠山', '戚墅堰', '常州', '丹阳', '镇江', '仙林', '南京', '昆山', '滁州北', '安亭西', '太仓南', '太仓', '常熟', '张家港', '南通西', '扬州', '泰州', '姜堰', '海安', '如皋', '南通', '海门', '启东', '松江南', '金山北', '嘉善南', '嘉兴南', '桐乡', '海宁西', '余杭', '杭州东', '杭州南', '诸暨', '义乌', '金华', '上海南', '松江', '嘉善', '海宁', '杭州', '江宁', '句容西', '溧水', '瓦屋山', '溧阳', '宜兴', '长兴', '湖州', '德清', '绍兴北', '绍兴东', '余姚北', '庄桥', '宁波', '绍兴', '上虞', '余姚', '奉化', '宁海', '三门县', '临海', '台州', '温岭', '雁荡山', '绅坊', '乐清', '永嘉', '温州南', '瑞安', '平阳', '苍南', '金华南', '武义北', '永康南', '武义', '永康', '温州', '富阳', '桐庐', '建德', '千岛湖', '绩溪北', '盐城', '东台', '全椒', '合肥南', '合肥', '江宁西', '马鞍山东', '当涂东', '芜湖', '繁昌西', '铜陵', '池州', '安庆', '东至', '巢湖东', '无为', '铜陵北', '南陵', '泾县', '旌德', '合肥北城', '水家湖', '肥东', '含山南', '芜湖北', '芜湖南', '湾沚南', '宣城', '郎溪南', '广德南', '安吉', '德清西', '长兴南', '广德', '马鞍山', '巢湖', '庐江', '桐城', '安庆西']

# 获取抓包得到的响应json, 解析后作函数返回值返回
# 注意携程的参数传递用的是POST方法, 参数存在字符串形式的字典payload里
def post_html(headers, departCityName, arriveCityName):
    url = "https://trains.ctrip.com/pages/booking/searchTrainList"
    # format使用时, 会把字典的大括号也匹配识别进去
    # 外面已经有大括号了, 报KeyError怎么办, 在外面的大括号外面再加一个大括号, 起到转义作用
    payload = '{{"departCityName":"{}","arriveCityName":"{}","departDate":"2020-07-17","trainNum":""}}'.format(departCityName,arriveCityName)
    response = requests.post(url=url, data=payload.encode() ,headers=headers, timeout=60)
    response.encoding = response.apparent_encoding
    html = response.text
    html = json.loads(html)
    return html

# 提取抓包返回值中的有效信息
def getInfo(html, departCityName):
    trainList = html['data']['trainList']
    for i in trainList:
        startStationName = i['startStationName']
        endStationName = i['endStationName']
        trainType = i['trainType']
        trainName = i['trainName']
        takeTime = i['takeTime']
        # 携程的铁路查询逻辑是按照城市划分的, 但本项目按照站点划分, 故剔除非本站点的同城车站
        # 如设置出发站为上海虹桥, 查询得到的结果里会包含上海站和上海南站的数据, 
        # 上海站和上海南站在站点List中都有记录。所以在上海虹桥站查询中需要剔除他们。
        if startStationName != departCityName:
            continue
        # 这里为项目后续需要, 分两块写入数据, 一块是分站点存储成141个csv, 一块是全部存进一个csv, 方便存入数据库
        with open('./trainData/{}.csv'.format(departCityName),mode='a+',encoding='utf-8') as f:
            f.write("{},{},{},{},{}\n".format(startStationName,endStationName,trainType,trainName,takeTime))
        # mode='a+', 指打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾，即文件打开时会是追加模式;
        # 如果该文件不存在，创建新文件用于读写。
        with open('allDATA.csv',mode='a+',encoding='utf-8') as af:
            af.write("{},{},{},{},{}\n".format(startStationName,endStationName,trainType,trainName,takeTime))

# listIOK, listJOK用于区别脚本程序在被携程反爬暂停后, 已经爬完的站点, 方便接着之前已完成的站点继续爬
listIOK = []
listJOK = []
for i in stationList:
	# 如果这个站点已经作为出发站爬过, 跳过
    if i in listIOK:
        continue
    for j in stationList:
    	# 如果这个站点已经作为到达站爬过, 跳过
        if j in listJOK:
            continue
        # 观察程序运行进度
        print(i,j)
        # 同站起迄, 跳过
        if i == j:
            continue
        departCityName = i
        arriveCityName = j
        html = post_html(headers, departCityName, arriveCityName)
        # time.sleep(10)
        # 有的站点之间没有互通线路, 响应值‘message’会为'Fail', 跳过
        if html['message'] == 'Fail':
            continue
        getInfo(html, departCityName)


 