const app = getApp();
const { get, post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')
const record = wx.getRecorderManager();
const play = wx.createInnerAudioContext();

Page({
    data: {
        userInfo: {},
        chatList: [],
        inputValue: '',
        Question: '',
        Answer: 'Hello，我是文心一言',
        plcaceHolder: '请输入问题',
        // 用户注册信息
        UserID: 1001,
        UserName: '王小明',
        Gender: '男',
        Birthday: '2001-10-11',
        FaceImg: '/static/image/header.png',
        UserType: 3,
        MxType: 1, // 聊天模型类型 1: 文心  2: GPT
        MxName: '文心一言', // 默认聊天模型名称

        // 播放按钮状态
        play_image: "/images/diy-play.jpg",
        playing: false,
        recording: false, // 判断是否正在录音
        record_detail: '点击开始录音',
        record_duration: '00', // 显示录音的时间
        RecordFilePath: '',
        RecText: '',
        GPTAnswer: '',
        toView: '' // 用于控制滚动的目标元素
    },

    onShow() {
        this.setData({ userInfo: app.globalData.userInfo, is_currentpage: 0 });
     
    },

    onLoad() {
       this.getInfo();
        
    },

    // 滚动到底部
    scrollToBottom() {
        this.setData({ toView: 'toBottom' });
    },

    // 发布聊天消息
    publishChat() {
        const userMessage = {
            userId: '1001',
            Question: this.data.inputValue,
            FaceImg: this.data.FaceImg
        };

        // 更新聊天记录，将用户消息追加到聊天列表，并滚动到底部
        this.setData({
            chatList: [...this.data.chatList, userMessage],
            Question: this.data.inputValue,
            inputValue: this.data.inputValue,
            // inputValue: '',
            plcaceHolder: '请输入问题'
        }, () => {
            this.scrollToBottom();
        });

        // 调用 GPT2 接口获取 AI 的回复
        this.GPT2();
    },

    // 获取输入框的值
    getInputValue(event) {
        this.setData({ inputValue: event.detail.value });
    },

    // GPT2请求
    GPT2() {
        const that = this;
        
        const params = {
            question: that.data.Question,
            UserID: that.data.UserID,
            UserName: that.data.UserName,
            Gender: that.data.Gender,
            Birthday: that.data.Birthday,
            FaceImg: that.data.FaceImg,
            MxName: that.data.MxName
        };
        
        get(apiConfig.endpoints.gpt, params, {
            showLoading: true,
            loadingText: 'AI思考中...'
        }).then(res => {
            const botReply = {
                userId: '1002',
                Answer: res.message || res,
                MxName: that.data.MxName
            };

            // 将机器人的回复追加到聊天记录并滚动到底部
            that.setData({
                chatList: [...that.data.chatList, botReply],
                Answer: res.message || res
            }, () => {
                that.scrollToBottom();
            });
        }).catch(err => {
            const errorReply = {
                userId: '1002',
                Answer: "调用 chatGPT(文心一言) 出错！",
                MxName: that.data.MxName
            };

            that.setData({
                chatList: [...that.data.chatList, errorReply],
                Answer: "调用 chatGPT(文心一言) 出错！"
            }, () => {
                that.scrollToBottom();
            });
        });
    },

    // 开始或停止录音
    Record() {
        if (!this.data.recording) {
            this.startRecording();
        } else {
            this.stopRecording();
        }
    },

    // 开始录音
    startRecording() {
        this.setData({
            recording: true,
            record_detail: '录音中，点击停止',
            record_duration: '00:00' // 重置时长显示
        });

        let duration = 0;
        this.recordTimer = setInterval(() => {
            duration++;
            const minutes = String(Math.floor(duration / 60)).padStart(2, '0');
            const seconds = String(duration % 60).padStart(2, '0');
            this.setData({ record_duration: `${minutes}:${seconds}` });
        }, 1000);

        record.start({
            sampleRate: 16000,
            numberOfChannels: 1,
            encodeBitRate: 96000,
            format: 'mp3',
            frameSize: 50
        });
    },

    // 停止录音并保存路径
    stopRecording() {
        clearInterval(this.recordTimer);
        const that = this;
        record.stop();
        record.onStop((res) => {
            const duration = parseInt(res.duration / 1000);

            if (duration < 1 || duration > 20) {
                wx.showToast({ title: '录音时长不符合要求，请重新录音', icon: 'none', duration: 3000 });
                that.setData({ recording: false, record_detail: '点击开始录音' });
            } else {
                that.setData({
                    recording: false,
                    record_detail: '录音完成，点击转换',
                    RecordFilePath: res.tempFilePath,
                    record_duration: '' // 隐藏时长
                });

                wx.showToast({ title: '录音完成', icon: 'success' });
                console.log("this.RecordFilePath:",res.tempFilePath);
                this.saveRecording(res.tempFilePath);
                // 因为存在 需要执行2次 RecToText() 才能想刷新 百度AIP 转换的结果到 输入问题框里，故先执行一次
                // that.RecToText();
                // that.RecToText();
                console.log('====================== 1 ');
              that.RecToText();
              console.log('====================== 2 ');
              // that.RecToText();
              // console.log('====================== 3 ');
              
         }
           

        });

              

    },


     ////////////////////////////////////////////////////
    //  将微信小程序的录音临时文件，copy到小程序的内部存储空间：
    // //  FPath_wx = r'C:\Users\sumeng\AppData\Local\微信开发者工具......\usr\SoundRecordFile.mp3'
     saveRecording(tempFilePath) {
     
      const that = this ;
      const fs = wx.getFileSystemManager();
      const recordingFilePath = `${wx.env.USER_DATA_PATH}/SoundRecordFile.mp3`;
  
      fs.copyFile({
        srcPath: tempFilePath,
        destPath: recordingFilePath,
        success: () => {
          wx.showToast({
            title: '录音保存成功!',
            icon: 'success',
          });
         
          that.setData({recordingFilePath });
         
        },
        fail: (err) => {
          console.error('录音保存失败：', err);
          wx.showToast({
            title: '录音保存失败!',
            icon: 'none',
          });
        },
      });
    },

    /////////////////////////////////////////////////////
    // 转录音为文本并填充到输入框  
    // 存在问题：
    // （1）需要执行2次才能将 语音转换的文本发送到 输入文本框中: 已经解决
    // （2）登录后直接语音聊天会退到主页： 解决办法，启动是让页面处于 chatGPT 页面
    //  (3) 录音后，将MP3语音文件通过百度AIP 转换为text ,会跳转到登录页面，同时注销用户登录信息： 已经解决，通过调用 getInfo()
 
    RecToText() {
        const that = this;
        
        this.setData({
          userInfo: app.globalData.userInfo   ,
        })
      console.log("==============userInfo========== 22222")  ; 
      console.log(this.data.userInfo)  ;
       
        post(apiConfig.endpoints.recToText, {}, {
            showLoading: true,
            loadingText: '转换中...',
            header: {
                'content-type': 'application/x-www-form-urlencoded'
            }
        }).then(res => {
            // wx.hideToast();
            console.log("========================res.question========================");
            console.log("res.question:", res.question || res);
   
            that.setData({
                inputValue: res.question || res,
                RecordFilePath: "http://usr/SoundRecordFile.mp3",
            });
            wx.showToast({ title: '转换成功', icon: 'success' });
            console.log("转换成功(0)");
                         
            // 这里是关键，回到原页面
            wx.navigateBack({
                delta: 0, // 返回的页面数，如果 delta 大于现有页面数，则返回到首页
            });
        }).catch(error => {
            // wx.hideToast();
            console.error("转换失败：", error);
            // 错误已在 request.js 中处理 
            console.log("====================转换失败==========================");
            console.log("转换失败，响应数据无效(2)!!!");
        });
        // getInfo()：其功能是从login时保存在userInfo.txt中的登录用户信息恢复用户信息（因为页面刷新或跳转使得用户登录信息丢失）
        this.getInfo();
    },

    // 播放或暂停音频
    PlayorStop() {
        if (!this.data.RecordFilePath) {
            wx.showToast({ title: '没有录音文件', icon: 'none' });
            return;
        }

        if (this.data.playing) {
            this.setData({ play_image: "/images/diy-play.jpg", playing: false });
            play.pause();
        } else {
            this.setData({ play_image: "/images/diy-stop.jpg", playing: true });
            play.src = this.data.RecordFilePath;
            play.play();

            play.onEnded(() => {
                this.setData({
                    play_image: "/images/diy-play.jpg",
                    playing: false
                });
            });
        }
    },

    // 切换到“文心”模型
    switchToWenxin() {
        this.setData({
            MxType: 1,
            MxName: '文心一言'
        });
    },

    // 切换到“GPT”模型
    switchToGPT() {
        this.setData({
            MxType: 2,
            MxName: 'GPT'
        });
    },


////////////////////////////////////////////////////  2024-12-05 修改 Begin..................
// getInfo()：其功能是从login时保存在userInfo.txt中的登录用户信息恢复用户信息（因为页面刷新或跳转使得用户登录信息丢失）：
// //UserID: lines[0],          // 唯一账号，没用
// UserID: lines[1],          // 为用户Phone 唯一账号
// UserName: lines[2],        // 用户昵称 
// // PassWord: lines[3],     // 暂时没用
// Gender:lines[4],
// // RegisterTime: lines[5],     // 暂时没用
// Birthday: lines[6],     
// FaceImg: lines[7],
// UserType: lines[8]

// 实例如下：
// 32
// 13811111111
// 张一
// 123456
// 女
// 2024-03-05 20:11:19
// 2005-09-08
// /static/icon/FaceImg/72KF7Z73ghU752a64f430b4aeb8a1071884dd0cd6531.png
// 3
////////////////////////////////////////////////////////////////////////////////////////////////// 
//getInfo(): 其功能是从login时保存在userInfo.txt中的登录用户信息恢复用户信息（因为页面刷新或跳转使得用户登录信息丢失）
///////////////////////////////////////////////////////////////////////////////////////////////////
getInfo(){
    var that = this;
    wx.getFileSystemManager().readFile({
    filePath: `${wx.env.USER_DATA_PATH}/userInfo.txt`, // 文件路径
    encoding: 'utf8', // 编码方式，这里使用utf8编码读取文本文件
    success: function(res) {
          // 成功读取文件后，res.data 将包含文件的内容
          console.log('文件内容：', res.data);
          var lines = res.data.split('\n');
          ///////////////////////  测试读取到的信息
          console.log('文件内容 lines：', lines);
          console.log('文件内容 lines[0]：', lines[0]);
          console.log('文件内容 lines[1]：', lines[1]);
          console.log('文件内容 lines[2]：', lines[2]);
          // 更新用户登录信息：你可以在这里对文件内容进行进一步处理
          that.setData({
                // UserID: lines[0],           // 实际用户注册的 UserID 没用，故无需处理
                UserID: lines[1],              // 对于用户注册的 Phone 
                UserName: lines[2],
                // PassWord: lines[3],        // 暂时没用，故无需处理
                Gender:lines[4],
                // RegisterTime: lines[5],     // 暂时没用，故无需处理
                Birthday: lines[6],     
                FaceImg: lines[7],
                UserType: lines[8]
        });
        /////////////////////////////////////////// 仅仅用于测试
        console.log("userInfo3 UserName: ",that.data.UserName);
        console.log("userInfo3 FaceImg :",that.data.FaceImg);

        /////////////////////////////////////////////////////////////
        //重新更新 globalData.userInfo  因为页面刷新、跳转，丢失全局变量信息，故在获取登录信息后（从login时保存在userInfo.txt）重新更新全局变量信息
        ////////////////////////////////////////////////////////////
        app.globalData.userInfo = {
          nickName:that.data.Username,
          Phone:that.data.Phone,
          Password:that.data.Password,
          Gender:that.data. Gender,
          Birthday:that.data.Birthday,
          FaceImg:that.data.FaceImg,
          UserType:that.data.UserType
         };

    },  //  success  end


    fail: function(err) {
         // 读取文件失败时的回调函数
           console.error('读取 userInfo.txt 文件失败：', err);
      }

  }); // wx.getFileSystemManager().readFile  end

  },   // getInfo()  end

///////////////////////////////////////////////////    2024-12-05 修改 END .......................


});
