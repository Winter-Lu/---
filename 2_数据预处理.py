# -*- coding = 'utf-8' -*-
__author__ = '七月小组'
'''本程序功能：对爬虫爬取的数据进行导入，抽取，预处理'''
#导入库
import jieba
import re
import pandas as pd


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


#步骤1
#读取爬虫爬取的数据，抽取评论数据
data_path = './data/dell_pc_data.csv'
df = pd.read_csv(data_path, encoding='utf-8')
comment = pd.DataFrame(df['评论内容'])
#步骤2
#去除空值
comment.dropna(inplace=True)
#步骤3
#去重
comment = pd.DataFrame(comment['评论内容'].apply(lambda s: s.strip()))#每一行都去除前后空格
comment = pd.DataFrame(comment['评论内容'].unique())#行间去重
#步骤4
#去除多余、干扰的数据，类似“外形外观：”这样的前缀词，系统的默认评论，以及商家自己的评论
comment = pd.DataFrame(comment[0].apply(lambda s: re.sub(r'^.{4}：', '', s)))#去除多余前缀词
comment = comment[comment[0] != '此用户未填写评价内容']#去除系统默认评论
for badword in ['小戴', '深情', '春风十里', '一缕微风', '客官', '小主', '主人', '幸福', '尊敬', '拥抱', '亲爱', '桥梁', '赤诚']:
    comment = comment[comment[0].apply(lambda s: badword not in s)] #去除商家自己的评论
#步骤5
#机械压缩,去除被压缩后长度不满4的语句
ser1 = comment[0].apply(str_unique)
comment = pd.DataFrame(ser1.apply(str_unique, reverse=True))
comment = comment[comment[0].apply(len) >= 4]
#步骤6
#jieba分词
comment = pd.DataFrame(comment[0].apply(lambda s: ' '.join(jieba.cut(s))))
comment = pd.DataFrame(comment[0].apply(lambda s: s.split(' ')))
#步骤7
#去除停用词
stopwords_path = './data/stopwords.txt'#停用词文件的路径
with open(stopwords_path, 'r', encoding='utf-8') as fr:
    stopwords = fr.read()#读取整个文件，返回一个字符串
stopwords = stopwords.split('\n')#以换行符为结点，将字符串分割，形成停用词列表
stopwords += [' ', '', '\n', '\t']#加入一些特殊停用词
#对于comment中的每一行数据，保留列表中不在stopwords中的元素
comment = pd.DataFrame(comment[0].apply(lambda s: [i for i in s if i not in stopwords]))
comment = pd.DataFrame(comment[0].apply(lambda s: ' '.join(s)))
#步骤8
#保存经过处理后的评论数据
comment_data_path = './data/comment_data.txt'
comment.to_csv(comment_data_path, encoding='utf-8', header=None, index=None)
print('数据预处理完毕')