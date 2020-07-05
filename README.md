# XieCheng-Trains-WebCrawler

## 项目简介

#### 统计长三角铁路车站的互通班次数据，分G、D/C、KTZX三类，最终结果用EXCEL表格展示。 ​​​​
#### Python-Requests爬虫获取某一天的铁路车次数据，存储进MySQL数据库中，再查询各站点两两之间的班次数量存进dict，最后用高维数组+DataFrame转换进Excel。

## 文件说明

#### Requirement 需求和车站列表

#### trainData和allDATA.csv 携程爬虫得到的车次数据（未去重）

#### changsanjiao.sql 车次数据（已去重），仓库中已删除

#### dictNum.npy 统计得到的Python字典，用npy存储

#### trainResult.xlsx和trainResult_without_0.xlsx 最终excel表

## 主要代码说明

#### 0_requests_trainInfo.py 携程爬虫，得到分出发站点的trainData文件夹和汇总数据allDATA.csv
#### 1_sql_trainInfo.py 将allDATA.csv存入MySQL并去重
#### 2_statistics_trainInfo.py 统计各站点列车互通班次数据，以字典格式存储于dictNum.npy
#### 3_data2excel_trainInfo.py 将字典通过DataFrame存入EXCEL
