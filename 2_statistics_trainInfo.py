# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 09:56:53 2020
@author: 10003
zjy车站互通性结果统计, 需要30min+
"""
import pymysql

# 站点列表, 共141个站点
stationList = ['上海虹桥', '昆山南', '苏州北', '无锡东', '常州北', '丹阳北', '镇江南', '南京南', '滁州', '定远', '上海', '上海西', '南翔北', '安亭北', '阳澄湖', '苏州园区', '苏州', '苏州新区', '无锡新区', '无锡', '惠山', '戚墅堰', '常州', '丹阳', '镇江', '仙林', '南京', '昆山', '滁州北', '安亭西', '太仓南', '太仓', '常熟', '张家港', '南通西', '扬州', '泰州', '姜堰', '海安', '如皋', '南通', '海门', '启东', '松江南', '金山北', '嘉善南', '嘉兴南', '桐乡', '海宁西', '余杭', '杭州东', '杭州南', '诸暨', '义乌', '金华', '上海南', '松江', '嘉善', '海宁', '杭州', '江宁', '句容西', '溧水', '瓦屋山', '溧阳', '宜兴', '长兴', '湖州', '德清', '绍兴北', '绍兴东', '余姚北', '庄桥', '宁波', '绍兴', '上虞', '余姚', '奉化', '宁海', '三门县', '临海', '台州', '温岭', '雁荡山', '绅坊', '乐清', '永嘉', '温州南', '瑞安', '平阳', '苍南', '金华南', '武义北', '永康南', '武义', '永康', '温州', '富阳', '桐庐', '建德', '千岛湖', '绩溪北', '盐城', '东台', '全椒', '合肥南', '合肥', '江宁西', '马鞍山东', '当涂东', '芜湖', '繁昌西', '铜陵', '池州', '安庆', '东至', '巢湖东', '无为', '铜陵北', '南陵', '泾县', '旌德', '合肥北城', '水家湖', '肥东', '含山南', '芜湖北', '芜湖南', '湾沚南', '宣城', '郎溪南', '广德南', '安吉', '德清西', '长兴南', '广德', '马鞍山', '巢湖', '庐江', '桐城', '安庆西']
# 初始化存放结果的字典
dictNum = {}
'''
字典dictNum的形式
{'上海虹桥,昆山南':[G, D(包括C), O(other)], '上海虹桥,苏州北':[G, D, O], ...}
'''

# 连接数据库
db = pymysql.connect("localhost","root","happy123","trainInfo")
cursor = db.cursor()

# 设计统计函数
def getCount(ss, es, tt):
    # 创建查询语句并执行查询
    sql = "SELECT count(*) FROM changsanjiao \
        WHERE startStationName = '{}' AND endStationName = '{}' AND trainType = '{}'".format(ss, es, tt)
    cursor.execute(sql)
    # 获取查询结果
    result = cursor.fetchall()
    return result[0][0]

# 开始统计, 结果存入dictNum字典中
for i in stationList:
    print(stationList.index(i))
    for j in stationList:
        listResult = []
        # G单独一档, D/C一档, 其他K/T/Z/X一档
        listResult.append(getCount(i,j,'G'))
        listResult.append(getCount(i,j,'D')+getCount(i,j,'C'))
        listResult.append(getCount(i,j,'K')+getCount(i,j,'T')+getCount(i,j,'Z')+getCount(i,j,'X'))
        dictNum[i+','+j] = listResult

# 关闭数据库连接
db.close()

# 计算结果dictNum存储
import numpy as np
np.save("dictNum.npy",dictNum)




