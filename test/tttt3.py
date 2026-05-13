import mutagen

# 假设音频文件的路径是 'path/to/your/audiofile.mp3'
base_dir =r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a\usr\Audio'

file_path =base_dir +'/6W3MEnyE02EGe4e19eea79b944154ecd956a82ec714c.ogg'

# 使用 mutagen.File 来打开音频文件
audio_file = mutagen.File(file_path, easy=True)

# 提取标题、艺术家和专辑名
title = audio_file.get('title', [None])[0]  # 'title' 标签可能不存在，所以使用列表和 [0] 来获取值或 None
artist = audio_file.get('artist', [None])[0]
album = audio_file.get('album', [None])[0]

# 打印提取的信息
print(f"Title: {title}")
print(f"Artist: {artist}")
print(f"Album: {album}")




# // 调用api接口，访问GPT2函数
#
# wx.request({   // 将聊天的问题（Questio），作为参数附在地址后面
#     url: 'http://127.0.0.1:5000/api/GPT?question=' + that.data.Question + '&UserID=' + that.data.UserID + '&UserName=' +
#          that.data.UserName + '&Gender=' + that.data.Gender + '&Birthday=' + that.data.Birthday + '&FaceImg=' + that.data.FaceImg,
#
#     method: 'GET',
#     success: res = > {    // 根据调用chatGPT的结果（res.data.message）修改答案（Answer）
#         that.setData({Answer: res.data.message});
#     },
#     fail: err = > {
#         that.setData({Answer: "调用 chatGPT 出错！"});
#
#     }
# });















#
# import openai
# import os
# def chatGPT(question):
#
#     try:
#         # 指定 OpenAI API 的密钥
#         openai.api_key = 'sk-rGKg0Qm1AxpJIB*******BlbkFJS0r2PJ5GBMrCQzldJwsM'
#
#         os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
#         os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"
#
#         q = [{"role": "user", "content": question}]
#
#         rsp = openai.ChatCompletion.create(
#           model="gpt-3.5-turbo-0301",
#           messages=q
#         )
#         msg = rsp.get("choices")[0]["message"]["content"]
#     except:
#         msg ="调用openAI出错，不能为你提供chat服务！"
#     return msg














#
# // 柱状图 点击事件 聊天数量按照性别点分布情况 (bar)
# barA(){
#     console.log("聊天数量按照性别分布情况（bar1)")
#     option = {
#              title: {
#                  text: '聊天数量按性别分布',
#                  left: 'center',
#              },
#              xAxis: {
#                         type: 'category',
#                         data :this.data.Xb_Data1,
#                         name :'性别' ,                //坐标轴名称
#                         nameLocation :'center' ,     //坐标轴名称显示位置
#                         nameTextStyle :{} ,          //坐标轴名称的文字样式
#                         nameGap :30,                 //坐标轴名称与轴线之间的距离
#                      },
#             yAxis: {
#                 type: 'value'
#             },
#
#             series: [{
#                 label: {                            //数据显示
#                     show: true,
#                     color :'inherit',
#                     position :'top',
#                     fontSize: 10,
#                  },
#
#                 data: this.data.Xb_Data2,
#                 type: 'bar',
#                 showBackground: true,
#                 backgroundStyle: {
#                     color: 'rgba(180, 180, 180, 0.2)'
#                 }
#               },
#             ]
#     }
#     chart2.setOption(option ,true);
#     this.setData({
#         index :4,
#     })
#
#     },
#
#
# import * as echarts from '../../ec-canvas/echarts';    // 引入echarts图表
# var option=[];                                         //图表配置项声明
# let chart2 = null;                                     // 初始化图表函数  开始
# function initChart2(canvas, width, height, dpr) {
#     chart2 = echarts.init(canvas, null, {
#         width: width,
#         height: height,
#         devicePixelRatio: dpr
#      })
#     canvas.setChart(chart2)
#     return chart2;
# }
#
# chart2.setOption(option ,true);
# this.setData({
#         index :4,
#     })
#
#
# # Flask后台路由函数统计性别分布情况
# comments = pd.read_excel(r'./Dialo.xlsx')
# num = comments['Gender'].value_counts().sort_index()
# X4 = num.index
# Y4 = []
# for k in range(len(X4)):
#     Y4.append(num[X4[k]])    # Y4 =[32232, 16160]
# X4 = list(X4)                # X4 =['女', '男']
#
# # Flask后台将性别分析结果返回给微信小程序
# "user_Data41": X4,
# "user_Data42": Y4,
#
#
# #微信小程序接收Flask后台数据
# success(res){
#     that.setData({
#         Xb_Data1: res.data.user_Data41,
#         Xb_Data2: res.data.user_Data42,
#     })
# }
#
#
#
# # 聊天情感分析
# from snownlp import SnowNLP
# line = open("zhddline_1000.txt", "r", encoding='utf8').readlines()
# sentimentslist = []
# for i in line:
#     s = SnowNLP(i)
#     sentimentslist.append(s.sentiments)
#
# # 区间转换为[-0.5, 0.5]
# result = []
# i = 0
# while i < len(sentimentslist):
#     result.append(sentimentslist[i] - 0.5)
#     i = i + 1
#
# X6 = np.arange(0, len(result), 1)
# Y6 = result
#
# x61 = list(map(int, X6))
# y62 = Y6
#
#
#
#
# # python随机生成姓名
#     # 姓氏列表
#     surnames = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何',
#                 '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏',
#                 '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史',
#                 '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅',
#                 '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹','欧阳','上官','诸葛']
#     # 男人名字列表
#     Man_names = ['小', '明', '强', '亮', '敏', '洁', '晓', '新', '建', '国', '军', '峰', '涛', '雷', '刚', '磊', '亚', '梦', '龙', '中', '涛',
#                  '桃', '民', '山', '凌', '阿', '天', '理', '宏', '高', '争', '正']
#
#     # 女人名字列表
#     Wen_names = ['小', '红', '丽', '美', '娜', '玲', '晓', '燕', '露', '芳', '艳', '静', '婷', '敏', '洁', '雅', '雪', '琳', '晓', '兰', '莉',
#                  '梦', '英', '妹', '靓', '媚', '琳', '妞', '茜', '溪']
#     # 男人姓名列表和女人姓名列表
#     Man = []
#     Wenmen = []
#
#     # 随机生成40个男性姓名
#     for i in range(30):
#         Man_surname = random.choice(surnames)            # 随机选一个姓
#         Man_name = ''.join(random.sample(Man_names, 2))  # 随机选两个用空字符串连接
#         Man.append(Man_surname + Man_name)               # 姓+男姓名
#
#     # 随机生成60个女性姓名
#     for i in range(40):
#         Wen_surname = random.choice(surnames)            # 随机选一个姓
#         Wen_name = ''.join(random.sample(Wen_names, 2))  # 随机选两个用空字符串连接
#         Wenmen.append(Wen_surname + Wen_name)            # 姓+女性名
#
#
#     random.choice(Man)                                   # 随机选择一个男姓姓名
#     random.choice(Wenmen)                                # 随机选择一个女姓姓名