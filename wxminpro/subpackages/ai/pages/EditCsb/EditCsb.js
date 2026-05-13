// pages/EditCsb/EditCsb.js
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({
   /**
   * 页面的初始数据
   */
  data: {
    MinYear: '',
    MaxYear: '',
    BL: '',
    ManN:'',
    WenmenN:'',
    ChatN: '',
    submitting: false,
  },

  onParamMinYearInput: function(e) {
    this.setData({
      MinYear: e.detail.value
    });
  },

  onParamMaxYearInput: function(e) {
    this.setData({
      MaxYear: e.detail.value
    });
  },

  onParamBLInput: function(e) {
    this.setData({
      BL: e.detail.value
    });
  },


onParamManNInput: function(e) {
  this.setData({
    ManN: e.detail.value
  });
},

onParamWenmenNInput: function(e) {
  this.setData({
    WenmenN: e.detail.value
  });
},

onParamChatNInput: function(e) {
  this.setData({
    ChatN: e.detail.value
  });
},


  onSubmit: function() {
    const { MinYear, MaxYear, BL, ManN, WenmenN, ChatN } = this.data;
    
    // 表单验证
    if (!MinYear || !MaxYear || !BL || !ManN || !WenmenN || !ChatN) {
      wx.showToast({
        title: '请填写所有参数',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 数值范围验证
    const minYear = parseInt(MinYear);
    const maxYear = parseInt(MaxYear);
    const bl = parseInt(BL);
    const manN = parseInt(ManN);
    const wenmenN = parseInt(WenmenN);
    const chatN = parseInt(ChatN);

    if (minYear < 10 || minYear > 30) {
      wx.showToast({
        title: '最小年龄应在10-30之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (maxYear < 30 || maxYear > 80) {
      wx.showToast({
        title: '最大年龄应在30-80之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (bl < 0 || bl > 100) {
      wx.showToast({
        title: '男女比例应在0-100之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (manN < 30 || manN > 50) {
      wx.showToast({
        title: '男性人数应在30-50之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (wenmenN < 30 || wenmenN > 50) {
      wx.showToast({
        title: '女性人数应在30-50之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (chatN < 2000 || chatN > 20000) {
      wx.showToast({
        title: '聊天记录数应在2000-20000之间',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 设置提交状态
    this.setData({
      submitting: true
    });

    post(apiConfig.endpoints.editCsb, {
      MinYear: minYear,
      MaxYear: maxYear,
      BL: bl,
      ManN: manN,
      WenmenN: wenmenN,
      ChatN: chatN,
    }, {
      showLoading: true,
      loadingText: '提交中...',
      timeout: 10000
    }).then(res => {
      this.setData({
        submitting: false
      });

      if (res && res.message) {
        wx.showToast({
          title: '提交成功',
          icon: 'success',
          duration: 2000
        });
      } else {
        wx.showToast({
          title: res?.error || '提交失败',
          icon: 'none',
          duration: 2000
        });
      }
    }).catch(err => {
      this.setData({
        submitting: false
      });
      console.error('提交失败：', err);
      // 错误已在 request.js 中处理
    });
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



});