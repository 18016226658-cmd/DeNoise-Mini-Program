// pages/CreateDialo/createDialo.js
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    Answer:[] ,
    Birthday:[],
    ChatTime:[],
    Gender:[],
    NL:[],
    Question:[],
    UserName:[],
    Year:[],
    DD:[],
    listData:[],
    loading: false,
    // listData: [
    //   {  "UserName":"张三", "Gender": "男", "Birthday": "2018年4月19日","NL":20 },
    //   {  "UserName":"李四", "Gender": "女", "Birthday": "2018年4月17日","NL":21 },
     
    //   { "UserName": "王五", "Gender": "男", "Birthday": "2018年4月16日" ,"NL":22},
    //   {  "UserName": "赵六", "Gender": "女", "Birthday": "2018年4月15日","NL":23 }
    //  ]
    
  },

  onLoad: function () {
   console.log('onLoad')
  },

  CreateDialo:function(){
    let that=this;
    
    // 显示加载状态
    that.setData({
      loading: true,
      listData: []
    });
    
    post(apiConfig.endpoints.createDialo, {}, {
      showLoading: true,
      loadingText: '生成中...',
      timeout: 30000
    }).then(res => {
      console.log("生成数据集成功:", res)
      
      const listData = Array.isArray(res) ? res : [];
      that.setData({
        listData: listData,
        loading: false
      });
      
      if (listData.length > 0) {
        wx.showToast({
          title: `成功生成 ${listData.length} 条记录`,
          icon: 'success',
          duration: 2000
        });
      } else {
        wx.showToast({
          title: '生成失败，请重试',
          icon: 'none',
          duration: 2000
        });
      }
    }).catch(err => {
      console.error("生成数据集失败:", err);
      that.setData({
        loading: false
      });
      // 错误已在 request.js 中处理
    })
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