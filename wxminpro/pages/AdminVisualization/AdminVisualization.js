// pages/AdminVisualization/AdminVisualization.js
// ============================================
// 管理员可视化界面
// ============================================
// 功能：显示降噪数据统计图表（仅管理员可见）

const app = getApp()
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    userType: 2,
    loading: false,
    // 当前展示的图表类型：date/week/time/user
    currentChart: 'date',
    // 图表图片路径（由后端生成）
    chartImages: {
      dateImage: '',
      weekImage: '',
      timeImage: '',
      userImage: ''
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const userInfo = app.globalData.userInfo
    if (userInfo) {
      const userType = userInfo.UserType || userInfo.user_UserType || 2
      if (userType !== 1) {
        wx.showToast({
          title: '仅管理员可访问',
          icon: 'none',
          duration: 2000
        })
        setTimeout(() => {
          wx.switchTab({
            url: '/pages/home/home'
          })
        }, 2000)
        return
      }
      this.setData({ userType: userType })
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
      return
    }
    
    // 加载图表图片路径
    this.loadChartImages()
  },

  /**
   * 加载图表图片路径
   */
  loadChartImages() {
    const that = this
    that.setData({ loading: true })

    // 直接使用后端生成的图片路径（后端启动时已自动生成）
    const baseURL = apiConfig.baseURL
    const timestamp = Date.now() // 添加时间戳防止缓存
    
    const chartImages = {
      dateImage: `${baseURL}/static/visualization/date_line.png?t=${timestamp}`,
      weekImage: `${baseURL}/static/visualization/week_pie.png?t=${timestamp}`,
      timeImage: `${baseURL}/static/visualization/time_line.png?t=${timestamp}`,
      userImage: `${baseURL}/static/visualization/user_bar.png?t=${timestamp}`
    }
    
    // 生成所有图片URL数组（用于预览）
    const allImageUrls = [
      chartImages.dateImage,
      chartImages.weekImage,
      chartImages.timeImage,
      chartImages.userImage
    ]
    
    that.setData({ 
      chartImages: chartImages,
      allImageUrls: allImageUrls,
      loading: false 
    })
    
    console.log('图表图片路径已加载：', chartImages)
  },

  // 切换图表按钮
  showDateChart() {
    this.setData({ currentChart: 'date' })
  },
  showWeekChart() {
    this.setData({ currentChart: 'week' })
  },
  showTimeChart() {
    this.setData({ currentChart: 'time' })
  },
  showUserChart() {
    this.setData({ currentChart: 'user' })
  },

  /**
   * 预览图片（点击图片可全屏查看，支持双指缩放）
   */
  previewImage(e) {
    const currentUrl = e.currentTarget.dataset.url
    // dataset 中的 data-urls 只支持字符串，这里统一使用 data 里的 allImageUrls，
    // 保证传给 wx.previewImage 的始终是字符串数组
    const urls = (this.data.allImageUrls && this.data.allImageUrls.length > 0)
      ? this.data.allImageUrls
      : [currentUrl]

    wx.previewImage({
      current: currentUrl, // 当前显示图片的http链接
      urls: urls // 需要预览的图片http链接列表
    })
  },

  /**
   * 重新生成可视化图表
   */
  /**
   * 重新生成可视化图表
   */
  regenerateCharts() {
    const that = this
    
    wx.showLoading({
      title: '生成图表中...',
      mask: true
    })
    
    post(apiConfig.endpoints.regenerateVisualization || '/api/regenerateVisualization', {}, {
      showLoading: false, // 手动控制loading
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      wx.hideLoading()
      
      // 兼容后端返回格式
      let result = res
      if (typeof res === 'string') {
        try {
          result = JSON.parse(res)
        } catch (e) {
          console.error('解析响应失败：', e)
        }
      }
      
      if (result && result.success) {
        // 更新图片路径（使用新的时间戳）
        const baseURL = apiConfig.baseURL
        const timestamp = Date.now()
        
        // 后端返回的是相对路径（例如：/static/visualization/date_line.png?t=xxx）
        // 这里统一补上 baseURL，避免小程序把它当成本地资源导致加载失败
        const serverData = (result && result.data) || {}
        const chartImages = {
          dateImage: serverData.dateImage
            ? `${baseURL}${serverData.dateImage}`
            : `${baseURL}/static/visualization/date_line.png?t=${timestamp}`,
          weekImage: serverData.weekImage
            ? `${baseURL}${serverData.weekImage}`
            : `${baseURL}/static/visualization/week_pie.png?t=${timestamp}`,
          timeImage: serverData.timeImage
            ? `${baseURL}${serverData.timeImage}`
            : `${baseURL}/static/visualization/time_line.png?t=${timestamp}`,
          userImage: serverData.userImage
            ? `${baseURL}${serverData.userImage}`
            : `${baseURL}/static/visualization/user_bar.png?t=${timestamp}`
        }
        
        const allImageUrls = [
          chartImages.dateImage,
          chartImages.weekImage,
          chartImages.timeImage,
          chartImages.userImage
        ]
        
        that.setData({
          chartImages: chartImages,
          allImageUrls: allImageUrls
        })
        
        wx.showToast({
          title: '图表已更新',
          icon: 'success',
          duration: 2000
        })
      } else {
        wx.showToast({
          title: (result && result.message) || '生成失败',
          icon: 'none',
          duration: 2000
        })
      }
    }).catch(err => {
      wx.hideLoading()
      console.error("重新生成图表失败：", err)
      wx.showToast({
        title: '生成失败，请重试',
        icon: 'none',
        duration: 2000
      })
    })
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    // 重新加载图表图片（添加新的时间戳）
    this.loadChartImages()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  }
})


