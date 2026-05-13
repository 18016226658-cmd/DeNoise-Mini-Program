import pymysql
import datetime

# 连接数据库
connect = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',  # 数据库用户名
    passwd='123456',  # 密码
    db='audio',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()
try:
    UserID = "13222222222"
    myUserName = "222"
    myGender = "女"
    myBirthday = "2002-10-10"
    mySepTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    myMxName = "htdemucs"
    myAudioName = "蒋倩如 - 小河淌水"
    myExtension = "ogg"
    myFileSize = 5.85
    myDuration = 279.69

    sql = """
    INSERT INTO sepaudiotable (
        UserID, UserName, Gender, Birthday, SepTime, MxName, AudioName, Extension, FileSize, Duration
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    data = (
    UserID, myUserName, myGender, myBirthday, mySepTime, myMxName, myAudioName, myExtension, myFileSize, myDuration)
    cursor.execute(sql, data)
    # 提交事务
    connect.commit()
    print('成功保存分离记录')
except Exception as e:
    print(f"保存分离记录表出错: {e}")
finally:
    # 关闭游标和连接
    cursor.close()
    connect.close()

# import pymysql
# import datetime
# # 连接数据库
# connect = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',  # 数据库用户名
#     passwd='123456',  # 密码
#     db='audio',
#     charset='utf8'
# )
#
# # 获取游标
# cursor = connect.cursor()
# try:
#     UserID = "13222222222"
#     myUserName = "222"
#     myGender = "女"
#     myBirthday = "2002-10-10"
#     mySepTime = str(datetime.datetime.now())
#     myMxName = "htdemucs"
#     myAudioName = "蒋倩如 - 小河淌水"
#     myExtension = "ogg"
#     myFileSize = 5.85
#     myDuration = 279.69
#
#     sql = "INSERT INTO sepaudiotable ( UserID, UserName, Gender, Birthday,SepTime,MxName, AudioName,Extension,FileSize,Duration) VALUES ('%s', '%s', %s,  '%s', '%s','%s' ,'%s' ,'%s','%s','%s')"
#     print(sql)
#     data = (UserID, myUserName, myGender, myBirthday, mySepTime, myMxName, myAudioName, myExtension, myFileSize,myDuration)
#     print(data)
#     cursor.execute(sql % data)
#     # 提交事务（对于大多数数据库操作是必需的）
#     connect.commit()
#     cursor.close()
#     connect.close()
#     print('成功保存分离记录')
# except Exception as e:
#     print(f"保存分离记录表出错:{e}")

# 程序运行结果输出如下：
# INSERT INTO sepaudiotable ( UserID, UserName, Gender, Birthday,SepTime,MxName, AudioName,Extension,FileSize,Duration) VALUES ('%s', '%s', %s,  '%s', '%s','%s' ,'%s' ,'%s','%s','%s')
# ('13222222222', '222', '女', '2002-10-10', '2025-01-05 20:37:20.617747', 'htdemucs', '蒋倩如 - 小河淌水', 'ogg', 5.85, 279.69)
# 保存分离记录表出错:(1054, "Unknown column '女' in 'field list'")




# INSERT INTO sepaudiotable(UserID, UserName, Gender, Birthday, SepTime, MxName, AudioName, Extension, FileSize, Duration) VALUES('%s', '%s', % s, '%s', '%s', '%s', '%s', '%.2f', '%.2f')
# ('13222222222', '222', '女', '2002-10-10', '2025-01-05 19:43:52.621386', 'htdemucs', '蒋倩如 - 小河淌水', 'ogg', 5.85,279.69)
# 保存分离记录表出错:must be real number, not str
#
# 数据表sepaudiotable 对应的字段类型如下
# UserID, UserName, Gender, Birthday,SepTime, MxName, AudioName,Extension,FileSize,Duration
# varchar,varchar,  varchar,date,    datetime,varchar,varchar,  varchar,  double,  double