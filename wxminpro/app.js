// app.js
App({
  globalData: {
    userInfo: null,
    isLoggedIn: false
  },

  /**
   * 小程序启动时的生命周期函数
   */
  onLaunch() {
    console.log('小程序启动')
    // 检查用户登录状态
    this.checkLoginStatus()
  },

  /**
   * 检查用户登录状态
   */
  checkLoginStatus() {
    try {
      const userInfo = wx.getStorageSync('userInfo')
      if (userInfo && userInfo.Phone) {
        this.globalData.userInfo = userInfo
        this.globalData.isLoggedIn = true
        console.log('用户已登录:', userInfo.UserName)
      } else {
        this.globalData.isLoggedIn = false
        console.log('用户未登录')
        // 未登录时跳转到登录页面
        wx.reLaunch({
          url: '/pages/login/login'
        })
      }
    } catch (e) {
      console.error('检查登录状态失败:', e)
      this.globalData.isLoggedIn = false
      wx.reLaunch({
        url: '/pages/login/login'
      })
    }
  },

  /**
   * 小程序显示时的生命周期函数
   */
  onShow() {
    console.log('小程序显示')
    // 每次显示时检查登录状态
    this.checkLoginStatus()
  },

  /**
   * 小程序隐藏时的生命周期函数
   */
  onHide() {
    console.log('小程序隐藏')
  },

  /**
   * 退出登录
   */
  logout() {
    try {
      wx.removeStorageSync('userInfo')
      wx.removeStorageSync('rememberedLogin')
      this.globalData.userInfo = null
      this.globalData.isLoggedIn = false
      wx.reLaunch({
        url: '/pages/login/login'
      })
    } catch (e) {
      console.error('退出登录失败:', e)
      wx.reLaunch({
        url: '/pages/login/login'
      })
    }
  }
})

