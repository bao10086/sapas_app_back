# -*- coding = utf-8 -*-
# @Time : 2022/11/21 10:07
# @Author : 曾佳宝
# @File : test.py
# @Software : PyCharm
import cpca

location_str = ["上海市黄浦区"]

df = cpca.transform(location_str)

print("省份：" + df.iat[0, 0])

print("城市：" + df.iat[0, 1])

print("区域：" + df.iat[0, 2])

print("详细：" + df.iat[0, 3])
