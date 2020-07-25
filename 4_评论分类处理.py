# -*- coding = 'utf-8' -*-
__author__ = '七月小组'
'''本程序功能：从评论数据中按前缀词抽取评论，保存到不同的文件，用于构建语义网络。 
   最后并可视化每种评论的条数'''
import jieba
import re
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt


#机械压缩函数，去除一行数据中连续重复的字段
def str_unique(raw_str,reverse=False):
    if reverse:
        raw_str = raw_str[::-1]
    res_str = ''
    for i in raw_str:
        if i not in res_str:
            res_str += i
    if reverse:
        res_str = res_str[::-1]
    return res_str

#提取特定前缀评论
with open('./data/dell_pc_data.csv',encoding='utf-8')as file:
    reader=csv.reader(file)
    column=[row[2]for row in reader]

ls=["包装保护","外形外观","画面品质","跑分评测","运行速度","游戏效果"]#不同的前缀词
len_comment = []#不同前缀词的评论各自的总条数
string_data = re.sub(u"(', ')", "\n",str(column) )
for i in range(0,6):
    comm=re.findall(r"{}(.+?)\\n*".format(ls[i]),string_data)
    name=['评论内容']
    comment=pd.DataFrame(columns=name,data=comm)
    comment.to_csv("./data/{}.csv".format(ls[i]),index=False)
    #步骤2
    # #去除空值
    comment.dropna(inplace=True)
    #步骤3
    # #去重
    comment= pd.DataFrame(comment['评论内容'].apply(lambda s: s.strip()))#每一行都去除前后空格
    comment= pd.DataFrame(comment['评论内容'].unique())#行间去重
    # #步骤5
    # #机械压缩,去除被压缩后长度不满4的语句
    ser1 = comment[0].apply(str_unique)
    comment = pd.DataFrame(ser1.apply(str_unique, reverse=True))
    comment = comment[comment[0].apply(len) >= 4]
    #步骤6
    # #jieba分词
    comment = pd.DataFrame(comment[0].apply(lambda s: ' '.join(jieba.cut(s))))
    comment = pd.DataFrame(comment[0].apply(lambda s: s.split(' ')))
    #步骤7
    # #去除停用词
    stopwords_path = './data/stopwords.txt'#停用词文件的路径
    with open(stopwords_path, 'r', encoding='utf-8') as fr:
        stopwords = fr.read()#读取整个文件，返回一个字符串
        stopwords = stopwords.split('\n')#以换行符为结点，将字符串分割，形成停用词列表
        stopwords += [' ', '', '\n']#加入一些特殊停用词
        # #对于comment中的每一行数据，保留列表中不在stopwords中的元素
    comment = pd.DataFrame(comment[0].apply(lambda s: [i for i in s if i not in stopwords]))
    comment= pd.DataFrame(comment[0].apply(lambda s: ' '.join(s)))
    #步骤8
    # #保存经过处理后的评论数据
    comment_data_path = './data/comment_data{}.txt'.format(i)
    len_comment.append(len(comment))
    comment.to_csv(comment_data_path, encoding='ANSI', header=None, index=None)
    os.remove("./data/{}.csv".format(ls[i]))
#步骤9
#画出柱状图，横轴为前缀词，纵轴为评论条数
plt.figure()
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.bar(ls, len_comment, width=0.5)
plt.ylabel('评论条数')
plt.title('类别-评论数')
plt.show()