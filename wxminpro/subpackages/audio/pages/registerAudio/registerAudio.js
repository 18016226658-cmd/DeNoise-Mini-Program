// pages/registerAudio/registerAudio.js
const { post, uploadFile } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    jin: true, // 控制注册按钮是否禁用
    registering: false, // 是否正在注册
    
    Phone: '',
    UserName: '',
    Gender: '',
    genderArray: ['男', '女'], // 性别选项数组
    genderIndex: 0, // 性别选择器索引
    Birthday: '',
    maxDate: '', // 最大日期（今天）
    Password: '',
    RegisterTime: '',
    FaceImg: '',
    Filename: '',
    Path: '',
    RegisterAnswer: '',
    
    MaxSepTimes: '',
    CurSepTimes: '',
    MaxNoiseTimes: '',
    CurNoiseTimes: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 设置最大日期为今天
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    this.setData({
      maxDate: `${year}-${month}-${day}`
    });
  },

  /**
   * 检查所有必填项是否已填写
   */
  checkFormComplete() {
    const { Phone, UserName, Gender, Birthday, Password } = this.data;
    if (Phone && UserName && Gender && Birthday && Password) {
      this.setData({ jin: false });
    } else {
      this.setData({ jin: true });
    }
  },

  /**
   * 手机号输入
   */
  PhoneInput: function(e) {
    const phone = e.detail.value.replace(/\D/g, ''); // 只允许数字
    this.setData({ Phone: phone });
    this.checkFormComplete();
  },

  /**
   * 用户名输入
   */
  UsernameInput: function(e) {
    const username = e.detail.value;
    this.setData({ UserName: username });
    this.checkFormComplete();
  },

  /**
   * 性别选择器改变
   */
  GenderChange: function(e) {
    const index = parseInt(e.detail.value);
    const gender = this.data.genderArray[index];
    this.setData({
      Gender: gender,
      genderIndex: index
    });
    this.checkFormComplete();
  },

  /**
   * 出生日期选择器改变
   */
  BirthdayChange: function(e) {
    const birthday = e.detail.value;
    this.setData({ Birthday: birthday });
    this.checkFormComplete();
  },

  /**
   * 密码输入
   */
  PasswordInput: function(e) {
    const password = e.detail.value;
    this.setData({ Password: password });
    this.checkFormComplete();
  },

  /**
   * 选择头像文件
   */
  SelectImgFile: function() {
    const that = this;
    wx.chooseMessageFile({
      count: 1,
      type: 'all',
      extension: ['png', '.png'],
      success(res) {
        const tempFilePaths = res.tempFiles;
        const size = res.tempFiles[0].size;
        const path = res.tempFiles[0].path;
        const filename = res.tempFiles[0].name;
        
        console.log('选择的文件信息：', {
          size: size,
          path: path,
          filename: filename
        });

        // 检查文件格式
        if (filename.indexOf(".png") === -1) {
          that.setData({ Filename: filename });
          wx.showToast({
            title: '文件格式必须为.png',
            icon: 'none',
            duration: 2000
          });
          return;
        }

        // 保存文件路径和文件名
        that.setData({
          Path: res.tempFiles[0].path,
          Filename: filename
        });
        
        console.log('头像文件路径：', that.data.Path);
        console.log('头像文件名：', that.data.Filename);
      },
      fail(err) {
        console.error('选择头像文件失败：', err);
        wx.showToast({
          title: '选择文件失败',
          icon: 'none',
          duration: 2000
        });
      }
    });
  },

  /**
   * 注册
   */
  Post: function() {
    const that = this;
    const { Phone, UserName, Gender, Birthday, Password, Path } = this.data;

    // 输入验证
    if (!Phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    const regExp = /^1[3456789]\d{9}$/;
    if (!regExp.test(Phone)) {
      wx.showModal({
        title: '提示',
        content: '手机号格式不正确！',
        showCancel: false,
        confirmText: '确定'
      });
      return;
    }

    if (!UserName) {
      wx.showToast({
        title: '请输入用户名',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!Gender) {
      wx.showToast({
        title: '请选择性别',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!Birthday) {
      wx.showToast({
        title: '请选择出生日期',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!Password) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 如果正在注册，不允许重复提交
    if (that.data.registering) {
      return;
    }

    that.setData({ 
      registering: true,
      RegisterAnswer: ''
    });
    wx.showLoading({
      title: '注册中...',
      mask: true
    });

    // 先上传头像文件（如果有）
    const uploadPromise = Path ? uploadFile(
      Path,
      apiConfig.endpoints.receiveFaceImg,
      { method: 'POST' },
      { name: 'file' }
    ).then(res => {
      console.log("头像上传成功：", res);
      const myFaceImg = res.user_FaceImg || "/static/image/header.png";
      that.setData({ FaceImg: myFaceImg });
      console.log("图像路径：", myFaceImg);
      return myFaceImg;
    }).catch(err => {
      console.error("头像上传失败：", err);
      // 即使上传失败，也使用默认头像继续注册
      that.setData({ FaceImg: "/static/image/header.png" });
      return "/static/image/header.png";
    }) : Promise.resolve("/static/image/header.png");

    // 上传头像后，保存注册信息
    uploadPromise.then((faceImg) => {
      console.log("开始保存注册信息...");
      
      return post(apiConfig.endpoints.registerAudio, {
        Phone: Phone,
        UserName: UserName,
        Gender: Gender,
        Birthday: Birthday,
        Password: Password,
        FaceImg: faceImg,
      }, {
        showLoading: false, // 已经在外部显示
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }
      });
    }).then(res => {
      wx.hideLoading();
      that.setData({ registering: false });
      
      console.log("注册响应：", res);
      console.log("注册响应数据：", res);

      if (res === '0') {
        that.setData({ RegisterAnswer: "注册成功" });
        console.log("注册成功");
        
        wx.showToast({
          title: '注册成功',
          icon: 'success',
          duration: 2000
        });

        // 延迟跳转到登录页面
        setTimeout(() => {
          wx.navigateTo({
            url: '/subpackages/audio/pages/LoginAudio/LoginAudio',
          });
        }, 1500);
      } else if (res === '1') {
        that.setData({ RegisterAnswer: "该手机号已经注册过" });
        console.log("该手机号已经注册过！");
        wx.showToast({
          title: '该手机号已注册',
          icon: 'none',
          duration: 2000
        });
      } else if (res === '2') {
        that.setData({ RegisterAnswer: "无法保存注册信息，注册失败!" });
        console.log("注册失败！");
        wx.showToast({
          title: '注册失败，请重试',
          icon: 'none',
          duration: 2000
        });
      } else {
        that.setData({ RegisterAnswer: "注册失败，未知错误" });
        wx.showToast({
          title: '注册失败',
          icon: 'none',
          duration: 2000
        });
      }
    }).catch(err => {
      wx.hideLoading();
      that.setData({ registering: false });
      console.error("注册请求失败：", err);
      that.setData({ RegisterAnswer: "网络错误，请检查后端服务" });
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
  onShow() {},

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
