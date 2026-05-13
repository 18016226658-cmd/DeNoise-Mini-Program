// pages/UserInfo/UserInfo.js
// ============================================
// 用户信息页面
// ============================================
// 功能：显示用户个人信息（普通用户）或所有用户信息（管理员）

const app = getApp()
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},           // 当前登录用户信息
    userType: 2,            // 用户类型：1-管理员，2-普通用户，3-游客
    userList: [],           // 用户列表（管理员可见）
    showUserList: false,    // 是否显示用户列表
    loading: false,         // 加载状态
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.getCurrentUserInfo()
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    this.getCurrentUserInfo()
  },

  /**
   * 获取当前登录用户信息
   */
  getCurrentUserInfo() {
    const userInfo = app.globalData.userInfo
    if (userInfo) {
      const userType = userInfo.UserType || userInfo.user_UserType || 2
      this.setData({
        userInfo: userInfo,
        userType: userType,
        showUserList: userType === 1  // 只有管理员才显示用户列表
      })
      
      // 如果是管理员，加载所有用户列表
      if (userType === 1) {
        this.loadUserList()
      }
    } else {
      wx.showToast({
        title: '请先登录',
        icon: 'none',
        duration: 2000
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 2000)
    }
  },

  /**
   * 加载用户列表（管理员功能）
   */
  loadUserList() {
    const that = this
    if (that.data.loading) {
      return
    }

    that.setData({ loading: true })

    post(apiConfig.endpoints.editUser, {}, {
      showLoading: false,
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      that.setData({ loading: false })
      
      console.log("用户列表：", res)
      
      const userList = Array.isArray(res) ? res : []
      that.setData({
        userList: userList
      })
    }).catch(err => {
      that.setData({ loading: false })
      console.error("获取用户列表失败：", err)
    })
  },

  /**
   * 跳转到管理员可视化界面
   */
  navigateToVisualization() {
    if (this.data.userType === 1) {
      wx.navigateTo({
        url: '/subpackages/user/pages/AdminVisualization/AdminVisualization'
      })
    } else {
      wx.showToast({
        title: '仅管理员可访问',
        icon: 'none',
        duration: 2000
      })
    }
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    if (this.data.userType === 1) {
      this.loadUserList()
    }
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  }
})

