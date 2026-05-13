// pages/loginout/loginout.js

Page({

  // 解决了注销后登录，用户登录类型不能改变的问题
  logout: function() {
    // 实际应用中，这里可以包含向服务器发送注销请求的代码
    wx.showToast({
      title: '注销成功',
      icon: 'success',
      duration: 2000,
      success: function() {
        // 注销成功后的操作，比如跳转到登录页面
        setTimeout(() => {
          
         wx.reLaunch({    //关闭所有页面，打开应用内的某一个页面。跳转后左上角出现返回首页，再次登录，用户类型控制正常
          // url: '/subpackages/user/pages/login/login' ,
          url: '/subpackages/audio/pages/LoginAudio/LoginAudio', // 需要跳转到的页面路径，路径后可以带参数
      
            });
          
        }, 2000);
      }
    });


  },
  goBack: function() {
    wx.navigateBack({
      delta: 1 // 返回上一级页面
    });
  }
});


