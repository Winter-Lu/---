# -*- coding = 'utf-8' -*-
__author__ = '七月小组'
'''本程序功能：使用爬虫，爬取京东商城戴尔笔记本电脑的数据'''
#导入库
import requests
import csv
import re
import time
import random


def spiderFromUrl(url):
    '''从给定的一个url，爬取评论数据，返回一个列表，列表元素也是一个列表，包含用户名，评论时间，评论内容'''
    response = requests.get(url, headers=headers)#取得响应
    response.raise_for_status()#异常检测
    response.encoding = 'gbk'#网页数据编码
    text = response.text
    #利用正则表达式匹配想要的信息
    comment = re.findall(r'\"content\":\".*?\"', text)#匹配评论
    name = re.findall(r'\"nickname\":\".*?\"', text)#匹配用户名
    time = re.findall(r'\"creationTime\":\".*?\"', text)#匹配评论时间
    result = []
    for j, k, i in zip(name, time, comment):
        result.append([j[12:-1], k[16:-1], i[11:-1]])
    return result#返回结果[[用户，时间，评论]]


def saveScv(result, path):
    '''向结果文件写入内容的函数'''
    with open(path, 'a', newline='',encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(result)


#步骤1
#初始化文件保存路径，url，headers
#save_path是保存爬取的网页数据的结果文件的路径
save_path = './data/dell_pc_data_test.csv'
#请求头，上面的函数里会使用这个变量
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap\
pleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
#urls里有6类地址，每种地址100个，但是有的种类的地址可能实际不足100个
'''这6类地址对应6类评论：
    全部评价
    好评
    差评
    追评
    视频晒图
    中评
    因为京东网站只给每类评论最多提供100页评论，所以最多能爬取600页数据'''
# urls = [['https://club.jd.com/comment/productPageComments.\
# action?callback=fetchJSON_comment98&productId=&\
# score={0}&sortType=5&page={1}&pageSize=10&isShadowSku=0&fold\
# =1'.format(i, j) for j in range(100)] for i in [1, 3]]#url中的score字段决定了评论的种类

urls = ['https://club.jd.com/comment/productPageComments.\
action?callback=fetchJSON_comment98&productId={2}&\
score={0}&sortType=5&page={1}&pageSize=10&isShadowSku=0&fold\
=1'.format(i, j, k) for j in range(100)  for i in [1, 3] for k in
        [100007152001, 100005322584, 100011396614, 68767776383,
         100006246946, 100010774634, 100011317048, 2136538, 100004901643,
         100005724680, 100006546527, 100007062945]]#url中的score字段决定了评论的种类，productID字段决定了产品，page决定了评论页
#步骤2
#向结果文件中写入表头：用户ID,评论时间,评论内容
head = ['用户ID','评论时间','评论内容']
with open(save_path, 'w', newline='', encoding='utf-8') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(head)
#步骤3
#爬取数据，调用spiderFromUrl函数爬取网页，调用saveScv函数保存数据
page_num = 0
for url in urls:
    page_num += 1
    if page_num%120 == 0:#每爬取120条数据就休息一会
        time.sleep(600)
    print('开始爬取第{}页数据……'.format(page_num))
    time.sleep(random.randint(1, 3))  # 增加延时，规避反爬虫机制
    try:
        rows = spiderFromUrl(url)  # rows是spiderFromUrl函数爬取的数据列表[[用户，时间，评论]]
        if len(rows) == 0:
            print('爬取的数据为空！')
            continue
        saveScv(rows, save_path)  # 将rows写入结果文件
    except:
        print('爬取失败！')  # 如果爬取失败，跳过，爬取下一页面
        continue
print('爬取数据完毕')