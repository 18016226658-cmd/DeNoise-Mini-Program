// pages/AdminVisualization/AdminVisualization.js
// ============================================
// 管理员可视化界面
// ============================================
// 功能：显示降噪数据统计图表（仅管理员可见）

const app = getApp()
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')
const echarts = require('../../../../ec-canvas/echarts.js')

let chartDate = null
let chartWeek = null
let chartTime = null
let chartUser = null

Page({
  /**
   * 页面的初始数据
   */
  data: {
    userType: 2,
    loading: false,
    // 图表数据
    dateData: [],      // 日期-降噪次数
    weekData: [],     // 周次-降噪次数
    timeData: [],     // 时间-降噪次数
    userData: [],     // 活跃用户-降噪次数
    // ECharts实例
    ecDate: {
      onInit: this.initDateChart.bind(this)
    },
    ecWeek: {
      onInit: this.initWeekChart.bind(this)
    },
    ecTime: {
      onInit: this.initTimeChart.bind(this)
    },
    ecUser: {
      onInit: this.initUserChart.bind(this)
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
          wx.navigateBack()
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
        wx.navigateBack()
      }, 2000)
      return
    }
    
    this.loadStatistics()
  },

  /**
   * 加载统计数据
   */
  loadStatistics() {
    const that = this
    that.setData({ loading: true })

    post(apiConfig.endpoints.getStatistics, {}, {
      showLoading: true,
      loadingText: '加载数据中...',
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      that.setData({ loading: false })
      
      console.log("统计数据：", res)
      
      // 处理数据
      if (res && res.data) {
        that.setData({
          dateData: res.data.dateData || [],
          weekData: res.data.weekData || [],
          timeData: res.data.timeData || [],
          userData: res.data.userData || []
        })
        
        // 更新图表
        that.updateCharts()
      }
    }).catch(err => {
      that.setData({ loading: false })
      console.error("获取统计数据失败：", err)
      wx.showToast({
        title: '加载数据失败',
        icon: 'none',
        duration: 2000
      })
    })
  },

  /**
   * 初始化日期折线图
   */
  initDateChart(canvas, width, height) {
    chartDate = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chartDate)
    return chartDate
  },

  /**
   * 初始化周次饼图
   */
  initWeekChart(canvas, width, height) {
    chartWeek = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chartWeek)
    return chartWeek
  },

  /**
   * 初始化时间折线图
   */
  initTimeChart(canvas, width, height) {
    chartTime = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chartTime)
    return chartTime
  },

  /**
   * 初始化用户柱状图
   */
  initUserChart(canvas, width, height) {
    chartUser = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chartUser)
    return chartUser
  },

  /**
   * 更新所有图表
   */
  updateCharts() {
    this.updateDateChart()
    this.updateWeekChart()
    this.updateTimeChart()
    this.updateUserChart()
  },

  /**
   * 更新日期折线图
   */
  updateDateChart() {
    const { dateData } = this.data
    const dates = dateData.map(item => item.date)
    const counts = dateData.map(item => item.count)

    const option = {
      title: {
        text: '日期-降噪次数',
        left: 'center',
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '降噪次数'
      },
      series: [{
        name: '降噪次数',
        type: 'line',
        data: counts,
        smooth: true,
        itemStyle: {
          color: '#6A5ACD'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: 'rgba(106, 90, 205, 0.3)'
            }, {
              offset: 1,
              color: 'rgba(106, 90, 205, 0.1)'
            }]
          }
        }
      }]
    }

    if (chartDate) {
      chartDate.setOption(option)
    }
  },

  /**
   * 更新周次饼图
   */
  updateWeekChart() {
    const { weekData } = this.data
    const data = weekData.map(item => ({
      value: item.count,
      name: item.week
    }))

    const option = {
      title: {
        text: '周次-降噪次数',
        left: 'center',
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle'
      },
      series: [{
        name: '降噪次数',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: data
      }]
    }

    if (chartWeek) {
      chartWeek.setOption(option)
    }
  },

  /**
   * 更新时间折线图
   */
  updateTimeChart() {
    const { timeData } = this.data
    const hours = timeData.map(item => item.hour + ':00')
    const counts = timeData.map(item => item.count)

    const option = {
      title: {
        text: '一天中时间-降噪次数',
        left: 'center',
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: hours,
        boundaryGap: false
      },
      yAxis: {
        type: 'value',
        name: '降噪次数'
      },
      series: [{
        name: '降噪次数',
        type: 'line',
        data: counts,
        smooth: true,
        itemStyle: {
          color: '#44ADFB'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: 'rgba(68, 173, 251, 0.3)'
            }, {
              offset: 1,
              color: 'rgba(68, 173, 251, 0.1)'
            }]
          }
        }
      }]
    }

    if (chartTime) {
      chartTime.setOption(option)
    }
  },

  /**
   * 更新用户柱状图
   */
  updateUserChart() {
    const { userData } = this.data
    const users = userData.map(item => item.userName || item.userId)
    const counts = userData.map(item => item.count)

    const option = {
      title: {
        text: '活跃用户-降噪次数',
        left: 'center',
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: users,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '降噪次数'
      },
      series: [{
        name: '降噪次数',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: '#6A5ACD'
            }, {
              offset: 1,
              color: '#44ADFB'
            }]
          }
        }
      }]
    }

    if (chartUser) {
      chartUser.setOption(option)
    }
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    this.loadStatistics()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  }
})

