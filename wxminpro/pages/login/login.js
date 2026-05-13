// pages/login/login.js
// ============================================
// 用户登录注册页面
// ============================================
// 功能：用户登录和注册功能，支持手机号+密码登录
// 说明：登录成功后保存用户信息到全局变量和本地存储

const app = getApp()
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

Page({
  data: {
    showRegister: false,        // 是否显示注册表单
    Phone: '',                  // 手机号
    Password: '',               // 密码
    showPassword: false,        // 是否显示密码
    rememberPassword: false,    // 是否记住密码
    
    // 注册相关
    registerPhone: '',          // 注册手机号
    registerUserName: '',        // 注册用户名
    registerGender: '',           // 注册性别
    registerBirthday: '',        // 注册出生日期
    registerPassword: '',        // 注册密码
    registerPasswordConfirm: '', // 确认密码
    showRegisterPassword: false, // 是否显示注册密码
    showRegisterPasswordConfirm: false, // 是否显示确认密码
    FaceImg: '/static/image/header.png', // 头像路径
    Path: '',                    // 头像临时路径
    Filename: '',                // 头像文件名
    jin: true                    // 按钮是否禁用
  },

  onLoad() {
    // 检查是否已登录
    this.checkLoginStatus()
    // 加载记住的密码
    this.loadRememberedPassword()
  },

  // 检查登录状态
  checkLoginStatus() {
    const userInfo = app.globalData.userInfo || wx.getStorageSync('userInfo')
    if (userInfo && userInfo.Phone) {
      // 已登录，跳转到首页
      wx.switchTab({
        url: '/pages/home/home'
      })
    }
  },

  // 加载记住的密码
  loadRememberedPassword() {
    try {
      const remembered = wx.getStorageSync('rememberedLogin')
      if (remembered && remembered.Phone) {
        this.setData({
          Phone: remembered.Phone,
          Password: remembered.Password || '',
          rememberPassword: true
        })
      }
    } catch (e) {
      console.error('加载记住密码失败:', e)
    }
  },

  // 手机号输入
  onPhoneInput(e) {
    const val = e.detail.value
    this.setData({ Phone: val })
    this.updateLoginButtonState()
  },

  // 密码输入
  onPasswordInput(e) {
    const val = e.detail.value
    this.setData({ Password: val })
    this.updateLoginButtonState()
  },

  // 更新登录按钮状态
  updateLoginButtonState() {
    const { Phone, Password } = this.data
    this.setData({
      jin: !(Phone && Password)
    })
  },

  // 切换密码显示
  togglePassword() {
    this.setData({
      showPassword: !this.data.showPassword
    })
  },

  // 记住密码切换
  onRememberPasswordChange(e) {
    this.setData({
      rememberPassword: e.detail.value.length > 0
    })
  },

  // 切换到注册
  switchToRegister() {
    this.setData({
      showRegister: true,
      Phone: '',
      Password: ''
    })
  },

  // 切换到登录
  switchToLogin() {
    this.setData({
      showRegister: false,
      registerPhone: '',
      registerUserName: '',
      registerGender: '',
      registerBirthday: '',
      registerPassword: '',
      registerPasswordConfirm: ''
    })
  },

  // 登录
  async handleLogin() {
    const { Phone, Password } = this.data

    if (!Phone || !Password) {
      wx.showToast({
        title: '请输入手机号和密码',
        icon: 'none'
      })
      return
    }

    // 验证手机号格式
    const phoneReg = /^1[3456789]\d{9}$/
    if (!phoneReg.test(Phone)) {
      wx.showToast({
        title: '手机号格式不正确',
        icon: 'none'
      })
      return
    }

    try {
      const res = await post(apiConfig.endpoints.loginAudio, {
        Phone: Phone,
        Password: Password
      }, {
        showLoading: true,
        loadingText: '登录中...',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }
      })

      // 处理登录失败（返回'0'）
      if (typeof res === 'string' && res === '0') {
        wx.showModal({
          title: '提示',
          content: '手机号或密码不正确！',
          showCancel: false
        })
        return
      }

      // 处理登录成功
      if (res && res !== '0' && res.user_Phone) {
        // 保存用户信息
        const userInfo = {
          Phone: res.user_Phone,
          UserName: res.user_name,
          Password: res.user_Password,
          Gender: res.user_Gender,
          Birthday: res.user_Birthday,
          FaceImg: res.user_FaceImg || '/static/image/header.png',
          UserType: res.user_UserType,
          MaxNoiseTimes: res.user_MaxNoiseTimes || 10,
          CurNoiseTimes: res.user_CurNoiseTimes || 0,
          MaxSepTimes: res.user_MaxSepTimes || 10,
          CurSepTimes: res.user_CurSepTimes || 0
        }

        // 更新全局变量
        app.globalData.userInfo = userInfo
        app.globalData.isLoggedIn = true

        // 保存到本地存储
        wx.setStorageSync('userInfo', userInfo)

        // 处理记住密码
        if (this.data.rememberPassword) {
          wx.setStorageSync('rememberedLogin', {
            Phone: Phone,
            Password: Password
          })
        } else {
          wx.removeStorageSync('rememberedLogin')
        }

        wx.showToast({
          title: '登录成功',
          icon: 'success',
          duration: 2000
        })

        setTimeout(() => {
          wx.switchTab({
            url: '/pages/home/home'
          })
        }, 1500)
      }
    } catch (error) {
      console.error('登录失败:', error)
      wx.showToast({
        title: '登录失败，请重试',
        icon: 'none'
      })
    }
  },

  // ============================================
  // 注册相关方法
  // ============================================
  
  // 注册手机号输入
  onRegisterPhoneInput(e) {
    const val = e.detail.value
    this.setData({ registerPhone: val })
    this.updateRegisterButtonState()
  },

  // 注册用户名输入
  onRegisterUserNameInput(e) {
    const val = e.detail.value
    this.setData({ registerUserName: val })
    this.updateRegisterButtonState()
  },

  // 注册性别输入
  onRegisterGenderInput(e) {
    const val = e.detail.value
    this.setData({ registerGender: val })
    this.updateRegisterButtonState()
  },

  // 注册出生日期输入
  onRegisterBirthdayInput(e) {
    const val = e.detail.value
    this.setData({ registerBirthday: val })
    this.updateRegisterButtonState()
  },

  // 注册密码输入
  onRegisterPasswordInput(e) {
    const val = e.detail.value
    this.setData({ registerPassword: val })
    this.updateRegisterButtonState()
  },

  // 确认密码输入
  onRegisterPasswordConfirmInput(e) {
    const val = e.detail.value
    this.setData({ registerPasswordConfirm: val })
    this.updateRegisterButtonState()
  },

  // 更新注册按钮状态
  updateRegisterButtonState() {
    const { registerPhone, registerUserName, registerGender, registerBirthday, registerPassword } = this.data
    this.setData({
      jin: !(registerPhone && registerUserName && registerGender && registerBirthday && registerPassword)
    })
  },

  // 切换注册密码显示
  toggleRegisterPassword() {
    this.setData({
      showRegisterPassword: !this.data.showRegisterPassword
    })
  },

  // 切换确认密码显示
  toggleRegisterPasswordConfirm() {
    this.setData({
      showRegisterPasswordConfirm: !this.data.showRegisterPasswordConfirm
    })
  },

  // 选择头像
  selectFaceImg() {
    const that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        const tempFilePaths = res.tempFiles
        if (tempFilePaths && tempFilePaths.length > 0) {
          const path = tempFilePaths[0].path
          const filename = path.slice(11) // 从 http://tmp/ 后提取文件名
          that.setData({
            Path: path,
            Filename: filename
          })
        }
      }
    })
  },

  // 注册
  async handleRegister() {
    const { registerPhone, registerUserName, registerGender, registerBirthday, registerPassword, registerPasswordConfirm } = this.data

    // 验证必填字段
    if (!registerPhone || !registerUserName || !registerGender || !registerBirthday || !registerPassword) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }

    // 验证手机号格式
    const phoneReg = /^1[3456789]\d{9}$/
    if (!phoneReg.test(registerPhone)) {
      wx.showToast({
        title: '手机号格式不正确',
        icon: 'none'
      })
      return
    }

    // 验证密码
    if (registerPassword.length < 6) {
      wx.showToast({
        title: '密码至少6位',
        icon: 'none'
      })
      return
    }

    if (registerPassword !== registerPasswordConfirm) {
      wx.showToast({
        title: '两次密码不一致',
        icon: 'none'
      })
      return
    }

    try {
      // 上传头像（如果有）
      let faceImg = '/static/image/header.png'
      if (this.data.Path) {
        try {
          const { uploadFile } = require('../../utils/request.js')
          const uploadRes = await uploadFile(
            this.data.Path,
            apiConfig.endpoints.receiveFaceImg,
            { method: 'POST' },
            { name: 'file' }
          )
          faceImg = uploadRes.user_FaceImg || faceImg
        } catch (e) {
          console.error('头像上传失败，使用默认头像:', e)
        }
      }

      // 发送注册请求
      const res = await post(apiConfig.endpoints.registerAudio, {
        Phone: registerPhone,
        UserName: registerUserName,
        Gender: registerGender,
        Birthday: registerBirthday,
        Password: registerPassword,
        FaceImg: faceImg
      }, {
        showLoading: true,
        loadingText: '注册中...',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }
      })

      // 处理注册结果
      if (res === '0') {
        wx.showToast({
          title: '注册成功',
          icon: 'success',
          duration: 2000
        })
        setTimeout(() => {
          this.switchToLogin()
          this.setData({
            Phone: registerPhone
          })
        }, 1500)
      } else if (res === '1') {
        wx.showToast({
          title: '该手机号已注册',
          icon: 'none'
        })
      } else if (res === '2') {
        wx.showToast({
          title: '注册失败，请重试',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('注册失败:', error)
      wx.showToast({
        title: '注册失败，请重试',
        icon: 'none'
      })
    }
  }
})

