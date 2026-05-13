// pages/history/history.js
const app = getApp()
const request = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

Page({
  data: {
    userInfo: {},
    historyList: [],
    loading: false,
    emptyText: '暂无历史记录'
  },

  onLoad() {
    this.getUserInfo()
    this.loadHistory()
  },

  onShow() {
    this.loadHistory()
  },

  // 获取用户信息
  getUserInfo() {
    const userInfo = app.globalData.userInfo
    if (userInfo) {
      this.setData({ userInfo })
    }
  },

  // 加载历史记录
  loadHistory() {
    const that = this
    this.setData({ loading: true })

    // 如果没有用户信息，直接显示空列表
    if (!this.data.userInfo || (!this.data.userInfo.Phone && !this.data.userInfo.UserID)) {
      this.setData({
        loading: false,
        historyList: [],
        emptyText: '请先登录'
      })
      return
    }

    const userType = this.data.userInfo.UserType || this.data.userInfo.user_UserType || 2

    request.post('/api/getDeNoiseHistory', {
      // 优先使用后端保存时使用的 UserID（例如管理员的 1001），
      // 如果没有再退回到手机号 Phone，确保能查到历史记录。
      UserID: this.data.userInfo.UserID || this.data.userInfo.Phone,
      UserType: userType, // 传给后端，用于管理员查看全部记录
    }, {
      showLoading: false,
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      // 处理响应数据：可能是 {success: true, data: [...]} 或直接是数组
      let historyList = []
      if (res && res.success !== false) {
        historyList = res.data || res || []
      } else if (Array.isArray(res)) {
        historyList = res
      }
      
      // 处理数据，确保字段完整
      historyList = historyList.map(item => {
        // 确保文件名字段
        if (!item.orgFileName && item.AudioName) {
          item.orgFileName = item.AudioName
        }
        // 确保时间字段
        if (!item.createTime && item.DeNoiseTime) {
          item.createTime = item.DeNoiseTime
        }
        // 确保用户名显示
        if (!item.UserName && item.userName) {
          item.UserName = item.userName
        }
        return item
      })
      
      that.setData({
        historyList: historyList,
        loading: false,
        emptyText: historyList.length === 0 ? '暂无历史记录' : '暂无历史记录'
      })
    }).catch(err => {
      console.error('加载历史记录失败：', err)
      that.setData({
        loading: false,
        historyList: [],
        emptyText: '后端服务未启动，请启动后端服务后重试'
      })
    })
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadHistory()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  },

  // 播放原始音频
  playOriginal(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.historyList[index]
    if (item && item.originalPath) {
      // 这里可以打开音频播放器
      wx.showToast({
        title: '开始播放',
        icon: 'none'
      })
    }
  },

  // 播放降噪音频
  playDenoised(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.historyList[index]
    if (item && item.deNoisePath) {
      // 这里可以打开音频播放器
      wx.showToast({
        title: '开始播放',
        icon: 'none'
      })
    }
  },

  // 下载降噪文件
  downloadFile(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.historyList[index]
    if (item && item.deNoisePath) {
      wx.showLoading({ title: '下载中...' })
      // 调用下载接口
      request.post('/api/DownloadDeNoise', {
        file_url: item.deNoisePath,
        filename: item.filename
      }).then(res => {
        wx.hideLoading()
        wx.showToast({
          title: '下载成功',
          icon: 'success'
        })
      }).catch(err => {
        wx.hideLoading()
        wx.showToast({
          title: '下载失败',
          icon: 'none'
        })
      })
    }
  }
})

