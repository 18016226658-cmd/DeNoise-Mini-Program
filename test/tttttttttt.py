
（1）微信小程序JS代码，点击某个按钮对一个音频文件进行人声和背景音乐进行分离，separateAudio是按钮的响应代码,
filePath小程序要传递给后端flask python的要分离的音频文件的 url，它保存在页面的变量audioPath中。
separateAudio代码如下：
separateAudio() {
    const that = this;
    wx.request({
        url: 'http://127.0.0.1:5000/api/separateAudio', // Flask后端接口地址
        method: "POST",
        timeout: 300000, // 设置超时时间为300秒
        data: JSON.stringify({ filePath: that.data.audioPath }), // 将数据转为 JSON 字符串
        header: {
            'content-type': 'application/json' // 改为 JSON 格式
        },
        success: function(res)
        {
            console.log('1 success ========== res:', res);
            wx.showToast({
                title: '分离成功',
                icon: 'success'
            });

        },
        fail: function(err)
        {
            console.log('2 Error 分离失败===========err:', err);
            wx.showToast({
                title: '分离失败',
                icon: 'none'
            });
        }
    });
},
在小程序端运行：
既没有显示：1 success ========== res
也没有显示：2 Error 分离失败===========err:
页面无故刷新，显示
无效的 app.json permission["scope.userInfo"]
[system] WeChatLib: 3.3.3 (2024.1.23 17:19:51)
[system] Subpackages: N/A
[system] LazyCodeLoading: false
[pages/AudioSep/AudioSep] [Deprecation] '<audio>' is deprecated. Please use 'wx.createInnerAudioContext' instead.
[system] Launch Time: 880 ms
无效的 app.json permission["scope.userInfo"]

（2）下面是flask 的 url: 'http://127.0.0.1:5000/api/separateAudio' 路由代码，其中filePath是小程序传递过来的要分离的音频文件的访问 url，
api/separateAudio路由代码如下：
@app.route('/api/separateAudio', methods=['POST'])
def separateAudio():
    try:
        data = request.get_json()  # 解析 JSON 数据
        file_path = data.get("filePath")
        if not file_path:
            return jsonify({"error": "No file path provided"}), 400

        # 解析文件路径（这里假设 filePath 是相对于某个基础路径的）
        # 注意：这里假设 filePath 是服务器上的相对路径，而不是小程序中的路径
        # 你需要根据实际情况调整这部分逻辑
        WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a/'
        tt = file_path[7:]
        input_file = WX_TEMP_DIR + tt
        if not os.path.exists(input_file):
            return jsonify({"error": "File not found"}), 404

        output_dir = r'D:\WxMinPro\Audio\output'
        run_demucs(input_file, output_dir)
        result = {"success": 1, "files": output_dir}
        print(result)
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
运行这一步：显示：{'success': 1, 'files': 'D:\\WxMinPro\\Audio\\output'}

（3）这是利用demucs库，将input_file音频文件进行人声和背景音乐进行分离的代码，分离结果保存在output_dir中，
run_demucs代码如下：
def run_demucs(input_file, output_dir, model="htdemucs", device="cpu"):    #mdx_extra 和 htdemucs
    command = [
        "demucs",                         #"python", "-m", "demucs.separate",
        "-n", model,
        "--out", output_dir,             #  htdemucs  htdemucs_6s  mdx  mdx_extra
        "--device", device ,             # 如果有GPU 可以选择 cuda
        input_file
    ]

    try:
        result = subprocess.run(command)   # 显示进度条
        print("Demucs ran successfully!")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running Demucs:", e)
        print("Output:", e.stdout)
        print("Error Output:", e.stderr)
运行这一步显示：Demucs ran successfully!

（4）小程序运行中，后台能对filePath音频文件进行分离，但为什么分离结束后，小程序端既不会输出 console.log('1 success ========== res:', res); 也不会输出console.log('2 Error 分离失败===========err:', err);
同时页面会无故刷新，所有页面变量都被清空，问题出在什么地方，怎么修改响应的代码？















# （1）微信小程序JS代码，点击某个按钮对一个音频文件进行人声和背景音乐进行分离，separateAudio是按钮的响应代码,
# filePath小程序要传递给后端flask python的要分离的音频文件的 url，它保存在页面的变量audioPath中。separateAudio代码如下：
# separateAudio() {
#     const that = this;
#     wx.request({
#         url: 'http://127.0.0.1:5000/api/separateAudio', // Flask后端接口地址
#         method: "POST",
#         data: {
#             filePath: that.data.audioPath // 将数据传给后端
#         },
#         header: {
#             'content-type': 'application/x-www-form-urlencoded'
#         },
#         success: function(res)
#         {
#             console.log('1 success ========== res:', res);
#             wx.showToast({
#                 title: '分离成功',
#                 icon: 'success'
#             });
#
#         },
#         fail: function(err)
#         {
#             console.log('2 Error 分离失败===========err:', err);
#             wx.showToast({
#                 title: '分离失败',
#                 icon: 'none'
#             });
#         }
#     });
# },
#
# （2）下面是flask 的 url: 'http://127.0.0.1:5000/api/separateAudio' 路由代码，其中filePath是小程序传递过来的要分离的音频文件的访问 url，api/separateAudio路由代码如下：
# @app.route('/api/separateAudio', methods=['POST'])
# def separateAudio():
#     file = request.form.get("filePath")
#     tt = file[7:]
#     # WX_TEMP_DIR 是微信小程序临时文件夹主目录
#     WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a/'
#     input_file = WX_TEMP_DIR +  tt
#     output_dir = r'D:\WxMinPro\Audio\output'
#     t1=time.time()
#     run_demucs(input_file, output_dir)
#     t2=time.time()
#     print('共用时：'+str(int(t2-t1))+'秒')
#     result = {"success":1,"files":output_dir}
#     return jsonify(result)
#
# （3）这是利用demucs库，将input_file音频文件进行人声和背景音乐进行分离的代码，分离结果保存在output_dir中，run_demucs代码如下：
# def run_demucs(input_file, output_dir, model="htdemucs", device="cpu"):    #mdx_extra 和 htdemucs
#     command = [
#         "demucs",                         #"python", "-m", "demucs.separate",
#         "-n", model,
#         "--out", output_dir,             #  htdemucs  htdemucs_6s  mdx  mdx_extra
#         "--device", device ,             # 如果有GPU 可以选择 cuda
#         input_file
#     ]
#
#     try:
#         result = subprocess.run(command)   # 显示进度条
#         print("Demucs ran successfully!")
#         print("Output:", result.stdout)
#     except subprocess.CalledProcessError as e:
#         print("Error running Demucs:", e)
#         print("Output:", e.stdout)
#         print("Error Output:", e.stderr)
#
# （4）小程序运行中，后台能对filePath音频文件进行分离，但为什么不会输出 console.log('1 success ========== res:', res); 和console.log('2 Error 分离失败===========err:', err);
# 同时页面会无故刷新，所有页面变量都被清空，问题出在什么地方，怎么修改响应的代码？