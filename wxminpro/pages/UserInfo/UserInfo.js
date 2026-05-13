// pages/UserInfo/UserInfo.js
// ============================================
// 用户信息页面
// ============================================
// 功能：显示用户个人信息（普通用户）或所有用户信息（管理员）

const app = getApp()
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

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
        wx.switchTab({
          url: '/pages/home/home'
        })
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
      
      // 处理响应数据：如果返回的是字符串，需要解析JSON
      let userList = []
      if (typeof res === 'string') {
        try {
          userList = JSON.parse(res)
        } catch (e) {
          console.error("解析用户列表JSON失败：", e)
          userList = []
        }
      } else if (Array.isArray(res)) {
        userList = res
      } else if (res && Array.isArray(res.data)) {
        userList = res.data
      }
      
      // 确保每个用户都有配额字段，如果没有则设置默认值
      userList = userList.map(user => ({
        ...user,
        MaxSepTimes: user.MaxSepTimes || 10,
        CurSepTimes: user.CurSepTimes || 0,
        MaxNoiseTimes: user.MaxNoiseTimes || 10,
        CurNoiseTimes: user.CurNoiseTimes || 0
      }))
      
      that.setData({
        userList: userList
      })
    }).catch(err => {
      that.setData({ loading: false })
      console.error("获取用户列表失败：", err)
    })
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
  },

  /**
   * 编辑当前用户信息
   */
  editCurrentUser() {
    wx.navigateTo({
      url: '/pages/EditUserInfo/EditUserInfo'
    })
  },

  /**
   * 编辑其他用户信息（管理员功能）
   */
  editUser(e) {
    const phone = e.currentTarget.dataset.phone
    if (!phone) {
      return
    }
    wx.navigateTo({
      url: `/pages/EditUserInfo/EditUserInfo?phone=${phone}`
    })
  },

  /**
   * 退出账号
   */
  logout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出账号吗？',
      success(res) {
        if (res.confirm) {
          app.logout()
        }
      }
    })
  }
})


