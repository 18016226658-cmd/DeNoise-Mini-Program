// ============================================
// 用户登录页面
// ============================================
// 功能：用户登录功能，支持手机号+密码登录
// 路径：subpackages/user/pages/login/login.js
// 说明：登录成功后保存用户信息到全局变量和本地文件

// ============================================
// 1. 导入依赖
// ============================================
const app = getApp()  // 获取小程序全局实例
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
    headerPath: "/static/image/header.png",  // 默认头像路径
    jin: true,                               // 登录按钮是否禁用（true=禁用，false=可用）
    Username: '',                            // 用户名
    Password: '',                            // 密码
    longin: true,                            // 登录状态（未使用）
    Phone: '',                               // 手机号
    Birthday: '',                            // 出生日期
    Gender: '',                              // 性别
    FaceImg: '',                             // 头像路径
    UserType: 3,                             // 用户类型（1-管理员，2-普通用户，3-游客）
    loginType: 'password',                   // 登录方式：'password'（密码登录）或'code'（验证码登录）
    Code: '',                                // 验证码
    codeCountdown: 0,                        // 验证码倒计时（秒）
    codeTimer: null,                        // 验证码倒计时定时器
  },
 
  /**
   * 选择头像图片
   * ============
   * 功能：从相册或相机选择头像图片，并上传到服务器
   * 说明：此功能在登录页面中可能未使用，保留用于后续扩展
   */
  SelectImg: function(){
    var that = this;  // 保存this引用，用于在回调中使用
    
    // 调用微信API选择图片
    wx.chooseImage({
      count: 1,                              // 最多选择1张图片
      sizeType: ['original', 'compressed'],  // 可以同时选择原图和压缩图
      sourceType: ['album', 'camera'],       // 可以从相册选择或拍照
      success (res) {
        // 选择成功回调
        // 注意：这里使用的是res.tempFiles（文件对象），而不是res.tempFilePaths（路径字符串）
        const tempFilePaths = res.tempFiles
        var size = res.tempFiles[0].size;     // 文件大小
        var path = res.tempFiles[0].path      // 文件路径
        var filename = res.tempFiles[0].name; // 文件名
        
        console.log('res.tempFiles[0]:', res.tempFiles[0])
        console.log('size:', size)
        console.log('path:', path)
        console.log('filename:', filename)

        // 保存文件信息到页面数据
        that.setData({
          path: res.tempFiles[0].path,  // 将文件路径保存在页面变量上，方便后续调用
          filename: filename             // 渲染到wxml，方便用户知道自己选择了什么文件
        })
        
        console.log('path:', path)
        console.log('filename:', filename)
        console.log('临时路径', tempFilePaths)
        
        // 上传文件到服务器
        uploadFile(
          tempFilePaths[0].path,                    // 文件路径
          apiConfig.endpoints.receiveFaceImg,       // 上传接口
          { method: 'POST' },                       // 请求方法
          { name: 'file' }                          // 文件字段名
        ).then(res => {
          // 上传成功
          var mydata = res
          that.setData({FileSrc: tempFilePaths[0].path})
          // 设置保存路径（本地路径，用于显示）
          that.setData({SaveFileSrc: "D:\\WxMinPro\\Static\\chatGPT\\FaceImg\\" + filename})
          that.setData({msg: "上传成功"})
          console.log(res)
          console.log("上传成功")
        }).catch(err => {
          // 上传失败
          console.error("上传失败：", err)
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          })
        })
      }
    })
  },



  /**
   * 切换登录方式
   * ============
   * 功能：在密码登录和验证码登录之间切换
   */
  switchLoginType: function(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({
      loginType: type,
      Password: '',
      Code: '',
      jin: true
    });
  },

  /**
   * 手机号输入框监听
   * ================
   * 功能：监听手机号输入，实时更新数据并控制登录按钮状态
   * 说明：根据登录方式，检查手机号和密码/验证码是否都不为空
   */
  PhoneInput: function(e){
    console.log(e)
    var val = e.detail.value.replace(/\D/g, '');  // 只允许数字
    var phone = val.slice(0, 11);  // 限制11位
    
    // 更新手机号数据
    this.setData({
      Phone: phone
    })
    
    // 根据登录方式检查
    if (this.data.loginType === 'password') {
      // 密码登录：手机号和密码都非空
      if(phone != '' && this.data.Password != ''){
        this.setData({
          jin: false  // 启用登录按钮
        })
      } else {
        this.setData({
          jin: true   // 禁用登录按钮
        })
      }
    } else {
      // 验证码登录：手机号和验证码都非空
      if(phone != '' && this.data.Code != ''){
        this.setData({
          jin: false  // 启用登录按钮
        })
      } else {
        this.setData({
          jin: true   // 禁用登录按钮
        })
      }
    }
  },
 
  /**
   * 密码输入框监听
   * ==============
   * 功能：监听密码输入，实时更新数据并控制登录按钮状态
   * 说明：只有当手机号和密码都不为空时，登录按钮才可用
   */
  passwordInput: function(e){
    var val = e.detail.value;  // 获取输入框的值
    
    // 更新密码数据
    this.setData({
      Password: val
    })
    
    // 只有手机号和密码都非空，才能启用【登录】按钮
    if(val != '' && this.data.Phone != ''){
      this.setData({
        jin: false  // 启用登录按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用登录按钮
      })
    }
  },

  /**
   * 验证码输入框监听
   * ================
   * 功能：监听验证码输入，实时更新数据并控制登录按钮状态
   */
  codeInput: function(e){
    var val = e.detail.value.replace(/\D/g, '');  // 只允许数字
    var code = val.slice(0, 6);  // 限制6位
    
    // 更新验证码数据
    this.setData({
      Code: code
    })
    
    // 只有手机号和验证码都非空，才能启用【登录】按钮
    if(code != '' && this.data.Phone != ''){
      this.setData({
        jin: false  // 启用登录按钮
      })
    } else {
      this.setData({
        jin: true   // 禁用登录按钮
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
 
  /**
   * 登录提交
   * ========
   * 功能：向服务器发送登录请求，验证用户身份
   * 流程：
   *   1. 获取手机号和密码/验证码
   *   2. 发送POST请求到登录接口
   *   3. 处理响应结果
   *   4. 登录成功：保存用户信息，跳转到首页
   *   5. 登录失败：显示错误提示
   */
  post: function(){ 
    var that = this;  // 保存this引用
    
    const { Phone, Password, Code, loginType } = this.data;

    // 输入验证
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

    // 根据登录方式验证
    if (loginType === 'password') {
      if (!Password) {
        wx.showToast({
          title: '请输入密码',
          icon: 'none',
          duration: 2000
        });
        return;
      }
    } else {
      if (!Code) {
        wx.showToast({
          title: '请输入验证码',
          icon: 'none',
          duration: 2000
        });
        return;
      }
      if (Code.length !== 6) {
        wx.showToast({
          title: '验证码为6位数字',
          icon: 'none',
          duration: 2000
        });
        return;
      }
    }

    // 构建请求数据
    const requestData = {
      Phone: Phone
    };

    // 根据登录方式添加不同的参数
    if (loginType === 'password') {
      requestData.Password = Password;
    } else {
      requestData.Code = Code;
    }

    // 发送登录请求
    post(apiConfig.endpoints.login, requestData, {
      showLoading: true,             // 显示加载提示
      loadingText: '登录中...',       // 加载提示文字
      header: {
        'content-type': 'application/x-www-form-urlencoded'  // 使用form格式
      }
    }).then(res => {
      console.log(res);
      
      // ============================================
      // 处理登录失败情况（返回'0'字符串）
      // ============================================
      if (typeof res === 'string' && res === '0') {
        wx.showModal({
          title: '提示',
          content: '手机号或密码不正确！',
          success (res) {
            if (res.confirm) {
              console.log('手机号或密码不正确')
            } else if (res.cancel) {
              console.log('手机号或密码不正确')
            }
          }
        });
        console.log("登录失败");
        return;
      }
      
      // ============================================
      // 处理登录成功情况（返回用户信息对象）
      // ============================================
      if (res && res !== 0) {
        console.log("登录成功")
        
        // 打印后端返回的用户数据（用于调试）
        console.log(res.user_id)
        console.log(res.user_Phone)
        console.log(res.user_name)
        console.log(res.user_Gender)
        console.log(res.user_Birthday)
        console.log(res.user_Password)
        console.log(res.user_FaceImg)
        console.log(res.user_UserType)
        
        // ============================================
        // 保存用户登录数据到页面data
        // ============================================
        that.setData({Phone: res.user_Phone})
        that.setData({Username: res.user_name})
        that.setData({Gender: res.user_Gender})
        that.setData({Birthday: res.user_Birthday})
        that.setData({Password: res.user_Password})
        that.setData({FaceImg: res.user_FaceImg})
        that.setData({UserType: res.user_UserType})

        // ============================================
        // 保存用户信息到全局变量（供其他页面使用）
        // ============================================
        app.globalData.userInfo = {
            nickName: that.data.Username,
            Phone: that.data.Phone,
            Password: that.data.Password,
            Gender: that.data.Gender,
            Birthday: that.data.Birthday,
            FaceImg: that.data.FaceImg,
            UserType: that.data.UserType
        }
        
        // ============================================
        // 保存用户信息到本地文件（持久化存储）
        // ============================================
        // 将用户登录信息格式化为字符串（使用换行符分隔）
        var mydata = "32\n" + res.user_Phone + "\n" + res.user_name + "\n" + 
                     res.user_Password + "\n" + res.user_Gender + "\n" + 
                     '2024-12-05 20:11:19' + "\n" + res.user_Birthday + "\n" + 
                     res.user_FaceImg + "\n" + res.user_UserType;
        console.log(mydata)
        // 将数据写入本地文件
        that.setInfo(mydata);

        // ============================================
        // 显示登录成功提示并跳转到首页
        // ============================================
        wx.showToast({
          title: '登录成功',
          icon: 'success',
          duration: 2000
        });

        // 延迟1.5秒后跳转到首页（等待Toast显示完成）
        setTimeout(() => {
          wx.switchTab({  // 导航到tabBar页面（首页）
            url: '/pages/home/home', 
          });
        }, 1500);
      } else {
        // ============================================
        // 其他失败情况
        // ============================================
        wx.showModal({
          title: '提示',
          content: '手机号或密码不正确！',
          success (res) {
            if (res.confirm) {
              console.log('手机号或密码不正确')
            } else if (res.cancel) {
              console.log('手机号或密码不正确')
            }
          }
        });
        console.log("登录失败");
      }
    }).catch(err => {
      // 请求失败（网络错误等）
      console.error("登录失败：", err);
      // 错误提示已在 request.js 中处理
    });
  },

  /**
   * 保存用户信息到本地文件
   * ======================
   * 功能：将用户登录信息写入微信小程序本地存储空间
   * 说明：使用文件系统API将用户信息持久化保存
   * 
   * @param {String} mydata 要保存的用户信息（格式化的字符串）
   * 
   * 文件路径：wx.env.USER_DATA_PATH/userInfo.txt
   * 注意：如果文件已存在会被覆盖
   */
  setInfo(mydata){
    const fileSystemManager = wx.getFileSystemManager();  // 获取文件系统管理器
    const filePath = `${wx.env.USER_DATA_PATH}/userInfo.txt`;  // 文件路径（用户数据目录）
    const data = mydata;  // 要写入文件的数据

    // 写入文件
    fileSystemManager.writeFile({
        filePath: filePath,    // 文件路径
        data: data,            // 要写入的数据
        encoding: 'utf8',      // 编码方式：使用utf8编码写入文本文件
      
        success: function() {
          // 文件写入成功时的回调函数
          console.log('文件写入成功');
          // 可以在这里进行后续操作，比如通知用户或读取刚写入的数据进行验证
        },
        fail: function(err) {
          // 文件写入失败时的回调函数
          console.error('文件写入失败：', err);
          // 可以在这里处理错误，比如显示错误消息给用户
        }
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