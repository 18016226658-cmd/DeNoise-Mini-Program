// pages/upload/upload.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
     imageList:["/static/image/ala.jpg","/static/image/header.png"]
  },
  uploadimage:function(){
    var  that = this
    wx.chooseImage({
      count: 9,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success (res) {
        // tempFilePath可以作为img标签的src属性显示图片
        // const tempFilePaths = res.tempFilePaths
        // console.log(res.tempFilePaths)
        that.setData({
          // 直接替换，原来的图片没有了
          // imageList:res.tempFilePaths 
          // 拼接在一起
          imageList:that.data.imageList.concat( res.tempFilePaths) 
        })
      }
    })

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