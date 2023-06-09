import requests
# import pandas as pd
import time
import json

# 行政区域查询 https://lbs.amap.com/api/webservice/guide/api/district

# 高德web key
key = ''  # 高德地图API
# 只支持单个关键词语搜索关键词支持,行政区名称、citycode、adcode

while True:  # 创建循环，如果查询结果成功，跳出循环
    keywords = input('请输入需查询的关键词，例如，搜索国家（中国），搜索省份（例如山东），能够显示市（例如济南），区（例如历下区）:\n')
    # 设置显示下级行政区级数,可选值：0、1、2、3
    subdistrict = input('设置显示下级行政区级数,输入数字：0、1、2、3：\n')
    # 此项控制行政区信息中返回行政区边界坐标点;base:不返回行政区边界坐标点；all:只返回当前查询district的边界值，不返回子节点的边界值；
    extensions = 'base'
    url = f'http://restapi.amap.com/v3/config/district?key={key}&keywords={keywords}&subdistrict={subdistrict}&extensions={extensions}'
    r = requests.get(url)
    data = r.json()
    # print(data)
    建议结果列表 = data['count']
    # print(建议结果列表)
    if 建议结果列表 == '0':
        print('参数输入错误，请重新输入！返回值：', 建议结果列表)
    else:
        break
jsontext = {'citys':[]}

行政区数据列表 = []  # 创建空列表，用户存储查询的数据

s1 = data['districts'][0]['adcode']  # 区域编码
s2 = data['districts'][0]['name']  # 行政区名称
s3 = data['districts'][0]['center']  # 区域中心点
s4 = data['districts'][0]['level']  # 行政区划级别
s5 = data['districts'][0]['citycode']  # 城市编码
if s4 == 'country':
    行政区数据列表.append([s2, '', '', '', '', s1, s3, s4, s5])  # 国家
    # jsontext['points'].append({'name':s2, 'citycode':s5})  # 国家


if s4 == 'province':
    # 行政区数据列表.append(['', s2, '', '', '', s1, s3, s4, s5])  # 省份
       
     jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份
if s4 == 'city':
    # 行政区数据列表.append(['', '', s2, '', '', s1, s3, s4, s5])  # 市
    jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份

if s4 == 'district':
    # 行政区数据列表.append(['', '', '', s2, '', s1, s3, s4, s5])  # 区县
    jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份
if s4 == 'street':
    # 行政区数据列表.append(['', '', '', '', s2, s1, s3, s4, s5])  # 街道
    jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份

一级行政区数据 = data['districts'][0]['districts']
一级行政区个数 = len(一级行政区数据)
#print(一级行政区个数)

for i in range(0, 一级行政区个数):
    s1 = 一级行政区数据[i]['adcode']
    s2 = 一级行政区数据[i]['name']
    s3 = 一级行政区数据[i]['center']
    s4 = 一级行政区数据[i]['level']
    s5 = 一级行政区数据[i]['citycode']
    if s4 == 'country':
        # 行政区数据列表.append([s2, '', '', '', '', s1, s3, s4, s5])  # 国家
        jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份
    if s4 == 'province':
        # 行政区数据列表.append(['', s2, '', '', '', s1, s3, s4, s5])  # 省份
        jsontext['citys'].append({'adcode' : s1, 'name':s2})  # 省份
    if s4 == 'city':
        # 行政区数据列表.append(['', '', s2, '', '', s1, s3, s4, s5])  # 市
        jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
    if s4 == 'district':
        # 行政区数据列表.append(['', '', '', s2, '', s1, s3, s4, s5])  # 区县
        jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
    if s4 == 'street':
        # 行政区数据列表.append(['', '', '', '', s2, s1, s3, s4, s5])  # 街道
        jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份

    二级行政区数据 = 一级行政区数据[i]['districts']
    二级行政区个数 = len(二级行政区数据)

    for x in range(0, 二级行政区个数):
        s1 = 二级行政区数据[x]['adcode']
        s2 = 二级行政区数据[x]['name']
        s3 = 二级行政区数据[x]['center']
        s4 = 二级行政区数据[x]['level']
        s5 = 二级行政区数据[x]['citycode']
        if s4 == 'country':
            # 行政区数据列表.append([s2, '', '', '', '', s1, s3, s4, s5])  # 国家
            jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
        if s4 == 'province':
            # 行政区数据列表.append(['', s2, '', '', '', s1, s3, s4, s5])  # 省份
            jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
        if s4 == 'city':
            # 行政区数据列表.append(['', '', s2, '', '', s1, s3, s4, s5])  # 市
            jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
        if s4 == 'district':
            # 行政区数据列表.append(['', '', '', s2, '', s1, s3, s4, s5])  # 区县
            jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
        if s4 == 'street':
            # 行政区数据列表.append(['', '', '', '', s2, s1, s3, s4, s5])  # 街道
            jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份

        三级行政区数据 = 二级行政区数据[x]['districts']
        三级行政区个数 = len(三级行政区数据)

        for y in range(0, 三级行政区个数):
            s1 = 三级行政区数据[y]['adcode']
            s2 = 三级行政区数据[y]['name']
            s3 = 三级行政区数据[y]['center']
            s4 = 三级行政区数据[y]['level']
            s5 = 三级行政区数据[y]['citycode']
            if s4 == 'country':
                # 行政区数据列表.append([s2, '', '', '', '', s1, s3, s4, s5])  # 国家
                jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
            if s4 == 'province':
                # 行政区数据列表.append(['', s2, '', '', '', s1, s3, s4, s5])  # 省份
                jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
            if s4 == 'city':
                # 行政区数据列表.append(['', '', s2, '', '', s1, s3, s4, s5])  # 市
                jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
            if s4 == 'district':
                # 行政区数据列表.append(['', '', '', s2, '', s1, s3, s4, s5])  # 区县
                jsontext['citys'].append({'adcode' : s1, 'name':s2, 'citycode':s5})  # 省份
            if s4 == 'street':
                # 行政区数据列表.append(['', '', '', '', s2, s1, s3, s4, s5])  # 街道
                jsontext['citys'].append({'adcode' : s1, 'name': s2, 'citycode': s5})  # 省份

# df = pd.DataFrame(行政区数据列表, columns=['国家', '省份', '市', '区县', '街道', '区域编码', '区域中心点', '行政区划分级别', '城市编码'])
# print(行政区数据列表)
# df = jsontext = {'points': 行政区数据列表}


# print('jsontext:=====' + str(jsontext))

路径 = '行政区域查询-' + str(time.strftime("%Y-%m-%d %H时%M分%S秒", time.localtime())) + '.json'
with open(路径, 'w', encoding='utf-8') as f:#此处用到的是字节形式将列表写入文件，如果要读入同样也要用decode转化为字符
      
        print("原始数据：",jsontext) 
        json.dump(jsontext, f)
        # print("转换成json后的数据：",j_str)
        # l_str = json.loads(j_str)
        # print("转换成字典类型后的数据：",l_str)

        # f.write(j_str)

        # f.close()      


# df.to_csv(路径)
input('查询完成，结果输出在本程序目录下：' + 路径)
