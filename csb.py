请生成一个微信小程序页面，页面功能是让用户输入三个参数，提交到后台flask Python程序中将三个参数保存MySQL数据表csb中。要求微信小程序的输入界面要美丽。
为了创建一个微信小程序页面，该页面需要用户输入三个参数并提交到后台的Flask Python程序，最终将这三个参数保存到MySQL数据库表csb中，我们可以按照以下步骤进行。同时，为了确保输入界面美观，我们可以利用微信小程序提供的组件和样式。

步骤 1: 设置Flask后端

首先，我们需要设置一个Flask后端来接收微信小程序的请求，并将数据保存到MySQL数据库中。

【python】
 # app.py (Flask 后端)
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL数据库配置
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 连接到MySQL数据库
connection = pymysql.connect(**db_config)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    param1 = data.get('param1')
    param2 = data.get('param2')
    param3 = data.get('param3')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO csb (param1, param2, param3) VALUES (%s, %s, %s)"
            cursor.execute(sql, (param1, param2, param3))
        connection.commit()
        return jsonify({'message': 'Data submitted successfully!'}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

确保你的MySQL数据库中已经创建了csb表，并且包含了param1,param2,param3这三个字段。

步骤 2: 创建微信小程序前端

接下来，我们创建微信小程序的前端页面，让用户输入三个参数并提交。

1. 创建页面结构

在pages/submit/submit.wxml中：

【xml】
 <view class="container">
  <view class="input-group">
    <label>参数1</label>
    <input type="text" bindinput="onParam1Input" placeholder="请输入参数1" />
  </view>
  <view class="input-group">
    <label>参数2</label>
    <input type="text" bindinput="onParam2Input" placeholder="请输入参数2" />
  </view>
  <view class="input-group">
    <label>参数3</label>
    <input type="text" bindinput="onParam3Input" placeholder="请输入参数3" />
  </view>
  <button type="primary" bindtap="onSubmit">提交</button>
</view>

2. 添加样式

在pages/submit/submit.wxss中：

【css】
 .container {
  padding: 20px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #1aad19;
  color: white;
  border: none;
  border-radius: 4px;
}

3. 编写页面逻辑

在pages/submit/submit.js中：

【javascript】
 Page({
  data: {
    param1: '',
    param2: '',
    param3: '',
  },

  onParam1Input: function(e) {
    this.setData({
      param1: e.detail.value
    });
  },

  onParam2Input: function(e) {
    this.setData({
      param2: e.detail.value
    });
  },

  onParam3Input: function(e) {
    this.setData({
      param3: e.detail.value
    });
  },

  onSubmit: function() {
    const { param1, param2, param3 } = this.data;
    wx.request({
      url: 'http://your_flask_server_address/submit', // 替换为你的Flask服务器地址
      method: 'POST',
      data: {
        param1: param1,
        param2: param2,
        param3: param3,
      },
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.data.message) {
          wx.showToast({
            title: '提交成功',
            icon: 'success',
            duration: 2000
          });
        } else {
          wx.showToast({
            title: '提交失败：' + res.data.error,
            icon: 'none',
            duration: 2000
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误',
          icon: 'none',
          duration: 2000
        });
      }
    });
  }
});

4. 配置页面路径

在app.json中添加页面路径配置：

【json】
 {
  "pages": [
    "pages/submit/submit"
    // 其他页面路径...
  ],
  "window": {
    "navigationBarBackgroundColor": "#ffffff",
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "参数提交"
  }
}

步骤 3: 运行和测试

  1. 确保你的Flask后端正在运行，并且可以通过网络访问。

  2. 使用微信开发者工具打开你的微信小程序项目。

  3. 编译并运行小程序，访问你创建的提交页面。

  4. 输入三个参数并提交，检查是否成功保存到MySQL数据库中。

请注意，由于微信小程序的安全策略，你可能需要在微信公众平台上配置你的服务器域名，以便小程序能够正常发送网络请求。同时，确保你的Flask后端支持CORS（跨源资源共享），以便接受来自微信小程序的请求。如果Flask后端和微信小程序不在同一个域下，你可能需要安装并配置Flask-CORS扩展。