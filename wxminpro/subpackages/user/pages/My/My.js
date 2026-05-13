// pages/My/My.js
const { post } = require('../../../utils/request.js')
const apiConfig = require('../../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    listData: [],
    loading: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function() {
    console.log('onLoad - 浏览用户页面');
    // 页面加载时自动获取用户列表
    this.EditUser();
  },

  /**
   * 获取用户列表
   */
  EditUser: function() {
    const that = this;
    
    // 如果正在加载，不允许重复请求
    if (that.data.loading) {
      return;
    }

    that.setData({ loading: true });

    post(apiConfig.endpoints.editUser, {}, {
      showLoading: true,
      loadingText: '加载中...',
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      that.setData({ loading: false });
      
      console.log("====== 后端返回的注册用户表（users）信息 =======");
      console.log(res);
      
      // 确保返回的是数组
      const userList = Array.isArray(res) ? res : [];
      
      that.setData({
        listData: userList
      });
      
      if (userList.length === 0) {
        wx.showToast({
          title: '暂无用户数据',
          icon: 'none',
          duration: 2000
        });
      } else {
        wx.showToast({
          title: `加载成功，共${userList.length}位用户`,
          icon: 'success',
          duration: 2000
        });
      }
    }).catch(err => {
      that.setData({ loading: false });
      console.error("获取用户列表失败：", err);
      // 错误已在 request.js 中处理
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 页面显示时刷新用户列表
    this.EditUser();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {},

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {},

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {
    // 下拉刷新
    this.EditUser();
    wx.stopPullDownRefresh();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {}
});
