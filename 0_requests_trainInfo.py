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
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4170.0 Safari/537.36 Edg/85.0.552.1',
    # 'Cookie':'_ga=GA1.2.1924561349.1589446686; MKT_CKID=1589446687826.4b6x3.caei; _RSG=eeqY6_h.D3AFKmPZNrf5x9; _RDG=28cf8d4f6a324e200d0eb947e2fa80cb28; _RGUID=a0cdfabf-c68b-4a28-9ec5-a755e367050f; _abtest_userid=f64ff0f1-eb00-4010-96ec-eb3b82a89be8; _gid=GA1.2.1588205113.1593762495; Session=smartlinkcode=U130727&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4902&SID=130727&OUID=&createtime=1593762495&Expires=1594367294705; MKT_CKID_LMT=1593762494773; MKT_Pagesource=PC; ibu_wws_c=1596354509199%7Czh-cn; _jzqco=%7C%7C%7C%7C%7C1.1753895851.1589446687771.1593762494758.1593762512916.1593762494758.1593762512916.0.0.0.3.3; __zpspc=9.2.1593762494.1593762512.2%233%7Ccn.bing.com%7C%7C%7C%7C%23; manualclose=1; ASP.NET_SessionSvc=MTAuMjUuMTQ4LjE0Mnw5MDkwfG91eWFuZ3xkZWZhdWx0fDE1ODkwMDUyMjkzMzM; _RF1=183.232.44.18; _bfa=1.1589446678193.liw5r.1.1589446678193.1593762492241.2.8; _bfs=1.6; _bfi=p1%3D108002%26p2%3D108002%26v1%3D8%26v2%3D7; _gat=1',
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    # 'Cookie':'searchlist=searchlisttop=100; _RSG=ynafgs0PuP8T5huooo3uZA; _RDG=28e938d1d85e6326593884ef9bab057f7a; _RGUID=8678640d-aaa6-4c7c-a8f8-0f2cb2e2b15d; _ga=GA1.2.697192664.1540560476; _abtest_userid=614c1245-c52f-482f-bbe2-0f54164acf90; FlightIntl=Search=[%22TYO|%E4%B8%9C%E4%BA%AC(%E7%BE%BD%E7%94%B0%E6%9C%BA%E5%9C%BA)(HND)|228|TYO|HND|540%22%2C%22SPK|%E6%9C%AD%E5%B9%8C(%E6%96%B0%E5%8D%83%E5%B2%81%E6%9C%BA%E5%9C%BA)(CTS)|641|SPK|CTS|540%22%2C%222020-03-14%22]; MKT_CKID=1582354409193.pmkiv.dryr; __utma=1.697192664.1540560476.1585119538.1585125754.2; __utmz=1.1585125754.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RF1=101.88.0.241; HotelCityID=1358split%E6%BA%A7%E9%98%B3splitLiyangsplit2020-07-18split2020-07-19split0; MKT_CKID_LMT=1593763194744; _gid=GA1.2.708488394.1593763195; MKT_Pagesource=PC; gad_city=bfc57e4d16854aac15936b76ba41619a; _gat=1; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1593792256&Expires=1594397056294; _jzqco=%7C%7C%7C%7C1593763194891%7C1.1456204518.1540560476016.1593791823227.1593792256301.1593791823227.1593792256301.undefined.0.0.107.107; ASP.NET_SessionSvc=MTAuMTQuMjA2LjF8OTA5MHxvdXlhbmd8ZGVmYXVsdHwxNTg5MDA0OTY5NDAw; _bfi=p1%3D108002%26p2%3D100101991%26v1%3D186%26v2%3D185; __zpspc=9.47.1593792256.1593792265.2%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; appFloatCnt=20; _bfa=1.1540560473681.2jga1r.1.1593763191948.1593791820457.38.187.212044; _bfs=1.7',
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    # 'Cookie':'_bfi=p1%3D108002%26p2%3D108001%26v1%3D4%26v2%3D3; appFloatCnt=4; _bfs=1.2; MKT_Pagesource=PC; _gat=1; _RDG=289f587be8a11927a2155a97a86444f818; _gid=GA1.2.1779794915.1593780710; _ga=GA1.2.348189850.1593780710; _bfa=1.1593780705418.a9dsf.1.1593780705418.1593801938746.2.4; _RGUID=f018ce3d-55dc-4d87-8526-771f7da3363f; _RSG=7s4tLrZpO0F_OpezznTcK8; _RF1=58.33.102.30',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Cookie':'_abtest_userid=c14a3382-d31b-4748-8cce-febf95ae399e; _bfa=1.1593801963404.3c9dgh.1.1593801963404.1593801963404.1.2; _bfs=1.2; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1593801966&Expires=1594406766314; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RF1=101.88.0.241; _RSG=8KqTnGTGcs381znQhIOFuA; _RDG=2852e6f401c5b22f2d3e73819dc3201e6f; _RGUID=3da641d4-3177-4508-ae0f-612adac7d048; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1593801966316&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1593801963404.3c9dgh"}; _jzqco=%7C%7C%7C%7C1593801966608%7C1.2045888078.1593801966347.1593801966347.1593801966347.1593801966347.1593801966347.0.0.0.1.1; MKT_CKID=1593801966352.25zh9.fuy4; MKT_CKID_LMT=1593801966354; __zpspc=9.1.1593801966.1593801966.1%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _ga=GA1.2.1257012410.1593801966; _gid=GA1.2.1645279845.1593801966; _gat=1; MKT_Pagesource=PC; _bfi=p1%3D100101991%26p2%3D0%26v1%3D1%26v2%3D0; ASP.NET_SessionSvc=MTAuNjEuMjIuMjl8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU4OTAwNDMyMzE0NQ; gad_city=bfc57e4d16854aac15936b76ba41619a',
    'Origin':'http://trains.ctrip.com',
    'referer':'https://trains.ctrip.com/pages/booking/search?ticketType=0&fromCn=%25E4%25B8%258A%25E6%25B5%25B7%25E8%2599%25B9%25E6%25A1%25A5&toCn=%25E6%259D%25AD%25E5%25B7%259E&day=2020-07-29&mkt_header=&allianceID=&sid=&ouid=&orderSource=',
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


 

