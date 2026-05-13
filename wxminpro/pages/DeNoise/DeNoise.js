// ============================================
// 音频降噪页面
// ============================================
// 功能：音频文件降噪处理，使用巴特沃斯滤波器算法去除噪音
// 路径：pages/DeNoise/DeNoise.js
// 说明：支持选择音频文件、上传到服务器、获取音频信息、执行降噪、播放对比、下载降噪文件

// ============================================
// 1. 导入依赖
// ============================================
const apiConfig = require('../../config/api.js')  // 导入API配置

// ============================================
// 2. 页面定义
// ============================================
Page({
  /**
   * 页面的初始数据
   */
  data: {
    // ============================================
    // 音频文件相关
    // ============================================
    audioPath: '',          // 原始音频文件路径（用于播放）
    AudioFilePath: '',      // 音频文件路径（备用）
    filePath: '',           // 文件临时路径
    fileSize: '0.00',       // 文件大小（MB）
    duration: '00:00:00',   // 音频时长（格式化显示）
    filename: '',           // 服务器返回的唯一文件名
    extension: '',          // 文件扩展名（wav/mp3/ogg等）
    DeNoisePath: '',        // 降噪后的音频文件路径（用于播放）
    DeNoiseFilename: '',    // 降噪后的文件名（用于下载）
    orgFileName: '',        // 用户本地的原始文件名（带扩展名）
    
    // ============================================
    // 降噪状态相关
    // ============================================
    DeNoisedOK: '0',        // 降噪完成标记（'0'=未完成，'1'=已完成）
    title: '',              // 音频标题（从元数据获取）
    artist: '',             // 艺术家（从元数据获取）
    album: '',              // 专辑（从元数据获取）
    
    // ============================================
    // 音频播放相关
    // ============================================
    audioContext: null,     // 音频播放上下文对象
    isPlaying: false,       // 是否正在播放
    Mduration: '0:00',      // 音频时长（简短格式）
    progress: 0,            // 播放进度（0-100）
    seqProgress: 0,         // 序列进度（备用）
    currentTime: 0,         // 当前播放时间（秒）
    maxTime: 0,             // 最大播放时间（秒）
    currentTimeFormatted: '00:00:00',  // 当前播放时间（格式化）
    separatedFiles: [],     // 分离后的文件列表（备用）
    audioType: '',          // 音频类型（备用）

    // ============================================
    // 用户信息
    // ============================================
    UserID: 1001,           // 用户ID（默认值，实际从登录信息获取）
    UserName: '王小明',      // 用户名（默认值）
    Phone: '',               // 手机号
    Password: '123456',      // 密码（默认值）
    Gender: '男',            // 性别（默认值）
    RegisterTime: '2024-02-22 18:48:39',  // 注册时间（默认值）
    Birthday: '2001-10-11',  // 出生日期（默认值）
    FaceImg: '',             // 头像路径
    
    // ============================================
    // 用户配额信息
    // ============================================
    MaxSepTimes: 10,        // 音频分离最大次数
    CurSepTimes: 0,         // 音频分离当前已用次数
    MaxNoiseTimes: 10,      // 音频降噪最大次数
    CurNoiseTimes: 0,       // 音频降噪当前已用次数
    
    // ============================================
    // 降噪参数
    // ============================================
    n_channels: '',          // 音频声道数（1-单声道，2-立体声）
    Order: 5,                // 巴特沃斯滤波阶数（默认5）
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    // 获取用户信息
    this.getUserAndDeNoiseInfo();

    // 创建音频播放上下文
    const innerAudioContext = wx.createInnerAudioContext();
    innerAudioContext.src = this.data.audioPath;

    innerAudioContext.onCanplay(() => {
      const Tduration = innerAudioContext.duration;
      console.log('音频时长:', Tduration);
    });

    this.audioContext = wx.createInnerAudioContext();
    
    this.audioContext.onTimeUpdate(() => {
      this.setData({
        progress: Math.floor((this.audioContext.currentTime / this.audioContext.duration) * 100)
      });
    });
    
    this.audioContext.onEnded(() => {
      this.setData({
        isPlaying: false,
        progress: 0
      });
    });
  },

  /**
   * 选择音频文件并上传
   * ===================
   * 功能：选择音频文件后自动上传到服务器，然后获取文件信息
   */
  chooseAudio() {
    const that = this;
    
    // 调用微信API选择文件
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['WAV', 'wav', 'mp3', 'ogg', 'aac', 'flac', 'm4a'],
      success(res) {
        const tempFilePath = res.tempFiles[0].path;
        const org_FileName = res.tempFiles[0].name;
        
        console.log("选择文件成功:", org_FileName);
        
        wx.showLoading({
          title: '上传中...',
          mask: true
        });
        
        // 上传文件到服务器
        const { uploadFile } = require('../../utils/request.js');
        uploadFile(
          tempFilePath,
          apiConfig.endpoints.uploadAudio,
          {},
          { name: 'file' }
        ).then(uploadRes => {
          console.log("上传成功:", uploadRes);
          
          if (uploadRes.success) {
            // 上传成功，保存文件信息
            that.setData({
              filePath: tempFilePath,
              orgFileName: org_FileName,
              filename: uploadRes.filename,  // 服务器返回的唯一文件名
              extension: uploadRes.extension,
              fileSize: uploadRes.fileSize,
              duration: that.formatDuration(uploadRes.durationSeconds || uploadRes.duration),
              n_channels: uploadRes.n_channels,
              title: '',
              artist: '',
              album: '',
              audioPath: tempFilePath,  // 原始音频播放路径（临时文件）
              DeNoisePath: '',  // 清空降噪后的路径
              DeNoisedOK: '0'   // 重置降噪状态
            });
            
            wx.hideLoading();
            wx.showToast({
              title: '上传成功',
              icon: 'success'
            });
          } else {
            wx.hideLoading();
            wx.showToast({
              title: uploadRes.error || '上传失败',
              icon: 'none'
            });
          }
        }).catch(err => {
          console.error("上传失败:", err);
          wx.hideLoading();
          wx.showToast({
            title: '上传失败，请重试',
            icon: 'none'
          });
        });
      },
      fail(err) {
        console.error('选择文件失败', err);
        wx.showToast({
          title: '选择文件失败',
          icon: 'none'
        });
      }
    });
  },
   
  /**
   * 执行音频降噪
   */
  DeNoiseAudio() {
    const that = this;
    
    // 检查用户降噪配额
    let TCurNoiseTimes = this.data.CurNoiseTimes;
    let TMaxNoiseTimes = this.data.MaxNoiseTimes;
    let nnn = TMaxNoiseTimes - TCurNoiseTimes;
    console.log('剩余降噪次数:', nnn);
    
    if (nnn <= 0) {
      wx.showToast({
        title: '音频降噪次数已用完，请向管理员申请追加音频降噪额度！',
        icon: 'none',
        duration: 4000,
      });
      return;
    }
    
    // 显示处理中提示
    wx.showLoading({
      title: '降噪处理中...',
      mask: true
    });
    
    // 发送降噪请求
    wx.request({    
      url: apiConfig.baseURL + apiConfig.endpoints.deNoiseAudio,
      method: "POST",
      timeout: 100000,
      header: {
        'content-type': 'application/json'
      },
      data: {
        audioPath: that.data.audioPath,
        filePath: that.data.filePath,
        fileSize: that.data.fileSize,
        duration: that.data.duration,
        orgFileName: that.data.orgFileName,
        filename: that.data.filename,  // 服务器返回的唯一文件名
        extension: that.data.extension,
        title: that.data.title,
        artist: that.data.artist,
        album: that.data.album,
        
        MaxSepTimes: that.data.MaxSepTimes,
        CurSepTimes: that.data.CurSepTimes,
        
        MaxNoiseTimes: that.data.MaxNoiseTimes,
        CurNoiseTimes: that.data.CurNoiseTimes,
        
        UserID: that.data.UserID,
        Phone: that.data.Phone,
        UserName: that.data.UserName,
        Gender: that.data.Gender,
        Birthday: that.data.Birthday,

        n_channels: that.data.n_channels,
        Order: that.data.Order
      }, 
      success: function(res){
        wx.hideLoading();
        console.log('降噪响应:', res);
        
        if (res.statusCode == 200 && res.data && res.data.success !== false) {
          // 降噪成功
          var ff = res.data.files;
          // 使用服务器URL进行试听（支持在线播放）
          var vPath = apiConfig.baseURL + '/api/audio/play/' + ff;
          
          that.setData({
            DeNoiseFiles: that.data.audioPath,
            seqProgress: 0,
            DeNoiseOK: '1',
            DeNoisePath: vPath,  // 降噪后的音频播放URL
            DeNoiseFilename: ff,  // 保存文件名用于下载
            n_channels: that.data.n_channels, 
          });
          
          wx.showToast({
            title: '降噪成功',
            icon: 'success'
          });
          
          console.log('降噪成功，文件:', ff);
          console.log('试听URL:', vPath);
        } else {
          var errorMsg = res.data && res.data.message ? res.data.message : '降噪失败！';
          console.log('降噪失败，状态码:', res.statusCode, '错误信息:', errorMsg);
          wx.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 3000
          });
          that.setData({
            DeNoiseFiles: that.data.audioPath,
            seqProgress: 0,
            DeNoiseOK: '0',
            DeNoisePath: '',
            DeNoiseFilename: '',
            n_channels: '', 
          });
        }
      },
      fail: function(err){ 
        wx.hideLoading();
        console.log('降噪失败:', err);
        wx.showToast({
          title: '降噪失败',
          icon: 'none'
        });
        that.setData({
          DeNoiseFiles: that.data.audioPath,
          seqProgress: 0,
          DeNoiseOK: '0',
          DeNoisePath: '',
          DeNoiseFilename: '',
          n_channels: '', 
        });
      }
    });
  },

  SetAudioStart: function(){
    this.AudioCtx.pause();
    this.AudioCtx.seek(0);
  },

  SetDeNoiseStart: function(){
    this.DeNoiseCtx.pause();
    this.DeNoiseCtx.seek(0);
  },

  onReady: function(e){
    this.AudioCtx = wx.createAudioContext('myAudio');
    this.DeNoiseCtx = wx.createAudioContext('DeNoiseAudio');
  },

  togglePlayPause() {
    if (this.audioContext.paused || this.audioContext.src === '') {
      if (this.audioContext.src) {
        this.audioContext.play();
        this.setData({ isPlaying: true });
      } else {
        wx.showToast({ title: '请选择音频文件', icon: 'none' });
      }
    } else {
      this.audioContext.pause();
      this.setData({ isPlaying: false });
    }
  },

  onAudioTimeUpdate(e) {
    const currentTime = e.detail.currentTime;
    const myduration = e.detail.duration;
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });
  },

  onDeNoiseTimeUpdate(e) {
    const currentTime = e.detail.currentTime;
    const myduration = e.detail.duration;
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });
  },

  formatDuration(duration) {
    // 支持两种格式：秒数（数字）或 "HH:MM:SS" 字符串
    if (typeof duration === 'number') {
      const hours = Math.floor(duration / 3600);
      const minutes = Math.floor((duration % 3600) / 60);
      const secs = Math.floor(duration % 60);
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    } else if (typeof duration === 'string' && duration.includes(':')) {
      return duration;
    } else {
      const seconds = parseFloat(duration) || 0;
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
  },

  /**
   * 获取用户信息和降噪历史
   */
  getUserAndDeNoiseInfo(){
    var that = this;
    // 从全局变量获取用户信息
    const app = getApp();
    if (app.globalData.userInfo) {
      const userInfo = app.globalData.userInfo;
      that.setData({
        UserID: userInfo.UserID || userInfo.user_id || 1001,
        Phone: userInfo.Phone || userInfo.user_Phone || '',
        UserName: userInfo.UserName || userInfo.user_name || '王小明',
        Password: userInfo.Password || userInfo.user_Password || '',
        Gender: userInfo.Gender || userInfo.user_Gender || '男',
        RegisterTime: userInfo.RegisterTime || userInfo.user_RegisterTime || '',
        Birthday: userInfo.Birthday || userInfo.user_Birthday || '',
        FaceImg: userInfo.FaceImg || userInfo.user_FaceImg || '',
        MaxNoiseTimes: userInfo.MaxNoiseTimes || userInfo.user_MaxNoiseTimes || 10,
        CurNoiseTimes: userInfo.CurNoiseTimes || userInfo.user_CurNoiseTimes || 0,
        MaxSepTimes: userInfo.MaxSepTimes || userInfo.user_MaxSepTimes || 10,
        CurSepTimes: userInfo.CurSepTimes || userInfo.user_CurSepTimes || 0
      });
    }
  },

  /**
   * 下载降噪后的音频文件（支持自定义文件名和路径）
   */
  DownloadDeNoise: function() {
    const that = this;
    
    // 检查是否有降噪后的文件
    if (!that.data.DeNoiseFilename) {
      wx.showToast({
        title: '请先完成降噪处理',
        icon: 'none'
      });
      return;
    }
    
    // 生成默认文件名（基于原始文件名）
    const defaultFileName = that.data.orgFileName 
      ? that.data.orgFileName.replace(/\.[^/.]+$/, '-降噪.wav')
      : '降噪音频-' + new Date().getTime() + '.wav';
    
    // 弹出输入框让用户输入自定义文件名
    wx.showModal({
      title: '自定义文件名',
      editable: true,
      placeholderText: '请输入文件名（不含扩展名）',
      content: defaultFileName.replace('.wav', ''),
      success(res) {
        if (res.confirm) {
          // 用户确认，使用输入的文件名
          let customFileName = res.content.trim();
          if (!customFileName) {
            customFileName = defaultFileName.replace('.wav', '');
          }
          // 确保有扩展名
          if (!customFileName.endsWith('.wav')) {
            customFileName += '.wav';
          }
          that.doDownloadDeNoise(customFileName);
        }
      }
    });
  },

  /**
   * 执行下载操作
   */
  doDownloadDeNoise: function(customFileName) {
    const that = this;
    
    wx.showLoading({ 
      title: '下载中...',
      mask: true
    });
    
    // 构建下载URL，同时把自定义文件名传给后端（用于服务器端下载文件名）
    const baseDownloadUrl = `${apiConfig.baseURL}${apiConfig.endpoints.downloadDeNoise}`;
    const query = `filename=${encodeURIComponent(that.data.DeNoiseFilename)}&customName=${encodeURIComponent(customFileName)}`;
    const downloadUrl = `${baseDownloadUrl}?${query}`;
    
    console.log('下载URL:', downloadUrl);
    console.log('自定义文件名:', customFileName);
    
    // 使用微信下载文件API
    wx.downloadFile({
      url: downloadUrl,
      success(res) {
        if (res.statusCode === 200) {
          // 下载成功，保存文件
          const tempFilePath = res.tempFilePath;
          
          // 使用文件系统API保存文件（不指定路径，使用系统默认路径）
          const fs = wx.getFileSystemManager();
          
          // 先读取临时文件内容
          fs.readFile({
            filePath: tempFilePath,
            success(readRes) {
              // 确定保存路径（使用系统文件目录，不指定复杂路径）
              let filePath = '';
              try {
                // 尝试使用USER_DATA_PATH
                if (typeof wx !== 'undefined' && wx.env && wx.env.USER_DATA_PATH) {
                  filePath = `${wx.env.USER_DATA_PATH}/${customFileName}`;
                } else {
                  // 如果USER_DATA_PATH不可用，使用临时文件所在目录
                  const tempDir = tempFilePath.substring(0, tempFilePath.lastIndexOf('/'));
                  filePath = `${tempDir}/${customFileName}`;
                }
              } catch (e) {
                // 如果出错，使用临时文件所在目录
                const tempDir = tempFilePath.substring(0, tempFilePath.lastIndexOf('/'));
                filePath = `${tempDir}/${customFileName}`;
              }
              
              // 写入文件
              fs.writeFile({
                filePath: filePath,
                data: readRes.data,
                success() {
                  wx.hideLoading();
                  wx.showModal({
                    title: '下载成功',
                    content: `文件已保存\n文件名：${customFileName}`,
                    showCancel: false,
                    confirmText: '确定'
                  });
                  console.log('文件已保存到:', filePath);
                },
                fail(writeErr) {
                  console.error('保存文件失败:', writeErr);
                  
                  // 如果writeFile失败，提示用户文件已下载
                  wx.hideLoading();
                  wx.showModal({
                    title: '下载完成',
                    content: `文件已下载\n文件名：${customFileName}\n\n文件位于临时目录，系统会自动管理`,
                    showCancel: false,
                    confirmText: '确定'
                  });
                  console.log('文件位于临时目录:', tempFilePath);
                }
              });
            },
            fail(readErr) {
              wx.hideLoading();
              console.error('读取临时文件失败:', readErr);
              wx.showToast({
                title: '保存文件失败',
                icon: 'none',
                duration: 2000
              });
            }
          });
        } else {
          wx.hideLoading();
          wx.showToast({
            title: '下载失败',
            icon: 'none'
          });
        }
      },
      fail(err) {
        wx.hideLoading();
        console.error('下载文件失败:', err);
        wx.showToast({
          title: '下载失败，请检查网络',
          icon: 'none'
        });
      },
      complete() {
        // 兜底关闭 loading，防止某些异常分支未正确隐藏
        try {
          wx.hideLoading();
        } catch (e) {}
      }
    });
  }
})
