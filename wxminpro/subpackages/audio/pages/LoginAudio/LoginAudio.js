// pages/LoginAudio/LoginAudio.js
const app = getApp()
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    Phone: '',
    Password: '',
    jin: true, // 控制登录按钮是否禁用
    loggingIn: false, // 是否正在登录
    
    // 用户信息（从后端获取）
    UserID: 1001,
    UserName: '',
    Gender: '',
    RegisterTime: '',
    Birthday: '',
    FaceImg: '',
    audioType: '',
    MaxSepTimes: 10,
    CurSepTimes: 0,
    MaxNoiseTimes: 10,
    CurNoiseTimes: 0,
  },

  /**
   * 手机号输入
   */
  PhoneInput: function(e) {
    const phone = e.detail.value.replace(/\D/g, ''); // 只允许数字
    this.setData({ Phone: phone });
    
    // 只有手机号和密码都非空，才能点击登录按钮
    if (phone !== '' && this.data.Password !== '') {
      this.setData({ jin: false });
    } else {
      this.setData({ jin: true });
    }
  },

  /**
   * 密码输入
   */
  passwordInput: function(e) {
    const password = e.detail.value;
    this.setData({ Password: password });
    
    // 只有手机号和密码都非空，才能点击登录按钮
    if (password !== '' && this.data.Phone !== '') {
      this.setData({ jin: false });
    } else {
      this.setData({ jin: true });
    }
  },

  /**
   * 登录
   */
  post: function() {
    const that = this;
    const { Phone, Password } = this.data;

    // 输入验证
    if (!Phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(Phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!Password) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 如果正在登录，不允许重复提交
    if (that.data.loggingIn) {
      return;
    }

    that.setData({ loggingIn: true });

    post(apiConfig.endpoints.loginAudio, {
      Phone: Phone,
      Password: Password
    }, {
      showLoading: true,
      loadingText: '登录中...',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      }
    }).then(res => {
      that.setData({ loggingIn: false });
      
      console.log("登录响应：", res);
      
      // 处理字符串响应（'0'表示失败）
      if (typeof res === 'string' && res === '0') {
        wx.showModal({
          title: '提示',
          content: '手机号或密码不正确！',
          showCancel: false,
          confirmText: '确定'
        });
        return;
      }
      
      if (res && res !== 0) {
          // 登录成功
          console.log("登录成功");
          
          // 显示后端返回的数据（用于调试）
          console.log("用户ID:", res.data.user_id);
          console.log("手机号:", res.data.user_Phone);
          console.log("用户名:", res.data.user_name);
          console.log("性别:", res.data.user_Gender);
          console.log("生日:", res.data.user_Birthday);
          console.log("头像:", res.data.user_FaceImg);
          console.log("用户类型:", res.data.user_UserType);
          console.log("最大分离次数:", res.data.user_MaxSepTimes);
          console.log("当前分离次数:", res.data.user_CurSepTimes);
          console.log("最大降噪次数:", res.data.user_MaxNoiseTimes);
          console.log("当前降噪次数:", res.data.user_CurNoiseTimes);

          // 保存用户登录数据到页面
          that.setData({
            Phone: res.data.user_Phone,
            UserName: res.data.user_name,
            Gender: res.data.user_Gender,
            Birthday: res.data.user_Birthday,
            Password: res.data.user_Password,
            FaceImg: res.data.user_FaceImg || "/static/image/header.png",
            UserType: res.data.user_UserType,
            MaxSepTimes: res.data.user_MaxSepTimes,
            CurSepTimes: res.data.user_CurSepTimes,
            MaxNoiseTimes: res.data.user_MaxNoiseTimes,
            CurNoiseTimes: res.data.user_CurNoiseTimes
          });

          // 设置全局变量数据
          app.globalData.userInfo = {
            nickName: res.data.user_name,
            Phone: res.data.user_Phone,
            Password: res.data.user_Password,
            Gender: res.data.user_Gender,
            Birthday: res.data.user_Birthday,
            FaceImg: res.data.user_FaceImg || "/static/image/header.png",
            UserType: res.data.user_UserType,
            MaxSepTimes: res.data.user_MaxSepTimes,
            CurSepTimes: res.data.user_CurSepTimes,
            MaxNoiseTimes: res.data.user_MaxNoiseTimes,
            CurNoiseTimes: res.data.user_CurNoiseTimes
          };

          // 将用户登录信息保存到本地文件
          var mydata = "32\n" + 
            res.data.user_Phone + "\n" + 
            res.data.user_name + "\n" + 
            res.data.user_Password + "\n" + 
            res.data.user_Gender + "\n" + 
            '2024-12-05 20:11:19' + "\n" + 
            res.data.user_Birthday + "\n" + 
            res.data.user_FaceImg + "\n" + 
            res.data.user_UserType + "\n" +
            res.data.user_MaxSepTimes + "\n" + 
            res.data.user_CurSepTimes + "\n" +
            res.data.user_MaxNoiseTimes + "\n" + 
            res.data.user_CurNoiseTimes;
          
          console.log("====================================== mydata ========================");
          console.log(mydata);
          that.setInfo(mydata);

          // 显示成功提示
          wx.showToast({
            title: '登录成功',
            icon: 'success',
            duration: 2000
          });

          // 延迟跳转，让用户看到成功提示
          setTimeout(() => {
            wx.switchTab({
              url: '/pages/home/home'
            });
          }, 1500);
        } else {
          // 登录失败
          console.log("登录失败");
          wx.showModal({
            title: '提示',
            content: '手机号或密码不正确！',
            showCancel: false,
            confirmText: '确定',
            success(res) {
              if (res.confirm) {
                console.log('用户确认');
              }
            }
          });
        }
      }).catch(err => {
        that.setData({ loggingIn: false });
        console.error("登录请求失败：", err);
        // 错误已在 request.js 中处理
      });
  },

  /**
   * 将用户登录信息写到微信小程序本地存储空间
   */
  setInfo(mydata) {
    const fileSystemManager = wx.getFileSystemManager();
    const filePath = `${wx.env.USER_DATA_PATH}/userInfoAudio.txt`;
    
    console.log("保存文件路径：", filePath);

    fileSystemManager.writeFile({
      filePath: filePath,
      data: mydata,
      encoding: 'utf8',
      success: function() {
        console.log('用户信息文件写入成功');
      },
      fail: function(err) {
        console.error('用户信息文件写入失败：', err);
      }
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 页面加载时的初始化
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {},

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {},

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {}
});
