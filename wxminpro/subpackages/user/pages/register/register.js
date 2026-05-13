// ============================================
// 用户注册页面
// ============================================
// 功能：新用户注册功能，支持手机号、用户名、性别、生日、密码、头像等信息
// 路径：subpackages/user/pages/register/register.js
// 说明：注册成功后跳转到登录页面

// ============================================
// 1. 导入依赖
// ============================================
const { post, uploadFile } = require('../../../../utils/request.js')  // 导入请求工具
const apiConfig = require('../../../../config/api.js')  // 导入API配置

// ============================================
// 2. 页面定义
// ============================================
Page({

  /**
   * 页面的初始数据
   * ==============
   * 说明：定义页面中使用的所有数据变量
   */
  data: {
    jin: true,              // 注册按钮是否禁用（true=禁用，false=可用）
    Phone: '',              // 手机号
    UserName: '',          // 用户名
    Gender: '',            // 性别（'男'或'女'）
    Birthday: '',          // 出生日期（格式：YYYY-MM-DD）
    Password: '',          // 密码
    RegisterTime: '',      // 注册时间（由后端生成）
    FaceImg: '',           // 头像路径
    Filename: '',          // 头像文件名
    Path: '',              // 头像文件临时路径
    RegisterAnswer: '',    // 注册结果提示信息
    Code: '',              // 验证码
    codeCountdown: 0,      // 验证码倒计时（秒）
    codeTimer: null,       // 验证码倒计时定时器
  },
 
  /**
   * 手机号输入框监听
   * ================
   * 功能：监听手机号输入，实时更新数据并控制注册按钮状态
   * 说明：只有当所有必填字段都不为空时，注册按钮才可用
   */
  PhoneInput: function(e){
    var val = e.detail.value;  // 获取输入框的值
    
    // 更新手机号数据
    this.setData({
      Phone: val
    })
    
    // 检查所有必填字段是否都已填写
    if (this.data.Phone != '' && this.data.UserName != '' && 
        this.data.Gender != '' && this.data.Birthday != '' && 
        this.data.Password != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },

  /**
   * 用户名输入框监听
   * ================
   * 功能：监听用户名输入，实时更新数据并控制注册按钮状态
   */
  UsernameInput: function(e){
    var val = e.detail.value;  // 获取输入框的值
    
    // 更新用户名数据
    this.setData({
      UserName: val
    })
    
    // 检查所有必填字段是否都已填写（包括验证码）
    if(this.data.Phone != '' && this.data.UserName != '' && 
       this.data.Gender != '' && this.data.Birthday != '' && 
       this.data.Password != '' && this.data.Code != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },
 
  /**
   * 性别选择器监听
   * ==============
   * 功能：监听性别选择，实时更新数据并控制注册按钮状态
   * 说明：通常通过picker组件选择（'男'或'女'）
   */
  GenderInput: function(e){
    var val = e.detail.value;  // 获取选择的值
    
    // 更新性别数据
    this.setData({
      Gender: val
    })
 
    // 检查所有必填字段是否都已填写（包括验证码）
    if (this.data.Phone != '' && this.data.Birthday != '' && 
        this.data.Gender != '' && this.data.Password != '' && this.data.Code != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },
 
  /**
   * 出生日期选择器监听
   * ==================
   * 功能：监听出生日期选择，实时更新数据并控制注册按钮状态
   * 说明：通常通过picker组件选择日期（格式：YYYY-MM-DD）
   */
  BirthdayInput: function(e){
    var val = e.detail.value;  // 获取选择的日期
    
    // 更新出生日期数据
    this.setData({
      Birthday: val
    })
    
    // 检查所有必填字段是否都已填写（包括验证码）
    if(this.data.Phone != '' && this.data.UserName != '' && 
       this.data.Gender != '' && this.data.Birthday != '' && 
       this.data.Password != '' && this.data.Code != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },

  /**
   * 选择头像图片
   * ============
   * 功能：从相册或相机选择头像图片
   * 说明：选择后保存文件路径，在注册时上传
   */
  FaceImgInput: function(){
    var that = this;  // 保存this引用
    
    // 调用微信API选择图片
    wx.chooseImage({
      count: 1,                              // 最多选择1张图片
      sizeType: ['original', 'compressed'],  // 可以同时选择原图和压缩图
      sourceType: ['album', 'camera'],       // 可以从相册选择或拍照
      success (res) {
        // 选择成功回调
        const tempFilePaths = res.tempFiles;  // 获取文件对象数组
        var size = res.tempFiles[0].size;     // 文件大小
        var path1 = res.tempFiles[0].path     // 文件路径（格式：http://tmp/...）
        // 从路径中提取文件名（从第11个字符开始，跳过"http://tmp/"）
        var filename1 = path1.slice(11)
        
        console.log('res.tempFiles[0]:', res.tempFiles[0])
        console.log('size:', size)
        console.log('path:', path1)
        console.log('filename:', filename1)
        
        // 保存文件信息到页面数据
        that.setData({
          Path: res.tempFiles[0].path,  // 将文件路径保存在页面变量上，方便后续上传
          Filename: filename1           // 渲染到wxml，方便用户知道自己选择了什么文件
        })
        
        console.log("======  要上传的头像文件的路径  =============")
        console.log('Path:', that.data.Path)
        console.log("======  要上传的头像文件名  =============")
        console.log('Filename:', that.data.Filename)
        console.log('临时路径', tempFilePaths)
      }
    })
  },



// 选择要运行的C库文件
SelectImgFile:function(){
  var that=this//保留vue实例
  wx.chooseMessageFile({
    count: 1,//限制选择的文件数量
    // type: 'file',//非图片和视频的文件,不选默认为all
    type: 'all',//非图片和视频的文件,不选默认为all
    extension:['png','.png'],//此处限制文件类型
    success (res) {
       const tempFilePaths = res.tempFiles
       var size = res.tempFiles[0].size;
       var path = res.tempFiles[0].path
       var filename = res.tempFiles[0].name;
       var newfilename = filename + "";  
       console.log('res.tempFiles[0]:',res.tempFiles[0])
       console.log('size:',size)
       console.log('path:',path)
       console.log('filename:',filename)
      //  if (size > 4194304||newfilename.indexOf(".c")==-1){ //限制了文件的大小和具体文件类型
      if (newfilename.indexOf(".png")==-1){ //限制具体文件类型
           console.log("======  1  =============")
           that.setData({Filename: filename})
           that.setData({msg:"文件格式必须为 .png，上传失败！"})
           console.log("文件格式必须为 .png ,上传失败！")
           return 'ERR'        
       }
       else{
        console.log("======  2  =============")
        that.setData({
            Path: res.tempFiles[0].path, //将文件的路径保存在页面的变量上,方便 wx.uploadFile调用
            Filename: filename           //渲染到wxml方便用户知道自己选择了什么文件
           })
           console.log('Path:',that.data.Path)
           console.log('Filename:',that.data.Filename)
           console.log('临时路径',tempFilePaths)
           return '0'

       }
      } // end of  success of   wx.chooseMessageFile  
  }) // end of  wx.chooseMessageFile（）
},  // End of  SelectFile()

///////////////////////////////////////////////

  /**
   * 密码输入框监听
   * ==============
   * 功能：监听密码输入，实时更新数据并控制注册按钮状态
   */
  PasswordInput: function(e){
    var val = e.detail.value;  // 获取输入框的值
    
    // 更新密码数据
    this.setData({
      Password: val
    })
    
    // 检查所有必填字段是否都已填写（包括验证码）
    if(this.data.Phone != '' && this.data.UserName != '' && 
       this.data.Gender != '' && this.data.Birthday != '' && 
       this.data.Password != '' && this.data.Code != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },

  /**
   * 验证码输入框监听
   * ================
   * 功能：监听验证码输入，实时更新数据并控制注册按钮状态
   */
  CodeInput: function(e){
    var val = e.detail.value.replace(/\D/g, '');  // 只允许数字
    var code = val.slice(0, 6);  // 限制6位
    
    // 更新验证码数据
    this.setData({
      Code: code
    })
    
    // 检查所有必填字段是否都已填写
    if(this.data.Phone != '' && this.data.UserName != '' && 
       this.data.Gender != '' && this.data.Birthday != '' && 
       this.data.Password != '' && this.data.Code != ''){
      this.setData({
        jin: false  // 启用注册按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用注册按钮
      })
    }
  },

  /**
   * 获取验证码
   * ==========
   * 功能：向服务器请求发送验证码到用户手机
   */
  getCode: function() {
    const that = this;
    const { Phone, codeCountdown } = this.data;

    // 验证手机号格式
    if (!Phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(Phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 如果正在倒计时，不允许重复获取
    if (codeCountdown > 0) {
      return;
    }

    // 发送获取验证码请求
    post(apiConfig.endpoints.getCode, {
      Phone: Phone
    }, {
      showLoading: true,
      loadingText: '发送中...',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      }
    }).then(res => {
      console.log("获取验证码响应：", res);
      
      if (res === '0' || res === 0) {
        wx.showToast({
          title: '验证码发送失败',
          icon: 'none',
          duration: 2000
        });
        return;
      }

      // 验证码发送成功，开始倒计时
      wx.showToast({
        title: '验证码已发送',
        icon: 'success',
        duration: 2000
      });

      // 开始60秒倒计时
      that.setData({ codeCountdown: 60 });
      
      const timer = setInterval(() => {
        const countdown = that.data.codeCountdown - 1;
        if (countdown <= 0) {
          clearInterval(timer);
          that.setData({ 
            codeCountdown: 0,
            codeTimer: null
          });
        } else {
          that.setData({ codeCountdown: countdown });
        }
      }, 1000);

      that.setData({ codeTimer: timer });
    }).catch(err => {
      console.error("获取验证码失败：", err);
      wx.showToast({
        title: '获取验证码失败',
        icon: 'none',
        duration: 2000
      });
    });
  },
 
  // UploadImgFile:function(){
  //   var that = this ;
  //   // var val = this.data.Phone
  //   // var regExp = /^1[3456789]\d{9}$/; // 定义手机号格式的正则表达式 
  //   // if (regExp.test(val)) { 
  //   //   var  PhoneBJ ='1'  // 符合手机号格式要求
  //   //   // return true; 
  //   // } else {
  //   //   var  PhoneBJ ='0' 
  //   //   wx.showModal({
  //   //     title: '提示',
  //   //     content: '手机号格式不正确！',
  //   //     success (res) {
  //   //       if (res.confirm) {
  //   //         console.log('手机号格式不正确 用户点击确定')
  //   //       } else if (res.cancel) {
  //   //         console.log('手机号格式不正确 用户点击取消')
  //   //       }
  //   //     }
  //   //   }) 
  //   //     return false; // 不符合手机号格式要求
  //   // }
  //   var PhoneBJ='1'
  //   if (PhoneBJ=='1' ){
  //     // 上传头像文件
  //     console.log(" begin x.uploadFile........")     
  //      wx.uploadFile({
  //         url: 'http://127.0.0.1:5000/api/ReceiveFaceImg',  //请求数据接口地址,         
  //         filePath: that.data.Path,  //要上传的文件的路径  filePath: tempFilePaths[0].path,   //要上传的文件的路径
  //         name: 'file',
  //         header: {
  //            "Content-Type": "multipart/form-data"
  //          },
  //         formData: {
  //              method: 'POST'
  //          },
  //         success: function (res) {                    
  //             // 获取后端 返回的上传的图像路径，保存在FaceImg中
  //             // that.setData({FaceImg:res.data.user_FaceImg})  
  //             var  myFaceImg ="/static/icon/FaceImg/" + that.data.Filename
  //             // that.setData({FaceImg:res.data.user_FaceImg})  
  //             that.setData({FaceImg:myFaceImg})  
  //             console.log(res.data)
  //             console.log("上传成功")    
  //             console.log("图像路径如下：") 
  //             console.log(myFaceImg)
  //            }
  //      })  //end of  wx.uploadFile
  //     }
  // },



  /**
   * 注册提交
   * ========
   * 功能：向服务器发送注册请求，创建新用户账号
   * 流程：
   *   1. 验证手机号格式
   *   2. 上传头像（如果有）
   *   3. 发送注册请求
   *   4. 处理响应结果
   *   5. 注册成功：跳转到登录页面
   *   6. 注册失败：显示错误提示
   */
  Post: function(){
    var that = this;
    
    // ============================================
    // 1. 验证手机号格式
    // ============================================
    var val = this.data.Phone
    var regExp = /^1[3456789]\d{9}$/;  // 手机号格式正则表达式（11位，以1开头，第二位为3-9）
    
    if (regExp.test(val)) { 
      var PhoneBJ = '1'  // 符合手机号格式要求
    } else {
      var PhoneBJ = '0'  // 不符合格式
      wx.showModal({
        title: '提示',
        content: '手机号格式不正确！',
        success (res) {
          if (res.confirm) {
            console.log('手机号格式不正确 用户点击确定')
          } else if (res.cancel) {
            console.log('手机号格式不正确 用户点击取消')
          }
        }
      })
      return false;  // 不符合手机号格式要求，直接返回
    }

    // ============================================
    // 1.1 验证验证码
    // ============================================
    if (!this.data.Code) {
      wx.showToast({
        title: '请输入验证码',
        icon: 'none',
        duration: 2000
      });
      return false;
    }

    if (this.data.Code.length !== 6) {
      wx.showToast({
        title: '验证码为6位数字',
        icon: 'none',
        duration: 2000
      });
      return false;
    }

    // ============================================
    // 2. 上传头像文件（如果有）
    // ============================================
    if (PhoneBJ == '1'){
      console.log(" begin wx.uploadFile........")
      
      // 如果有头像文件，先上传头像；否则使用默认头像
      const uploadPromise = that.data.Path ? uploadFile(
        that.data.Path,                           // 头像文件路径
        apiConfig.endpoints.receiveFaceImg,       // 上传接口
        { method: 'POST' },                       // 请求方法
        { name: 'file' }                          // 文件字段名
      ).then(res => {
        // 上传成功
        console.log("头像上传成功：", res);
        const myFaceImg = res.user_FaceImg || "/static/image/header.png";  // 使用服务器返回的路径或默认路径
        that.setData({ FaceImg: myFaceImg });
        console.log("图像路径如下：", myFaceImg);
        return myFaceImg;
      }).catch(err => {
        // 上传失败，使用默认头像继续注册
        console.error("头像上传失败：", err);
        that.setData({ FaceImg: "/static/image/header.png" });
        return "/static/image/header.png";
      }) : Promise.resolve("/static/image/header.png");  // 没有头像文件，直接使用默认头像

      // ============================================
      // 3. 上传头像后，保存注册信息
      // ============================================
      uploadPromise.then((faceImg) => {
        console.log(" begin 保存注册信息 wx.request........");
        
        // 发送注册请求
        return post(apiConfig.endpoints.register, {
          Phone: that.data.Phone,        // 手机号
          UserName: that.data.UserName,  // 用户名
          Gender: that.data.Gender,      // 性别
          Birthday: that.data.Birthday,  // 出生日期
          Password: that.data.Password,  // 密码
          FaceImg: faceImg,              // 头像路径
          Code: that.data.Code,          // 验证码
        }, {
          showLoading: true,             // 显示加载提示
          loadingText: '注册中...',       // 加载提示文字
          header: {
            'content-type': 'application/x-www-form-urlencoded'  // 使用form格式
          }
        });
      }).then(res => {
        // ============================================
        // 4. 处理注册响应结果
        // ============================================
        console.log("====================  1 ====================");
        console.log(res);
        console.log("==================== 2 ====================");
        console.log("====================  3 ====================");
        
        if (res === '0') {
          // ============================================
          // 注册成功
          // ============================================
          that.setData({ RegisterAnswer: "注册成功" });
          console.log("====================  0  ok ====================");
          console.log("注册成功");
          
          wx.showToast({
            title: '注册成功',
            icon: 'success',
            duration: 2000
          });
          
          // 延迟1.5秒后跳转到登录页面
          setTimeout(() => {
            wx.navigateTo({
              url: '/subpackages/user/pages/login/login',
            });
          }, 1500);
          return true;
        } else if (res === '1') {
          // ============================================
          // 手机号已注册
          // ============================================
          that.setData({ RegisterAnswer: "该手机号已经注册过" });
          console.log("===========  1  该手机号已经注册过=================");
          console.log("该手机号已经注册过！");
          
          wx.showToast({
            title: '该手机号已注册',
            icon: 'none',
            duration: 2000
          });
          return false;
        } else if (res === '2') {
          // ============================================
          // 注册失败（数据库错误）
          // ============================================
          that.setData({ RegisterAnswer: "无法保存注册信息，注册失败!" });
          console.log("====================  2  保存出错===================");
          console.log("注册失败！");
          
          wx.showToast({
            title: '注册失败，请重试',
            icon: 'none',
            duration: 2000
          });
          return false;
        }
      }).catch(err => {
        // 请求失败（网络错误等）
        console.error("注册失败：", err);
        // 错误提示已在 request.js 中处理
      }); 
    } else {
      // ============================================
      // 手机号格式不正确
      // ============================================
      that.setData({RegisterAnswer: "手机格式不正确!"})
      console.log("手机格式不正确，注册失败！");    
      return false
    }
  },
  
  /**
   * 跳转到登录页面
   * ==============
   * 功能：导航到登录页面
   */
  Login: function(){
    wx.navigateTo({
      url: '/pages/login/login',
    })
  },

  /**
   * 跳转到注册页面
   * ==============
   * 功能：导航到注册页面（当前页面，可能未使用）
   */
  Register: function(){
    wx.navigateTo({
      url: '/subpackages/user/pages/register/register',
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
    // 清除验证码倒计时定时器
    if (this.data.codeTimer) {
      clearInterval(this.data.codeTimer);
      this.setData({ codeTimer: null });
    }
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