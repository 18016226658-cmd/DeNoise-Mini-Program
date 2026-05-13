// pages/home/home.js
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null
  },

  onLoad(options) {
    // 检查登录状态
    if (!app.globalData.isLoggedIn) {
      wx.reLaunch({
        url: '/pages/login/login'
      })
      return
    }
    // 加载用户信息
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },

  onShow() {
    // 每次显示时检查登录状态
    if (!app.globalData.isLoggedIn) {
      wx.reLaunch({
        url: '/pages/login/login'
      })
      return
    }
    // 更新用户信息
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },

  //注销账号
  goToLogout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success(res) {
        if (res.confirm) {
          app.logout()
        }
      }
    })
  },

  // 导航到音频降噪
  navigateToDeNoise() {
    wx.switchTab({
      url: '/pages/DeNoise/DeNoise'
    });
  },

  // 导航到录音功能
  navigateToSoundRecord() {
    wx.navigateTo({
      url: '/subpackages/audio/pages/soundRecord/soundRecord'
    });
  },

  // 导航到历史记录
  navigateToHistory() {
    wx.switchTab({
      url: '/pages/history/history'
    });
  }
})
