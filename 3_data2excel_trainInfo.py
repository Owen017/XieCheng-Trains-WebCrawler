# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 05:59:19 2020
@author: 10003
长三角城市铁路站点通达度分析————数据准备
(4)将字典通过多维数组和DataFrame存入EXCEL
"""
# 站点列表, 共141个站点
stationList = ['上海虹桥', '昆山南', '苏州北', '无锡东', '常州北', '丹阳北', '镇江南', '南京南', '滁州', '定远', '上海', '上海西', '南翔北', '安亭北', '阳澄湖', '苏州园区', '苏州', '苏州新区', '无锡新区', '无锡', '惠山', '戚墅堰', '常州', '丹阳', '镇江', '仙林', '南京', '昆山', '滁州北', '安亭西', '太仓南', '太仓', '常熟', '张家港', '南通西', '扬州', '泰州', '姜堰', '海安', '如皋', '南通', '海门', '启东', '松江南', '金山北', '嘉善南', '嘉兴南', '桐乡', '海宁西', '余杭', '杭州东', '杭州南', '诸暨', '义乌', '金华', '上海南', '松江', '嘉善', '海宁', '杭州', '江宁', '句容西', '溧水', '瓦屋山', '溧阳', '宜兴', '长兴', '湖州', '德清', '绍兴北', '绍兴东', '余姚北', '庄桥', '宁波', '绍兴', '上虞', '余姚', '奉化', '宁海', '三门县', '临海', '台州', '温岭', '雁荡山', '绅坊', '乐清', '永嘉', '温州南', '瑞安', '平阳', '苍南', '金华南', '武义北', '永康南', '武义', '永康', '温州', '富阳', '桐庐', '建德', '千岛湖', '绩溪北', '盐城', '东台', '全椒', '合肥南', '合肥', '江宁西', '马鞍山东', '当涂东', '芜湖', '繁昌西', '铜陵', '池州', '安庆', '东至', '巢湖东', '无为', '铜陵北', '南陵', '泾县', '旌德', '合肥北城', '水家湖', '肥东', '含山南', '芜湖北', '芜湖南', '湾沚南', '宣城', '郎溪南', '广德南', '安吉', '德清西', '长兴南', '广德', '马鞍山', '巢湖', '庐江', '桐城', '安庆西']

# 载入存储的字典dictNum.npy
# 通过参数allow_pickle=True打开权限, 默认取出的为array格式数据, 使用.item()方法将字典变量取出
import numpy as np 
dictNum = np.load("dictNum.npy",allow_pickle=True).item()

# 创建空多维数组们, dataG/dataDC/dataO表示三种分类的统计表, for i/j遍历赋值
dataG = np.empty([141,141], dtype=int)
dataDC = np.empty([141,141], dtype=int)
dataO = np.empty([141,141], dtype=int)
for i in range(141):
    for j in range(141):
        dataG[i,j] = dictNum[stationList[i]+','+stationList[j]][0]
        dataDC[i,j] = dictNum[stationList[i]+','+stationList[j]][1]
        dataO[i,j] = dictNum[stationList[i]+','+stationList[j]][2]

# 141*141多维数组 to pandas.DataFrame
import pandas as pd
df1 = pd.DataFrame(dataG, index=stationList, columns=stationList)
df2 = pd.DataFrame(dataDC, index=stationList, columns=stationList)
df3 = pd.DataFrame(dataO, index=stationList, columns=stationList)

# 存储三个df到一个excel中的不同sheet, to_excel()的索引index默认为True, 对应df中的index
writer = pd.ExcelWriter('trainResult.xlsx')
df1.to_excel(writer, sheet_name = 'G')
df2.to_excel(writer, sheet_name = 'DC')
df3.to_excel(writer, sheet_name = 'KTZX')
writer.save()
writer.close()

