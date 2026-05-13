// pages/telphone/telphone.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    Phone: "",
    Code: "",
    responseData: {}, // 存储后端Python for Flask 返回的数据
    gettingCode: false, // 是否正在获取验证码
    countdown: 0, // 倒计时秒数
    loggingIn: false, // 是否正在登录
    countdownTimer: null // 倒计时定时器
  },

  /**
   * 手机号输入
   */
  inputPhone: function(e) {
    const phone = e.detail.value;
    // 只允许输入数字
    const phoneNum = phone.replace(/\D/g, '');
    this.setData({ Phone: phoneNum });
  },

  /**
   * 验证码输入
   */
  inputCode: function(e) {
    const code = e.detail.value;
    // 只允许输入数字
    const codeNum = code.replace(/\D/g, '');
    this.setData({ Code: codeNum });
  },

  /**
   * 获取验证码
   */
  getCode: function() {
    const that = this;
    const phone = this.data.Phone;

    // 验证手机号格式
    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 如果正在倒计时，不允许重复点击
    if (that.data.countdown > 0) {
      return;
    }

    that.setData({ gettingCode: true });
    wx.showLoading({
      title: '发送中...',
      mask: true
    });

    // 这里可以调用后端API获取验证码
    // 注意：如果后端没有 GetCode 接口，这里会失败，但会开始倒计时（用于测试）
    post('/api/GetCode', { Phone: phone }, {
      showLoading: false, // 已经在外部显示
    }).then(res => {
      that.setData({ gettingCode: false });
      
      wx.showToast({
        title: '验证码已发送',
        icon: 'success',
        duration: 2000
      });
      
      // 开始倒计时
      that.startCountdown();
    }).catch(err => {
      that.setData({ gettingCode: false });
      console.error('获取验证码失败：', err);
      
      // 即使后端接口失败，也允许开始倒计时（用于测试）
      // 实际项目中应该根据后端返回结果决定
      that.startCountdown();
      // 错误已在 request.js 中处理
    });
  },

  /**
   * 开始倒计时
   */
  startCountdown: function() {
    const that = this;
    let countdown = 60; // 60秒倒计时
    
    that.setData({ countdown: countdown });
    
    const timer = setInterval(function() {
      countdown--;
      if (countdown <= 0) {
        clearInterval(timer);
        that.setData({ 
          countdown: 0,
          countdownTimer: null
        });
      } else {
        that.setData({ countdown: countdown });
      }
    }, 1000);
    
    that.setData({ countdownTimer: timer });
  },

  /**
   * 登录
   */
  login: function(e) {
    const that = this;
    const { Phone, Code } = this.data;

    // 验证输入
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

    if (!Code) {
      wx.showToast({
        title: '请输入验证码',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (Code.length !== 6) {
      wx.showToast({
        title: '验证码应为6位数字',
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
    wx.showLoading({
      title: '登录中...',
      mask: true
    });

    console.log('登录请求：', Phone, Code);

    post(apiConfig.endpoints.formPost, {
      Phone: Phone,
      Code: Code
    }, {
      showLoading: false, // 已经在外部显示
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      }
    }).then(res => {
      that.setData({ loggingIn: false });
      
      console.log("登录成功", res);
      
      // 获取并更新后端返回的数据
      that.setData({
        responseData: res || {}
      });

      // 如果登录成功，可以跳转到其他页面
      if (res) {
        wx.showToast({
          title: '登录成功',
          icon: 'success',
          duration: 2000
        });
        
        // 这里可以根据后端返回的数据判断是否登录成功
        // 例如：if (res.success) { ... }
      }
    }).catch(err => {
      that.setData({ loggingIn: false });
      console.error("登录失败", err);
      // 错误已在 request.js 中处理
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 页面加载时的初始化
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {
    // 清除倒计时定时器
    if (this.data.countdownTimer) {
      clearInterval(this.data.countdownTimer);
      this.setData({ countdownTimer: null });
    }
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
