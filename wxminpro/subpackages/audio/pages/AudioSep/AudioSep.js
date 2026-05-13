// ============================================
// 音频分离页面
// ============================================
// 功能：音频文件分离处理，将音频分离为人声、伴奏、鼓、贝斯等
// 路径：subpackages/audio/pages/AudioSep/AudioSep.js
// 说明：支持选择音频文件、执行分离、播放分离后的音频、下载分离文件

// ============================================
// 1. 导入依赖
// ============================================
const app = getApp();  // 获取小程序全局实例
const { post } = require('../../../../utils/request.js')  // 导入请求工具
const apiConfig = require('../../../../config/api.js')  // 导入API配置

// ============================================
// 2. 页面定义
// ============================================
Page({
  /**
   * 页面的初始数据
   * ==============
   * 说明：定义页面中使用的所有数据变量
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
    filename: '',           // 文件名（不带扩展名）
    extension: '',          // 文件扩展名（wav/mp3/ogg等）
    
    // ============================================
    // 分离后的音频文件路径
    // ============================================
    vocalsPath: '',         // 人声文件路径
    otherPath: '',          // 其他音轨路径
    drumsPath: '',          // 鼓声文件路径
    bassPath: '',           // 贝斯文件路径
    
    // ============================================
    // 分离状态相关
    // ============================================
    separatedOK: '0',       // 分离完成标记（'0'=未完成，'1'=已完成）
    org_FileName: '',       // 原始文件名
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
    separatedFiles: [],     // 分离后的文件列表
        
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
    audioType: '',           // 音频类型（备用）
    
    // ============================================
    // 用户配额信息
    // ============================================
    MaxSepTimes: 10,        // 音频分离最大次数
    CurSepTimes: 0,         // 音频分离当前已用次数
    MaxNoiseTimes: 10,      // 音频降噪最大次数
    CurNoiseTimes: 0,       // 音频降噪当前已用次数  

  },
  onLoad() {
    this.getUserInfoAudio();
    /////////////////////////////////////////////////////
    const innerAudioContext = wx.createInnerAudioContext();
    innerAudioContext.src = this.data.audioPath; // 替换为你的音频文件路径

    // 监听音频可以播放事件
    innerAudioContext.onCanplay(() => {
    const Tduration = innerAudioContext.duration; // 获取音频时长

    // 如果不需要播放音频，可以在获取到时长后调用stop方法停止播放（可选）
    // innerAudioContext.stop();
    });

    // 如果需要播放音频，可以调用play方法（可选）
    // innerAudioContext.play();

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
   * 选择音频文件
   * ============
   * 功能：从文件管理器选择音频文件，获取文件信息并上传到服务器
   * 流程：
   *   1. 选择音频文件（支持多种格式）
   *   2. 提取文件名和扩展名
   *   3. 上传文件到服务器
   *   4. 获取音频信息（大小、时长、元数据）
   *   5. 更新页面显示
   */
  /**
   * 选择音频文件并上传
   * ===================
   * 功能：选择音频文件后自动上传到服务器，然后获取文件信息
   */
  chooseAudio() {
    const that = this;
    
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['MP3', 'wav', 'aac', 'mp3', 'ogg', 'flac', 'mp4', 'm4a'],
      success(res) {
        const tempFilePath = res.tempFiles[0].path;
        const org_FileName = res.tempFiles[0].name;
        
        console.log("选择文件成功:", org_FileName);
        
        wx.showLoading({
          title: '上传中...',
          mask: true
        });
        
        // 上传文件到服务器
        const { uploadFile } = require('../../../../utils/request.js');
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
              org_FileName: org_FileName,
              filename: uploadRes.filename,  // 服务器返回的唯一文件名
              extension: uploadRes.extension,
              fileSize: uploadRes.fileSize,
              duration: that.formatDuration(uploadRes.durationSeconds || uploadRes.duration),
              title: '',
              artist: '',
              album: '',
              audioPath: tempFilePath,  // 原始音频播放路径（临时文件）
              // 清空分离后的路径
              vocalsPath: '',
              otherPath: '',
              drumsPath: '',
              bassPath: '',
              separatedOK: '0'  // 重置分离状态
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
   


   //分离音频文件中人声和背景音乐 
   /**
   * 执行音频分离
   * ============
   * 功能：调用后端接口对音频文件进行分离处理（人声、伴奏、鼓、贝斯等）
   * 流程：
   *   1. 检查用户分离配额
   *   2. 发送分离请求到后端
   *   3. 等待处理完成（可能耗时很长，100秒+）
   *   4. 获取分离后的文件路径（人声、伴奏等）
   *   5. 更新页面显示
   *   6. 记录分离历史
   * 
   * 注意：
   *   - 音频分离处理时间较长，需要设置超长超时时间
   *   - 分离后的文件较大，注意磁盘空间
   *   - 支持htdemucs等分离模型
   */
  separateAudio() {
    // 暂停使用：功能开发中
    wx.showToast({
      title: '音频分离功能开发中，暂不可用',
      icon: 'none',
      duration: 2000,
    });
    return;

    const that = this;
    
    // ============================================
    // 1. 检查用户分离配额
    // ============================================
    console.log("============ 检查分离配额 =================  1");
    console.log(this.data.CurSepTimes);
    console.log(that.data.CurSepTimes);
    console.log(this.data.MaxSepTimes);
    console.log(that.data.MaxSepTimes);
    console.log("==================================================== 2  ");
    let TCurSepTimes = this.data.CurSepTimes ;
    let TMaxSepTimes = this.data.MaxSepTimes;
    let nn = TMaxSepTimes - TCurSepTimes;
    console.log(TCurSepTimes);
    console.log(TMaxSepTimes);
    console.log(nn);
    console.log("==================================================== 3  ");
    if ( nn <= 0) {
      console.log("分离音频次数已用完，请向管理员申请追加分离音频额度！!!!!");
      wx.showToast({
        title: '分离音频次数已用完，请向管理员申请追加分离音频额度！',
        icon: 'none',
        duration: 4000,
      });
    } else {

    post(apiConfig.endpoints.separateAudio, {
      audioPath: that.data.audioPath,
      // AudioFilePath: that.data.AudioFilePath,
      filePath: that.data.filePath,
      fileSize: that.data.fileSize,
      duration: that.data.duration,
      filename: that.data.filename,
      extension: that.data.extension,
      org_FileName: that.data.org_FileName,
      title: that.data.title,
      artist: that.data.artist,
      album: that.data.album,
      MaxSepTimes: that.data.MaxSepTimes,
      CurSepTimes: that.data.CurSepTimes,
      MaxNoiseTimes: that.data.MaxNoiseTimes,
      CurNoiseTimes: that.data.CurNoiseTimes,
      UserID: that.data.UserID,
      UserName: that.data.UserName,
      Gender: that.data.Gender,
      Birthday: that.data.Birthday,
    }, {
      showLoading: true,
      loadingText: '分离中，请稍候...',
      timeout: 1000000, // 设置超时时间为1000秒
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      console.log('1 ========== res:', res);     
      console.log('2 ========== res:', res);
      
      wx.showToast({
        title: '分离成功',
        icon: 'success'
      });

      // 使用服务器返回的路径或构建播放URL
      var base_name = that.data.filename.split('.')[0] || that.data.filename;
      // 使用服务器URL进行试听（支持在线播放）
      var vPath = res.vocalsPath ? (apiConfig.baseURL + res.vocalsPath) : (apiConfig.baseURL + '/api/audio/play/htdemucs/' + base_name + '/vocals.wav');
      var oPath = res.otherPath ? (apiConfig.baseURL + res.otherPath) : (apiConfig.baseURL + '/api/audio/play/htdemucs/' + base_name + '/other.wav');
      var dPath = res.drumsPath ? (apiConfig.baseURL + res.drumsPath) : (apiConfig.baseURL + '/api/audio/play/htdemucs/' + base_name + '/drums.wav');
      var bPath = res.bassPath ? (apiConfig.baseURL + res.bassPath) : (apiConfig.baseURL + '/api/audio/play/htdemucs/' + base_name + '/bass.wav');
      
      var separatedOK = '1'
      var tt = that.data.CurSepTimes
      var myCurSepTimes = 0
      if (typeof tt === 'string') {
        myCurSepTimes = parseInt(tt, 10);
      } else if (typeof tt === 'number') {
        myCurSepTimes = tt
      }
      
      that.setData({
        separatedFiles: that.data.audioPath,
        seqProgress: 0,
        separatedOK: '1',
        vocalsPath: vPath,  // 人声播放URL
        otherPath: oPath,   // 其他音轨播放URL
        drumsPath: dPath,   // 鼓声播放URL
        bassPath: bPath,    // 贝斯播放URL
        // 保存文件名用于下载
        vocalsFilename: 'htdemucs/' + base_name + '/vocals.wav',
        otherFilename: 'htdemucs/' + base_name + '/other.wav',
        drumsFilename: 'htdemucs/' + base_name + '/drums.wav',
        bassFilename: 'htdemucs/' + base_name + '/bass.wav',
        CurSepTimes: myCurSepTimes + 1,   // 分离次数 + 1
      });

      console.log('3-1  that.data.separatedOK ===========:', that.data.separatedOK);
      console.log('3-2  that.data.vocalsPath ===========:', that.data.vocalsPath);
      console.log('3-3  that.data.otherPath ===========:', that.data.otherPath);
      console.log('3-4  that.data.drumsPath ===========:', that.data.drumsPath);
      console.log('3-5  that.data.bassPath ===========:', that.data.bassPath);
      console.log('3-6  that.data.CurSepTimes ===========:', that.data.CurSepTimes);
      
      ////  将修改后的 分离次数 更新到 userAudioInfo.txt
      ///////////////////////////////////////////////////
    }).catch(err => {
      console.log('3 Error 分离失败===========:', err);
      wx.showToast({
        title: '分离失败',
        icon: 'none'
      });
      that.setData({
        separatedFiles: that.data.audioPath,
        seqProgress: 0,
        separatedOK: '0',
        vocalsPath: '',
        otherPath: '',
        drumsPath: '',
        bassPath: '',
      });
      console.log('4-1  that.data.separatedOK ===========:', that.data.separatedOK);
      console.log('4-2  that.data.vocalsPath ===========:', that.data.vocalsPath);
      console.log('4-3  that.data.otherPath ===========:', that.data.otherPath);
      console.log('4-4  that.data.drumsPath ===========:', that.data.drumsPath);
      console.log('4-5  that.data.bassPath ===========:', that.data.bassPath);
      // 错误已在 request.js 中处理
    });
  }   
    
  },  //end of separateAudio()

  ///////////////////////////////////////////////////////////////////

  delayedFunction() {
      console.log("3秒钟后执行这段代码");
  },
  ////////////////////////////////////////////
  SetAudioStart:function(){
    this.AudioCtx.pause();
    this.AudioCtx.seek(0);
  },

  SetVocalsStart:function(){
    this.VocalsCtx.pause();
    this.VocalsCtx.seek(0);
  },

  SetOtherStart:function(){
    this.VocalsCtx.pause();
    this.OtherCtx.seek(0);
  },

  SetDrumsStart:function(){
    this.DrumsCtx.pause();
    this.DrumsCtx.seek(0);
  },

  SetBassStart:function(){
    this.BassCtx.pause();
    this.BassCtx.seek(0);
  },
  
  // 设置5个音频播放控件
  onReady:function(e){
    this.AudioCtx = wx.createAudioContext('myAudio');
    this.VocalsCtx = wx.createAudioContext('VocalsAudio');
    this.OtherCtx = wx.createAudioContext('OtherAudio');
    this.DrumsCtx = wx.createAudioContext('DrumsAudio');
    this.BassCtx = wx.createAudioContext('BassAudio')
  },

  ////////////////////////////////////////////
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

  // 修正后的 onSliderChange 方法
  onSliderChange(e) {
    // const audioContext = wx.createInnerAudioContext();
    // audioContext.currentTime = e.detail.value; // 设置音频播放到指定位置
    if (this.data.isPlaying) { // 使用 this.data.isPlaying 而不是 this.isPlaying
      const currentTime = (e.detail.value / 100) * this.audioContext.duration;
      this.audioContext.currentTime = currentTime;
    }
  },

  ////////////////////////////////////////////////////////////
  onAudioTimeUpdate(e) {
    const currentTime = e.detail.currentTime; // 当前播放时间
    const myduration = e.detail.duration; // 音频总时长
    console.log( myduration);
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });

  },

  ///////////////////////////////////////////////////////////
  onVocalsTimeUpdate(e) {
    const currentTime = e.detail.currentTime; // 当前播放时间
    const myduration = e.detail.duration; // 音频总时长
    console.log( myduration);
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });
  
  },


  onOtherTimeUpdate(e) {
    const currentTime = e.detail.currentTime; // 当前播放时间
    const myduration = e.detail.duration; // 音频总时长
    console.log( myduration);
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });
    
  },
  /////////////////////////////////////////////////////////////

  onDrumsTimeUpdate(e) {
    const currentTime = e.detail.currentTime; // 当前播放时间
    const myduration = e.detail.duration; // 音频总时长
    console.log( myduration);
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });

  },
  //////////////////////////////////////////////////////////////////////
  onBassTimeUpdate(e) {
    const currentTime = e.detail.currentTime; // 当前播放时间
    const myduration = e.detail.duration; // 音频总时长
    console.log( myduration);
    console.log('当前播放时间:', currentTime, '总时长:', myduration);

    const durationSeconds = Math.floor(myduration);
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    this.setData({
      Mduration: `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
    });

  },
  /////////////////////////////////////////////////////////////////////

  //////////////////////////////////////////////////////////////
  formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const msecs = Math.floor((seconds % 1) * 100);
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}:${String(msecs).padStart(2, '0')}`;
  },

  //////////////////////////////////////////////////
  saveAudioFile(tempFilePath,filename,extension) {  
    const that = this ;
    const fs = wx.getFileSystemManager();
    const myAudioFilePath = `${wx.env.USER_DATA_PATH}/Audio/${filename}.${extension}`;
    // const myAudioFilePath = `${wx.env.USER_DATA_PATH}/${filename}.${extension}`;
    console.log("===========================  4 ")
    console.log(tempFilePath)
    console.log(myAudioFilePath)
    fs.copyFile({
      srcPath: tempFilePath,
      destPath: myAudioFilePath,
      success: () => {
        wx.showToast({
          title: '音频文件保存成功!',
          icon: 'success',
        });
        console.log("=============== 1 myAudioFilePath  ===============");
        console.log(myAudioFilePath);
        that.setData({AudioFilePath:myAudioFilePath });
        console.log("=============== 2 AudioFilePath  ===============");
        console.log(this.data.AudioFilePath);
      },
      fail: (err) => {
        console.error('音频保存失败：', err);
        wx.showToast({
          title: '音频文件保存失败!',
          icon: 'none',
        });
      },
    });
  },



    ///////////// 以下为 因为页面刷新丢失的变量，重新恢复
  getUserAndAudioInfo(){
      var that = this;
      ////// （1） 获取 AudioInfo.txt 更新页面上音频连接信息
      wx.getFileSystemManager().readFile({
      filePath: `${wx.env.USER_DATA_PATH}/AudioInfo.txt`, // 文件路径
      encoding: 'utf8', // 编码方式，这里使用utf8编码读取文本文件
      success: function(res) {
            // 成功读取文件后，res.data 将包含文件的内容
            console.log('文件内容：', res.data);
            var lines = res.data.split('\n');
      
            ///////////////////////  测试读取到的信息， 仅仅用于测试
            console.log('文件内容 lines：', lines);
            console.log('文件内容 lines[0]：', lines[0]);
            console.log('文件内容 lines[1]：', lines[1]);
            console.log('文件内容 lines[2]：', lines[2]);
            // 更新用户登录信息：你可以在这里对文件内容进行进一步处理
            that.setData({
                  audioPath: lines[0].slice(0, -1),       // 用户选择的音频文件，储存在：http://tmp
                  filePath: lines[1].slice(0, -1),        // 用户选择的音频文件， 储存在：http://tmp
                  fileSize: lines[2].slice(0, -1),        // 音频文件大小 MB
                  duration:lines[3].slice(0, -1),         // 音频文件大小播放时长（秒）
                  filename: lines[4].slice(0, -1),        // 音频文件名称
                  extension: lines[5].slice(0, -1),       // 音频文件扩展名称（ wav  ogg  mp3  flc ） 
                  org_FileName: lines[6].slice(0, -1),    // 音频文件原始文件名称（ org_FileName ） 
                  vocalsPath: lines[7].slice(0, -1),      // 人声文件 http://usr/Audio/output/....../vocals.wav
                  otherPath: lines[8].slice(0, -1),       // 伴奏文件 http://usr/Audio/output/....../other.wav
                  drumsPath: lines[9].slice(0, -1),       // 鼓声文件 http://usr/Audio/output/....../drum.wav
                  bassPath: lines[10].slice(0, -1),       // 贝斯声文件 http://usr/Audio/output/....../bass.wav
                  title: lines[11].slice(0, -1),          // 音乐标题
                  artist: lines[12].slice(0, -1),         // 音乐歌手
                  album : lines[13].slice(0, -1),         // 唱片集
                  separatedOK: lines[14]                  // 是否分离 成功： 1   失败：0 
                  
          });
          /////////////////////////////////////////// 仅仅用于测试
          console.log("AudioInfo.audioPath: ",that.data.audioPath);
          console.log("AudioInfo.audioPath: ",that.data.audioPath);
          console.log("AudioInfo.fileSize: ",that.data.fileSize);
          console.log("AudioInfo.duration: ",that.data.duration);
          console.log("AudioInfo.vocalsPath: ",that.data.vocalsPath);
          console.log("AudioInfo.otherPath: ",that.data.otherPath);
          console.log("AudioInfo.drumsPath: ",that.data.drumsPath);
          console.log("AudioInfo.bassPath: ",that.data.bassPath);

      },  //  success  end


      fail: function(err) {
          // 读取文件失败时的回调函数
            console.error('读取 AudioInfo.txt 文件失败：', err);
        }

      }); // wx.getFileSystemManager().readFile  end
      //////  获取 AudioInfo.txt 更新页面上音频连接信息  end

      ////// （2）获取userInfoAudio.txt信息，包括用户已经使用的分离次数信息（已废弃）
      // 说明：
      //   - 旧版本通过本地文本文件 userInfoAudio.txt 保存登录用户信息和分离/降噪次数
      //   - 新版本已经改为从后端接口和全局状态（app.globalData）获取这些信息
      //   - 因此这里不再读取该文件，避免控制台出现 readFile:fail not found 报错
      //   - 页面所需的 UserID、配额等，已经在进入分离页面时通过其他方式 setData 完成

    },   // getUserAndAudioInfo()  end


  // 以下函数没有启用
  setVcalsOtherInfo(AudioInfoData){
    // setInfo(mydata){
      const fileSystemManager = wx.getFileSystemManager();
      const filePath = `${wx.env.USER_DATA_PATH}/AudioInfo.txt`; // 文件路径
      // const data = '这是要写入文件的内容'; // 要写入文件的数据
      const data = mydata; // 要写入文件的数据
  
      fileSystemManager.writeFile({
          filePath: filePath, // 文件路径
          data: data, // 要写入的数据
          encoding: 'utf8', // 编码方式，这里使用utf8编码写入文本文件
        
      success: function() {
            // 文件写入成功时的回调函数
            console.log('AudioInfo.txt文件写入成功');
            // 你可以在这里进行后续操作，比如通知用户或读取刚写入的数据进行验证
        },
        fail: function(err) {
          // 文件写入失败时的回调函数
            console.error('AudioInfo.txt文件写入失败：', err);
        // 你可以在这里处理错误，比如显示错误消息给用户
      }
  });
  },

  /////////////////////////////////////////////////
// 下载人声文件音频文件
  DownloadVocals: function(){
    this.setData({
      audioType:'vocals',
  });
    this.DownloadAudio('vocals');
  },

  // 下载伴奏音频文件
  DownloadOther: function(){
    this.setData({
      audioType:'other',
  });
    this.DownloadAudio('other');
  },

  // 下载鼓声音频文件
  DownloadDrums: function(){
    this.setData({
      audioType:'drums',
  });
    this.DownloadAudio('drums');
  },

  // 下载贝斯音频文件
  DownloadBass: function(){
    this.setData({
      audioType:'bass',
  });
    this.DownloadAudio('bass');
  },

  /**
   * 下载分离后的音频文件
   * ====================
   * 功能：下载分离后的音频文件（人声、伴奏、鼓、贝斯）
   */
  DownloadAudio: function(audioType) {
    const that = this;
    
    // 获取对应的文件名和类型名称
    let filename = '';
    let typeName = '';
    if (audioType === 'vocals') {
      filename = that.data.vocalsFilename;
      typeName = '人声';
    } else if (audioType === 'other') {
      filename = that.data.otherFilename;
      typeName = '伴奏';
    } else if (audioType === 'drums') {
      filename = that.data.drumsFilename;
      typeName = '鼓声';
    } else if (audioType === 'bass') {
      filename = that.data.bassFilename;
      typeName = '贝斯';
    }
    
    if (!filename) {
      wx.showToast({
        title: '请先完成音频分离',
        icon: 'none'
      });
      return;
    }
    
    // 生成默认文件名
    const orgFileName = that.data.org_FileName || that.data.filename || '音频';
    const baseName = orgFileName.replace(/\.[^/.]+$/, '');
    const defaultFileName = `${baseName}-${typeName}.wav`;
    
    // 弹出输入框让用户输入自定义文件名
    wx.showModal({
      title: `自定义${typeName}文件名`,
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
          that.doDownloadAudio(audioType, filename, customFileName, typeName);
        }
      }
    });
  },

  /**
   * 执行下载操作
   */
  doDownloadAudio: function(audioType, serverFilename, customFileName, typeName) {
    const that = this;
    
    wx.showLoading({ 
      title: '下载中...',
      mask: true
    });
    
    // 构建下载URL（使用分离文件的下载接口）
    const downloadUrl = `${apiConfig.baseURL}/api/download/separated/${serverFilename}`;
    
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
                    content: `${typeName}文件已保存\n文件名：${customFileName}`,
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
                    content: `${typeName}文件已下载\n文件名：${customFileName}\n\n文件位于临时目录，系统会自动管理`,
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
      }
    });
  },

  /////////////////// 2025-01-07  用微信小程序JS实现 分离后的音频文件的下载 begin  目前为废弃
  DownloadAudio_temp: function(audioType) {
      const that = this;
      wx.showLoading({ title: '下载中...', });
      let myfile_url = '';
      let myTitle0 = '';
      if (audioType==='vocals'){
        myfile_url=this.data.vocalsPath;
        myTitle0 = 'vocals(人声).wav';
      };
      if (audioType==='other'){
        myfile_url=this.data.otherPath;
        myTitle0 = 'other(伴奏).wav';      
      };
      if (audioType==='drums'){
        myfile_url=this.data.drumsPath; 
        myTitle0 = 'drums(鼓).wav';  
      };
      if (audioType==='bass'){
        myfile_url=this.data.bassPath;  
        myTitle0 = 'bass(贝斯).wav';     
      };
      // 输出结果以验证
      console.log(myfile_url);
      console.log(this.data.org_FileName );
      console.log(myTitle0);

      ///////////////////////////////////////////////////////
      // 假设 title, org_FileName, 和 myTitle0 是已经定义好的变量
      // let title = ''; // 示例值，实际使用时应该有其他来源
      // let org_FileName = ''; // 示例值，实际使用时应该有其他来源
      // let myTitle0 = 'default_title.wav'; // 示例值，实际使用时应该根据需求设置
      let TempTitle = this.data.title;               // 歌曲标题:  茶歌
      let TempOrg_FileName = this.data.org_FileName; // 歌曲文件名（不含扩展名）: 杜聪 - 茶歌
      let myTitle = '';
      let outdir = '';

      // 假如 myTitle0 ： vocals(人声).wav
      if (!TempTitle) {
        if (!TempOrg_FileName) {
          myTitle = myTitle0;                          // vocals(人声).wav
          outdir = 'Temp';
        } else {
          myTitle = TempOrg_FileName + '-' + myTitle0;  // 杜聪 - 茶歌-vocals(人声).wav
          outdir = TempOrg_FileName ;
        }
      } else {
        myTitle = TempTitle + '-' + myTitle0;          // 茶歌-vocals(人声).wav
        outdir = TempTitle;
      }

      // 假如 myTitle0 ： other(伴奏).wav  则为：  茶歌-other(伴奏).wav
      // 输出结果以验证
      console.log(myTitle);    //  vocals(人声).wav

      ///////////////////////////////////////////////////////
      // 获取当前日期和时间
      const now = new Date();
      
      // 格式化日期和时间
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1，并补零
      const day = String(now.getDate()).padStart(2, '0'); // 补零
      const hours = String(now.getHours()).padStart(2, '0'); // 补零
      const minutes = String(now.getMinutes()).padStart(2, '0'); // 补零
      const seconds = String(now.getSeconds()).padStart(2, '0'); // 补零

      // 拼接日期时间字符串和outdir字符串
      const newOutdir = `${year}-${month}-${day}--${hours}-${minutes}-${seconds}-${outdir}`;

      const newFilename = `${year}-${month}-${day}--${hours}-${minutes}-${seconds}-${myTitle}`;
      // 2025-01-06--15-06-25-茶歌
  
      // 拼接完整的目录路径
      // const basePath = wx.env.USER_DATA_PATH;
      const basePath = '/Audio';
      const dirPath = `${basePath}/download/separate/${newOutdir}`;
      // 创建一个形如下面的文件夹 wx.env.USER_DATA_PATH/download/separate/2025-01-06--15-06-25-茶歌
      console.log("========================================= begin ");
      const url = myfile_url;             // 替换为实际的音频文件URL
      // 构建本地保存路径
      const fs = wx.getFileSystemManager(); // 获取文件系统管理器

      // 定义源路径和目标路径
      // C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a\usr\Audio\output\htdemucs\vStSMIGvKmxz8ec6eebe2edf0e786ebb119a09b40178
      const sourcePath = wx.env.USER_DATA_PATH + "\Audio\output\htdemucs\vStSMIGvKmxz8ec6eebe2edf0e786ebb119a09b40178/vocals.wav";
      const targetDir = wx.env.USER_DATA_PATH + "/Audio/Download/Separate";
      const targetPath = targetDir + "/vocals.wav";

      // 确保目标目录存在
      fs.access({
          path: targetDir,
          success: () => {
              console.log("目标目录已存在，准备复制文件");
              copyFile();
          },
          fail: () => {
              console.log("目标目录不存在，创建目录中...");
              fs.mkdir({
                  dirPath: targetDir,
                  recursive: true, // 递归创建目录
                  success: () => {
                      console.log("目标目录创建成功，准备复制文件");
                      that.copyFile();
                  },
                  fail: (err) => {
                      console.error("创建目录失败:", err);
                  }
              });
          }
      });

    // 复制文件函数
    function copyFile() {
        fs.copyFile({
            srcPath: sourcePath,
            destPath: targetPath,
            success: () => {
                console.log("文件复制成功:", targetPath);
            },
            fail: (err) => {
                console.error("文件复制失败:", err);
            }
        });
    }

  },
  /////////////////////////////////////////////////////////
  TTdownloadFile(url, filePath) {
    console.log("========================================= 1");
    console.log(url);
    console.log(filePath)
    wx.downloadFile({
      url,
      filePath,
      success: (res) => {
        const tempFilePath = res.tempFilePath;
        const savedFilePath = res.savedFilePath;
        console.log('文件下载成功', savedFilePath);

        // 这里可以添加其他操作，比如播放音频或显示下载成功提示
        wx.showToast({
          title: '下载成功',
          icon: 'success',
          duration: 2000
        });
        return 200 ;
      },
      fail: (err) => {
        console.error('文件下载失败22222', err);
        wx.showToast({
          title: '下载失败22222',
          icon: 'none',
          duration: 2000
        });
        return 405 ;
      }
      
    });
  },

  ////////////////////////////////////////////////////// 2025-01-07     end
  
  /**
   * 获取用户信息（旧逻辑，已废弃）
   * ============
   * 旧版本：从本地文件 userInfoAudio.txt 读取用户配额、资料
   * 新版本：用户信息和配额从后端接口 & app.globalData 获取，因此这里不再读取本地文件，避免报错
   */
  getUserInfoAudio(){
    // 直接使用 app.globalData.userInfo 或页面 onLoad/onShow 时从后端刷新配额；
    // 这里不再访问本地文件，避免 readFile:fail not found 报错。
    console.log('getUserInfoAudio 调用：本地 userInfoAudio.txt 逻辑已废弃，使用全局/后端数据。');

  },   // getInfo()  end


  })

//  "scope.userInfo": {
//     "desc": "你的信息将用于语音识别的用户验证"
//      }



