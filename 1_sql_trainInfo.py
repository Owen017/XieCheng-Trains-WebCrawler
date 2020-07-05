# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 10:01:14 2020
@author: 10003
长三角城市铁路站点通达度分析————数据准备
(2)将allDATA.csv存入MySQL并去重
"""

import pymysql

db = pymysql.connect("localhost","root","happy123","trainInfo")
cursor = db.cursor()

with open('allDATA.csv','r',encoding="utf-8") as f:
    rows = f.readlines()
    for row in rows:
        row = row.rstrip('\n')
        rowlist = row.split(',')
        sql = "INSERT INTO changsanjiao()\
               VALUES ('{0}','{1}','{2}','{3}','{4}')".format(rowlist[0],rowlist[1],rowlist[2],rowlist[3],rowlist[4])
        cursor.execute(sql)
        db.commit()

db.close()

'''
# 创建数据库的时候注意要添加主键id
# MySQL去重语句:
DELETE FROM changsanjiao
WHERE (startStationName, endStationName, trainType, trainName, takeTime) IN (
		SELECT t.startStationName, t.endStationName, t.trainType, t.trainName, t.takeTime
		FROM (
			SELECT startStationName, endStationName, trainType, trainName, takeTime
			FROM changsanjiao
			GROUP BY startStationName, endStationName, trainType, trainName, takeTime
			HAVING COUNT(1) > 1
		) t
	)
	AND id NOT IN (
		SELECT dt.minid
		FROM (
			SELECT MIN(id) AS minid
			FROM changsanjiao
			GROUP BY startStationName, endStationName, trainType, trainName, takeTime
			HAVING COUNT(1) > 1
		) dt
	)
'''