// pages/separateAudio/separateAudio.js
const apiConfig = require('../../../../config/api.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    audioPath: '',
    orgFileName: '',
    fileSize: '0.00',
    duration: '00:00:00',
    title: '',
    artist: '',
    vocalsPath: '',
    otherPath: ''
  },

  // 选择音频文件
  chooseAudio() {
    const that = this
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['WAV', 'wav', 'mp3', 'ogg'],
      success(res) {
        const tempFilePath = res.tempFiles[0].path
        const orgFileName = res.tempFiles[0].name
        that.setData({
          audioPath: tempFilePath,
          orgFileName: orgFileName
        })
        wx.showToast({
          title: '文件选择成功',
          icon: 'success'
        })
      },
      fail(err) {
        console.error('选择文件失败', err)
        wx.showToast({
          title: '选择文件失败',
          icon: 'none'
        })
      }
    })
  },

  // 分离音频
  separateAudio() {
    if (!this.data.audioPath) {
      wx.showToast({
        title: '请先选择音频文件',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '分离中...',
      mask: true
    })

    // 这里调用后端API进行音频分离
    wx.request({
      url: apiConfig.baseURL + apiConfig.endpoints.separateAudio,
      method: 'POST',
      header: {
        'content-type': 'application/json'  // 明确指定JSON格式
      },
      data: {
        audioPath: this.data.audioPath
      },
      success: (res) => {
        wx.hideLoading()
        if (res.statusCode === 200) {
          this.setData({
            vocalsPath: res.data.vocalsPath || '',
            otherPath: res.data.otherPath || ''
          })
          wx.showToast({
            title: '分离成功',
            icon: 'success'
          })
        } else {
          wx.showToast({
            title: '分离失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('分离失败', err)
        wx.showToast({
          title: '分离失败',
          icon: 'none'
        })
      }
    })
  },

  // 下载人声
  downloadVocals() {
    if (this.data.vocalsPath) {
      wx.showToast({
        title: '下载功能开发中',
        icon: 'none'
      })
    }
  },

  // 下载伴奏
  downloadOther() {
    if (this.data.otherPath) {
      wx.showToast({
        title: '下载功能开发中',
        icon: 'none'
      })
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})