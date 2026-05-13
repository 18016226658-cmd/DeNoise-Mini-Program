// pages/soundRecord/soundRecord.js
const { post, uploadFile } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

// Page({
//   /**
//   * 页面的初始数据
//   */
//  data: {
//    isRecording: false,
//    recordedFilePath: '',
//    audioCtx: null,
//  },

//  startRecording: function() {
//    const that = this;
//    wx.startRecord({
//      success: function(res) {
//        that.setData({
//          isRecording: true
//        });
//      }
//    });
//  },

//  stopRecording: function() {
//    const that = this;
//    wx.stopRecord({
//      success: function(res) {
//        that.setData({
//          isRecording: false,
//          recordedFilePath: res.tempFilePath
//        });
       
//        // 创建音频上下文
//        that.setData({
//          audioCtx: wx.createInnerAudioContext()
//        });
       
//        // 播放录制的音频
//        that.playRecordedAudio();
//      }
//    });
//  },

//  playRecordedAudio: function() {
//    const audioCtx = this.data.audioCtx;
//    if (audioCtx) {
//      audioCtx.src = this.data.recordedFilePath;
//      audioCtx.onPlay(() => {
//        console.log('开始播放');
//      });
//      audioCtx.onError((res) => {
//        console.log(res.errMsg);
//        console.log(res.errCode);
//      });
//      audioCtx.play();
//    }
//  },



//  /**
//   * 生命周期函数--监听页面加载
//   */
//  onLoad(options) {

//  },

//  /**
//   * 生命周期函数--监听页面初次渲染完成
//   */
//  onReady() {

//  },

//  /**
//   * 生命周期函数--监听页面显示
//   */
//  onShow() {

//  },

//  /**
//   * 生命周期函数--监听页面隐藏
//   */
//  onHide() {

//  },

//  /**
//   * 生命周期函数--监听页面卸载
//   */
//  onUnload() {

//  },

//  /**
//   * 页面相关事件处理函数--监听用户下拉动作
//   */
//  onPullDownRefresh() {

//  },

//  /**
//   * 页面上拉触底事件的处理函数
//   */
//  onReachBottom() {

//  },

//  /**
//   * 用户点击右上角分享
//   */
//  onShareAppMessage() {

//  },

// })

///////////////////////////////////////////////////////////////
// Page({
//   data: {
//     isRecording: false,
//     recordedFilePath: '',
//     audioCtx: null,
//     tmp: '',
//   },

//   startRecording: function() {
//     const that = this;
//     console.log('开始...');
//     wx.startRecord({
      
//       success: function(res) {
//         that.setData({
        
//           isRecording: true,
//           tmp:res.tempFilePath,
          
//         });
//         console.log('End...');
//         console.log(res.tempFilePath);
//         console.log(that.data.tmp);
//       }
//     });
//   },

//   stopRecording: function() {
//     const that = this;
//     console.log('开始 stopRecording...');
   

//     wx.stopRecord({
//       success: function(res) {
//         console.log(res);
//         console.log(res.tempFilePath);
//         console.log(that.data.tmp);
//         that.setData({
//           isRecording: false,
//           // recordedFilePath: res.tempFilePath
//           recordedFilePath: that.data.tmp
//         });
        
//         // 创建音频上下文
//         that.setData({
//           audioCtx: wx.createInnerAudioContext()
//         });
//         console.log(that.data.audioCtx);
//         // 播放录制的音频
//         that.playRecordedAudio();
//       }
//     });
//   },

//   playRecordedAudio: function() {
//     const audioCtx = this.data.audioCtx;
//     if (audioCtx) {
//       // audioCtx.src = this.data.recordedFilePath;
//       audioCtx.src = this.data.tmp;
//       console.log(audioCtx.src);
//       audioCtx.onPlay(() => {
//         console.log('开始播放');
//       });
//       audioCtx.onError((res) => {
//         console.log(res.errMsg);
//         console.log(res.errCode);
//       });
//       audioCtx.play();
//     }
//   }
// });



// // pages/audio/audio.js
// Page({
//   data: {
//     isRecording: false,
//     recordingTime: 0,
//     maxRecordingTime: 60, // 最大录音时长为60秒
//     recordedFilePath: '',
//     audioCtx: null,
//   },

//   startRecording: function() {
//     const that = this;
//     wx.startRecord({
//       success: function(res) {
//         that.setData({
//           isRecording: true,
//           recordingTime: 0
//         });
        
//         // 开始计时
//         that.timer = setInterval(function() {
//           that.setData({
//             recordingTime: that.data.recordingTime + 1
//           });
//           if (that.data.recordingTime >= that.data.maxRecordingTime) {
//             that.stopRecording();
//           }
//         }, 1000);
//       }
//     });
//   },

//   stopRecording: function() {
//     clearInterval(this.timer);
//     const that = this;
//     wx.stopRecord({
//       success: function(res) {
//         that.setData({
//           isRecording: false,
//           recordedFilePath: res.tempFilePath
//         });
        
//         // 创建音频上下文
//         that.setData({
//           audioCtx: wx.createInnerAudioContext()
//         });
        
//         // 播放录制的音频
//         that.playRecordedAudio();
//       }
//     });
//   },

//   playRecordedAudio: function() {
//     const audioCtx = this.data.audioCtx;
//     if (audioCtx) {
//       audioCtx.src = this.data.recordedFilePath;
//       audioCtx.onPlay(() => {
//         console.log('开始播放');
//       });
//       audioCtx.onError((res) => {
//         console.log(res.errMsg);
//         console.log(res.errCode);
//       });
//       audioCtx.play();
//     }
//   }
// });


// 创建record对象
var record = wx.getRecorderManager();
// 创建play对象
var play = wx.createInnerAudioContext();
 
Page({
 
  /**
   * 页面的初始数据
   */
  data: {
    //播放按钮
    play_image:"/images/diy-play.jpg",
    //判断是否在播放
    playing:false,
    //判断是否为当前页面
    is_currentpage:0,
    //判断录音进行至哪个状态，0为未录音，1为正在录音，2为完成录音
    record_type:0,
    //录音状态描述
    record_detail:'点击图标开始录音',
    //保存录音文件
    record_content:'',
    //保存录音长度
    record_duration:'00',
    //当前播放进度
    record_current: '00',
    //播放条占比
    record_percent: 0,
    
    //计时器时间，使暂停后可重新从该时间播放
    timer_time: 0 ,
    //保存录音文件路径
    RecordFilePath: '',
    //识别的文本
    RecText :'' ,
    GPTAnswer:  ''
  },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.setData({
      is_currentpage:0
    })
  },
 
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    //防止用户在切换页面后继续播放
    this.setData({
      is_currentpage:1
    })
  },
  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    //防止用户在切换页面后继续播放
    this.setData({
      is_currentpage:1
    })
  },
  //录音
  Record: function(res){
    //判断是否在播放音频
    if(this.data.playing)
    {
      //若正在播放音频则无法录音
    }
    else
    {
      //判断录音状态  0：录音时间过长  录音时间过短   准备重新录音    1：正在录音       2：
      if(this.data.record_type == 0 || this.data.record_type == 2)
      {
        //切换录音状态
        this.setData({
          record_type: 1,
          record_detail: '正在录音',
        })
        var that = this
        //声明设置对象
        var options = {
          sampleRate: 16000,
          numberOfChannels: 1,
          encodeBitRate: 96000,
          format: 'mp3',
          // format: 'pcm',
          frameSize: 50
        }
        //开始录音
        record.start(options)
      }
      else if(this.data.record_type == 1)
      {
        //停止录音
        record.stop();
        
        var that = this
        record.onStop((ress) => {
          //获取整数化的录音时长
          var duration = parseInt(ress.duration/1000)
          console.log(parseInt(ress.duration/1000))
          //防止录音时间过短
          // if(ress.duration<3000){
          if(ress.duration<1000){
            wx.showToast({
              title: '录音时间太短，请重新录音',
              icon: 'none',
              duration: 3000
            })
            that.setData({
              record_type:0,
              record_detail:'点击图标开始录音'
            })
          }
          // else if(ress.duration>30000)
          else if(ress.duration>20000)
          {
            //防止录音时间过长
            wx.showToast({
              title: '录音时间过长，请重新录音',
              icon: 'none',
              duration: 3000
            })
            that.setData({
              record_type:0,
              record_detail:'点击图标开始录音'
            })
          }
          else{
            //判断录音时长是否低于十秒，若低于十秒则加上前置0
            if(duration < 10)   
            {
              var t = duration
              duration = '0'+t
            }
            that.setData({
              record_type: 2,
              record_detail: '点击图标重新录音',
              //储存录音文件
              record_content: ress.tempFilePath,
              // 保存文件到本地
              ///////////////////////////////////////////
             
              //储存录音长度
              record_duration: duration,
              //重置播放进度
              record_current: '00',
              //重置播放条占比
              record_percent: 0,
              //重置计时器时间
              timer_time:0
            })
            
          }
          ///////////////////////////////////////////
          // 以前这里使用 wx.saveFile 将录音永久保存到本地，
          // 但大文件会触发“超过本地存储上限”的错误，且真机/工具格式不完全一致。
          // 实际播放和上传都可以直接使用临时路径，不需要额外保存。
          // 因此这里改为直接使用临时文件路径：
          that.setData({
            RecordFilePath: ress.tempFilePath   // 直接使用录音生成的临时路径
          })

          // 上传录音到服务器（如需）
          uploadFile(
            ress.tempFilePath,
            '/api/SoundRecordFile',  // 后端已实现该端点
            { method: 'POST' },
            { name: 'file' }
          ).then(res => {
            console.log(res)
            console.log("上传成功")
            // 上传成功后返回上一页（如果你希望留在本页，可以去掉 navigateBack）
            wx.navigateBack({
              delta: 0
            });
          }).catch(err => {
            console.error("上传失败：", err)
            wx.showToast({
              title: '上传失败',
              icon: 'none'
            })
          })

        })
      }
    }
  },

  // 将录音文件转换为 text文本文件
  RecToText: function(){
    // 当前项目尚未对接语音转文字后台接口，为避免报错，这里先给出友好提示
    wx.showToast({
      title: '语音转文字功能暂未开通',
      icon: 'none',
      duration: 2000
    })
      },
        
   /////////////////////////////////////////// 

  //播放或暂停
  PlayorStop: function(){
    //判断是否在录音以及未录音
    console.log(this.data.record_type);
    if(this.data.record_type != 2)
    {
      //在录音或未录音则无法播放音频
      console.log('在录音或未录音则无法播放音频');
    }
    else if(this.data.record_type == 2)
    {
      var that = this
      //判断是否在播放
      console.log('判断是否在播放');
      console.log(that.data.playing);
      if(that.data.playing){
        that.setData({
          //改变播放图标
          play_image:"/images/diy-play.jpg",
          //将播放状态设置为否
          playing:false
        })
        //暂停播放
        play.pause()
        //暂停计时器
        clearInterval(t)
        return;
      }
      that.setData({
        //更改播放图标
        play_image:"/images/diy-stop.jpg",
        //将播放状态设置为是
        playing:true
      });
      play.onError((res) => {
        // 播放音频失败的回调
        console.log('播放音频失败的回调')
        console.log(res)
      })
      //设置播放的录音链接，可以是录音的临时路径或已上传至服务器的链接
      console.log('播放的录音链接')
      console.log(that.data.record_content)
      // 直接使用本次录音的临时路径进行播放，避免依赖 saveFile 带来的存储限制
      play.src = that.data.RecordFilePath || that.data.record_content
      //开始播放
      play.play();
      //设置计时器
      var t = setInterval(function(){
        //判断是否结束播放以及是否在当前页面
        if(that.data.record_duration == that.data.timer_time|| that.data.is_currentpage == 1)
        {
          //清空计时器
          clearInterval(t)
          that.setData({
            //重置播放数值
            play_image:"/images/diy-play.jpg",
            playing:false,
            record_percent: 0,
            record_current: '00',
            timer_time:0
          });      
          console.log("结束")
          //结束播放
          play.stop()
        }
        //判断是否暂停
        else if(that.data.playing == false)
        {
          //清空计时器，达到暂停效果
          clearInterval(t)
        }
        else
        {
          //若当前时间小于10，则加上前置0
          if(that.data.timer_time < 10)
          {
            var current = '0'+(that.data.timer_time+1)
          }
          else
          {
            var current = that.data.timer_time+1
          }
          //获得当前播放条长度
          var long = (that.data.timer_time+1)/that.data.record_duration*80
          //当前计时器时间加1
          var time = that.data.timer_time+1
          that.setData({
            record_percent: long,
            record_current: current,
            timer_time: time
          })
        }
      }, 1000);
    }
    
  },
})
