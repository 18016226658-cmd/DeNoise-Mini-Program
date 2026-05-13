import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import _flatten
import os

from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud  #本例使用 pyecharts中的WordCloud
from pyecharts.globals import SymbolType

# from pyecharts.charts import WordCloud   as  WC  #本例使用 pyecharts中的WordCloud

import webbrowser #爬虫的浏览器自动化

import jieba


# 指定 chrome


currentPath = os.getcwd()  #
# Question , Answer, UserID, UserName, ChatTime, Gender, Birthday ,NL   Year

comments = pd.read_excel(r'./Dialo.xlsx')
# print(comments)
df1=comments['UserName'].value_counts()
print(df1.shape)
print(df1)

print(comments['UserName'].value_counts().head(100))

comments['UserName']  # 本身没有更新
comments.head()

num = comments['UserName'].value_counts().value_counts().sort_index(ascending=False)
num2 = num[:200]    #前面8个
print(num2)



# (1) 聊天数量按照日期分布情况（line)
#######################################################
num =comments['ChatTime'].dt.date.value_counts().sort_index()
# print(num.head())
print(" ============== 1  聊天数量按照日期分布情况（line)  ")
print(num.index[::30])
print(num[::30])
print(" ============== X  Y  =================  ")
X1 = num.index[::30]
Y1 = []
for k in range(len(X1)):
    Y1.append(num[X1[k]])


X1=list(X1)
print(X1)
print(Y1)

plt.figure(figsize=(16,9))
plt.plot(range(len(num)) ,num )

# plt.xticks( range(len(num))[::7] , num.index[::7] ,rotation=45)
plt.xticks( range(len(num))[::30] , num.index[::30] ,rotation=45)
plt.show()

# (2)聊天数量按照周次分布情况 （line)
num =comments['ChatTime'].dt.dayofweek.map({0:'周一' , 1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}).value_counts()
print("聊天数量按照周次分布情况")
print(num.head())

print(" ============== 2  聊天数量按照周次分布情况 （line)  ")
print(num.index)
print(num)
X2 = num.index
Y2 = []
for k in range(len(X2)):
    Y2.append(num[X2[k]])

X2=list(X2)
print(X2)
print(Y2)

plt.rcParams['font.sans-serif']='SimHei'
plt.figure(figsize=(16,9))
plt.plot(range(len(num)) ,num )
plt.xlabel('星期')
plt.ylabel('聊天次数')
plt.xticks( range(len(num)) , num.index ,rotation=45)
plt.title('聊天数量周内分布')
plt.show()

# (3)聊天数量按照 一天里的时间点分布情况  （line)
num =comments['ChatTime'].dt.hour.value_counts().sort_index()
print("聊天数量按照 一天里的时间点分布情况")
# print(num.head())
print(" ============== 3  聊天数量按照 一天里的时间点分布情况  （line) ")
print(num.index)
print(num)
X3 = num.index
Y3 = []
for k in range(len(X3)):
    Y3.append(num[X3[k]])

X3=list(X3)
print(X3)
print(Y3)



plt.rcParams['font.sans-serif']='SimHei'
plt.figure(figsize=(16,9))
plt.plot(range(len(num)) ,num )
plt.xlabel('时间')
plt.ylabel('聊天次数')
plt.xticks( range(len(num)) , num.index ,rotation=45)
plt.title('聊天发布数量天内分布')
plt.show()


# (4)聊天数量按照性别点分布情况 (bar)
num =comments['Gender'].value_counts().sort_index()
print("聊天数量按照性别分布情况")
# print(num.head())

print(" ============== 4  聊天数量按照性别点分布情况 (bar) ")
print(num.index)
print(num)
X4 = num.index
Y4 = []
for k in range(len(X4)):
    Y4.append(num[X4[k]])

X4=list(X4)
print(X4)
print(Y4)





plt.rcParams['font.sans-serif']='SimHei'
plt.figure(figsize=(16,9))
plt.bar(x=num.index ,height=num)
plt.xlabel('性别')
plt.ylabel('聊天次数')
plt.title('聊天数量性别的分布')
plt.show()

# (5) 聊天数量按照年龄分布情况  (bar)
num =comments['NL'].value_counts().sort_index()
print("聊天数量按照年龄分布情况")
# print(num.head())

print(" ============== 5  聊天数量按照年龄分布情况  (bar) ")
print(num.index)
print(num)
X5 = num.index
Y5 = []
for k in range(len(X5)):
    Y5.append(num[X5[k]])

X5=list(X5)
print(X5)
print(Y5)



plt.rcParams['font.sans-serif']='SimHei'
plt.figure(figsize=(16,9))
plt.bar(x=num.index ,height=num)
plt.xlabel('年龄')
plt.ylabel('聊天次数')
plt.title('聊天数量按年龄分布')
plt.show()

# (5) 聊天问题词云图
# 指定 chrome 浏览器
# IEPath ="C:\Program Files\Google\Chrome\Application\chrome.exe"
IEPath = r"C:\Users\sumeng\AppData\Local\Google\Chrome\Application\chrome.exe"
webbrowser.register('IE', None, webbrowser.BackgroundBrowser(IEPath))
currentPath = os.getcwd()  # 当前目录 （把以后要用的文件都存在里面）

HTML_file = 'myEcharts_词云图.html'
# Question, Answer
Word = 'Question'

def word_cloud(Word , HTML_file):

    # 数据读取
    comments = pd.read_excel('./Dialo.xlsx').astype(str)

    print(comments[Word])

    # jieba.load_userdict(dict_path)                 # dict_path为文件类对象或自定义词典的路径
    jieba.load_userdict('./word_cloud/hong.txt')    # 加载自定义词典
    pic = plt.imread('./word_cloud/aixin.jpg')

    yp_name = 'ChatGPT聊天'
    # print(jieba.lcut('yp_name'))
    '''
        jieba.cut 和jieba.lcut           #分词库
        lcut 将返回的对象转化为list对象返回
    
        cut(self, sentence, cut_all=False, HMM=True, use_paddle=False)
            sentence: 需要分词的字符串;
            cut_all: 参数用来控制是否采用全模式；
            HMM: 参数用来控制是否使用 HMM 模型;
            use_paddle: 参数用来控制是否使用paddle模式下的分词模式，paddle模式采用延迟加载方式，通过enable_paddle接口安装paddlepaddle-tiny
    
        jieba 是目前表现较为不错的 Python 中文分词组件，它主要有以下特性：
    
        支持四种分词模式：
    
        精确模式
        全模式
        搜索引擎模式
        paddle模式
        支持繁体分词
    
        支持自定义词典
    '''
    # 分词
    comment_cut = comments[Word].apply(jieba.lcut)  # 每一个弹幕评论都使用分词函数 lcut
    print("\n===================================  comment_cut  ===================\n")
    print(comment_cut)
    '''
    0                  [喂, ，, 吉姆, ，, 晚饭, 后, 去, 喝点, 啤酒, 怎么样, ？]
    1                           [什么, 意思, ?, 它会, 帮助, 我们, 放松, 。]
    2        [我, 想, 你, 是, 对, 的, 。, 但是, 我们, 该, 怎么办, 呢, ？, 我,...
    3        [这, 是, 个, 好, 主意, 。, 我, 听说, 玛丽和, 莎莉, 经常, 去, 那里,...
    '''


    # 加载停用词表
    with open('./word_cloud/stoplist.txt', encoding='utf-8') as f:
        stop_words = f.read()
    f.close()
    stop_words += '\n'

    # 去除停用词
    comment_after = comment_cut.apply(lambda x: [i for i in x if i not in stop_words])  # 去除停用词

    print(comment_after)
    '''
    Name: Question, Length: 48392, dtype: object
    0                            [吉姆, 晚饭, 喝点, 啤酒]
    1                                    [它会, 放松]
    2                             [想, 不想, 坐在, 家里]
    3            [主意, 听说, 玛丽和, 莎莉, 打乒乓球, 也许, 四人组]
    '''

    word_fre = pd.Series(  _flatten( list(comment_after) ) ).value_counts()
    print("\n 2 ===================================  word_fre  ===================\n")
    print(word_fre)
    '''
    
    想             3354
    喜欢            1951
    工作            1488
    谢谢            1482
    真的            1310
                  ... 
    引体向上             1
    '''

    # print(type(word_fre))
    # 去除停用词后的词


    #用WordCloud库绘制词云图

    #绘制词云图
    pic = plt.imread('./word_cloud/aixin.jpg')

    # Word_Cloud = WordCloud(mask=pic , background_color='white' ,font_path='c:/windows/Fonts/simhei.TTF')
    # Word_Cloud.fit_words(word_fre)
    # plt.imshow(Word_Cloud)
    # plt.axis('off')
    # plt.show()


    #下面为用 ：pyecharts绘制词云图  不能生成词云图
    print(word_fre.index)

    #弹幕中的“词” 如下
    '''
    Index(['想', '喜欢', '工作', '谢谢', '真的', '我会', '这是', '告诉', '我能', '买',
           ...
           '廉颇', '无济于事', '休完', '受薪', '不令', '引体向上', '金山', '3367', '7834623464',
           '脱帽致敬'],
          dtype='object', length=19255)
    '''

    # 将Series 数据 转换成 List类型
    myList=[]
    for   i  in word_fre.index:
        if word_fre[i]>1:            # word_fre['虽远必']
            myList += [(i ,int(word_fre[i] ))]    # ('虽远必' ,285)

    print(len(myList))   # 11009
    print(myList[:10])

    '''
    [('想', 3354), ('喜欢', 1951), ('工作', 1488), ('谢谢', 1482), ('真的', 1310), ('我会', 1226), ('这是', 1194),,...]
    '''

    print(type(myList))   # <class 'list'>

    #用生成的数据 赋值给 myList 能生成词云  直接用生成的 myList 就不能生成词云 ！！！！
    # 这个是   word_fre[i]>100 产生的 数据



    # 如果用系统里产生的一部分数据 可以显示 词云图 ，但是要是用全部的  myList 数据就显示不出词云图

    #词云图的绘制
    wc= WordCloud()
    # wc=WC()

    # wc.add(yp_name,myList, shape='diamond',is_draw_out_of_bound=True)
    # print(wc)

    # wc.add(yp_name,myList, shape='arrow', word_size_range=[3, 50])
    # shape 词云图轮廓 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
    wc.add(yp_name,myList,mask_image='./word_cloud/aixin.jpg',is_draw_out_of_bound=False ,word_gap=5,width=300 ,height=400)

    # wc.add(yp_name,myList,is_draw_out_of_bound=False)

    wc.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-ChatGPT词云分析"))

    wc.render(path=HTML_file)                #HTML_file = 'myEcharts_词云图.html'
    # 浏览器显示生成的 china.html
    url = r"file:///" + currentPath + "/"+ HTML_file
    print(url)
    webbrowser.get('IE').open(url, new=1, autoraise=True)  # 用指定的浏览器打开 url 页面
    print('生成词云成功!')



    '''
    pyecharts提供了多种个性化配置方案，可以按需选择。
    
    # 系列名称，用于 tooltip 的显示，legend 的图例筛选。
    series_name: str,
    
    # 系列数据项，[(word1, count1), (word2, count2)]
    data_pair: Sequence,
    
    # 词云图轮廓，有 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star' 可选
    shape: str = "circle",
    
    # 自定义的图片（目前支持 jpg, jpeg, png, ico 的格式，其他的图片格式待测试）
    # 该参数支持：
    # 1、 base64 （需要补充 data 头）；
    # 2、本地文件路径（相对或者绝对路径都可以）
    # 注：如果使用了 mask_image 之后第一次渲染会出现空白的情况，再刷新一次就可以了（Echarts 的问题）
    # Echarts Issue: https://github.com/ecomfe/echarts-wordcloud/issues/74
    mask_image: types.Optional[str] = None,
    
    # 单词间隔
    word_gap: Numeric = 20,
    
    # 单词字体大小范围
    word_size_range=None,
    
    # 旋转单词角度
    rotate_step: Numeric = 45,
    
    # 距离左侧的距离
    pos_left: types.Optional[str] = None,
    
    # 距离顶部的距离
    pos_top: types.Optional[str] = None,
    
    # 距离右侧的距离
    pos_right: types.Optional[str] = None,
    
    # 距离底部的距离
    pos_bottom: types.Optional[str] = None,
    
    # 词云图的宽度
    width: types.Optional[str] = None,
    
    # 词云图的高度
    height: types.Optional[str] = None,
    
    # 允许词云图的数据展示在画布范围之外
    is_draw_out_of_bound: bool = False,
    
    # 提示框组件配置项，参考 `series_options.TooltipOpts`
    tooltip_opts: Union[opts.TooltipOpts, dict, None] = None,
    
    # 词云图文字的配置
    textstyle_opts: types.TextStyle = None,
    
    # 词云图文字阴影的范围
    emphasis_shadow_blur: types.Optional[types.Numeric] = None,
    
    # 词云图文字阴影的颜色
    emphasis_shadow_color: types.Optional[str] = None,
    和其他可视化库不一样，pyecharts支持链式调用。
    
    也就是说添加图表元素、修改图表配置，只需要简单的调用组件即可。
    
    
    
    '''
































#
# #####################################################################3
#
# #下面为用 ：pyecharts绘制词云图  不能生成词云图
# print(word_fre.index)
#
# # 将Series 数据 转换成 List类型
# myList=[]
# for   i  in word_fre.index:
#     if word_fre[i]>1:
#         myList += [(i ,int(word_fre[i] ))]
#
# print(len(myList))   # 13
# print(myList)
# print(type(myList))   # <class 'list'>
#
# #用生成的数据 赋值给 myList 能生成词云  直接用生成的 myList 就不能生成词云 ！！！！
# # 这个是   word_fre[i]>100 产生的 数据
# # myList = [('中国', 210), ('真的', 205), ('致敬', 191), ('记者', 161), ('哈哈哈', 126), ('这是', 126), ('真实', 126), ('五常', 116), ('太', 113), ('电影', 110), ('想', 104), ('队长', 102), ('卧槽', 102)]
#
#
# # 如果用系统里产生的一部分数据 可以显示 词云图 ，但是要是用全部的  myList 数据就显示不出词云图
# #词云图的绘制
# wc= WordCloud()
# wc.add(yp_name,myList, shape='diamond',is_draw_out_of_bound=True)
# wc.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-《战狼》词云分析"))
#
# wc.render(path=HTML_file)                #HTML_file = 'myEcharts_词云图.html'
# # 浏览器显示生成的 myEcharts_词云图.html
# url = r"file:///" + currentPath + "/"+ HTML_file
# print(url)
# webbrowser.get('IE').open(url, new=1, autoraise=True)  # 用指定的浏览器打开 url 页面
# print('生成词云成功!')


word_cloud(Word, HTML_file)

HTML_file = 'Question_词云图.html'
# Question, Answer
Word = 'Question'

word_cloud(Word, HTML_file)



HTML_file = 'Answer_词云图.html'
# Question, Answer
Word = 'Answer'

word_cloud(Word, HTML_file)