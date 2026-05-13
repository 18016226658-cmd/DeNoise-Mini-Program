// pages/chat/chat.js
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    // 用户注册信息
    UserID: 1001,
    UserName: '王小明',
    Gender: '男',
    Birthday: '2001-10-11',
    FaceImg: '/static/image/header.png',
    UserType: 3, // 注册用户类型  1：管理员   2：Vip用户   3：普通用户
    EditChatType: 1, // 用户聊天大模型的类型  1：文心一言   2：ChatGPT
    UserTypeText: '普通用户' // 用户类型文本
  },

  /**
   * 获取用户类型文本
   */
  getUserTypeText(userType) {
    const typeMap = {
      1: '管理员',
      2: 'VIP用户',
      3: '普通用户'
    };
    return typeMap[userType] || '普通用户';
  },

  /**
   * 浏览用户
   */
  DispUser: function() {
    wx.navigateTo({
      url: '/subpackages/user/pages/My/My',
    });
  },

  /**
   * 修改用户类型
   */
  EditUserType: function() {
    wx.navigateTo({
      url: '/subpackages/user/pages/EditUser/EditUser',
    });
  },

  /**
   * 删除用户
   */
  DelUser: function() {
    wx.navigateTo({
      url: '/subpackages/user/pages/DelUser/DelUser',
    });
  },

  /**
   * 修改仿真模型
   */
  EditCsb: function() {
    wx.navigateTo({
      url: '/subpackages/ai/pages/EditCsb/EditCsb',
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    console.log("==============userInfo==========  1111 ");
    const userInfo = app.globalData.userInfo;

    // 如果用户未登录，使用默认值
    if (!userInfo) {
      console.log('用户未登录，使用默认用户信息');
      wx.showToast({
        title: '请先登录',
        icon: 'none',
        duration: 2000
      });
      this.setData({
        userInfo: {},
        UserName: this.data.UserName || '王小明',
        UserID: this.data.UserID || 1001,
        Gender: this.data.Gender || '男',
        Birthday: this.data.Birthday || '2001-10-11',
        FaceImg: this.data.FaceImg || '/static/image/header.png',
        UserType: this.data.UserType || 3,
        UserTypeText: this.getUserTypeText(this.data.UserType || 3)
      });
      return;
    }

    // 用户已登录，使用实际用户信息
    const userType = userInfo.UserType || this.data.UserType || 3;
    this.setData({
      userInfo: userInfo,
      UserName: userInfo.UserName || userInfo.nickName || this.data.UserName || '王小明',
      Gender: userInfo.Gender || this.data.Gender || '男',
      Birthday: userInfo.Birthday || this.data.Birthday || '2001-10-11',
      UserID: userInfo.Phone || userInfo.UserID || this.data.UserID || 1001,
      FaceImg: userInfo.FaceImg || this.data.FaceImg || '/static/image/header.png',
      UserType: userType,
      UserTypeText: this.getUserTypeText(userType)
    });
    
    console.log("==============userInfo========== 22222");
    console.log(this.data.userInfo);
    console.log(this.data.UserType);
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 页面显示时刷新用户信息
    const userInfo = app.globalData.userInfo;
    if (userInfo) {
      const userType = userInfo.UserType || this.data.UserType || 3;
      this.setData({
        userInfo: userInfo,
        UserName: userInfo.UserName || userInfo.nickName || this.data.UserName,
        Gender: userInfo.Gender || this.data.Gender,
        Birthday: userInfo.Birthday || this.data.Birthday,
        UserID: userInfo.Phone || userInfo.UserID || this.data.UserID,
        FaceImg: userInfo.FaceImg || this.data.FaceImg,
        UserType: userType,
        UserTypeText: this.getUserTypeText(userType)
      });
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {},

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
  onPullDownRefresh() {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {}
});
