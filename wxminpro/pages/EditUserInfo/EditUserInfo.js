// pages/EditUserInfo/EditUserInfo.js
// ============================================
// 用户信息编辑页面
// ============================================
// 功能：编辑用户信息（管理员可编辑所有用户，普通用户只能编辑自己）

const app = getApp()
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    // 当前登录用户信息（用于权限验证）
    currentUser: {},
    currentUserType: 2,
    
    // 要编辑的目标用户信息
    targetUser: {
      Phone: '',
      UserName: '',
      Gender: '男',
      Birthday: '',
      UserType: 2,
      MaxSepTimes: 10,
      MaxNoiseTimes: 10
    },
    
    // 编辑表单数据
    formData: {
      UserName: '',
      Gender: '男',
      Birthday: '',
      UserType: 2,
      MaxSepTimes: 10,
      MaxNoiseTimes: 10
    },
    
    // 性别选项
    genderOptions: ['男', '女'],
    
    // 用户类型选项
    userTypeOptions: [
      { value: 1, label: '管理员' },
      { value: 2, label: '普通用户' },
      { value: 3, label: '游客' }
    ],
    
    // 当前选择的用户类型索引
    selectedUserTypeIndex: 0,
    
    // 是否可编辑用户类型和配额（仅管理员）
    canEditUserType: false,
    canEditQuota: false,
    
    // 最大日期（今天）
    maxDate: '',
    
    loading: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 计算今天的日期字符串（用于生日选择器的end属性）
    const today = new Date()
    const year = today.getFullYear()
    const month = String(today.getMonth() + 1).padStart(2, '0')
    const day = String(today.getDate()).padStart(2, '0')
    const maxDate = `${year}-${month}-${day}`
    
    // 获取当前登录用户信息
    const currentUser = app.globalData.userInfo
    if (!currentUser) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 2000)
      return
    }
    
    const currentUserType = currentUser.UserType || currentUser.user_UserType || 2
    const currentUserPhone = currentUser.Phone || currentUser.user_Phone
    
    // 获取要编辑的目标用户手机号（从页面参数或使用当前用户）
    const targetPhone = options.phone || currentUserPhone
    
    this.setData({
      currentUser: currentUser,
      currentUserType: currentUserType,
      canEditUserType: currentUserType === 1,
      canEditQuota: currentUserType === 1,
      maxDate: maxDate
    })
    
    // 加载目标用户信息
    this.loadTargetUserInfo(targetPhone)
  },

  /**
   * 加载目标用户信息
   */
  loadTargetUserInfo(phone) {
    const that = this
    
    // 如果是编辑自己，直接使用当前用户信息
    const currentUser = that.data.currentUser
    const currentUserPhone = currentUser.Phone || currentUser.user_Phone
    
    if (phone === currentUserPhone) {
      // 编辑自己
      const targetUser = {
        Phone: currentUserPhone,
        UserName: currentUser.UserName || currentUser.user_name || '',
        Gender: currentUser.Gender || currentUser.user_Gender || '男',
        Birthday: currentUser.Birthday || currentUser.user_Birthday || '',
        UserType: currentUser.UserType || currentUser.user_UserType || 2,
        MaxSepTimes: currentUser.MaxSepTimes || currentUser.user_MaxSepTimes || 10,
        MaxNoiseTimes: currentUser.MaxNoiseTimes || currentUser.user_MaxNoiseTimes || 10
      }
      
      // 计算用户类型索引
      const userTypeIndex = that.data.userTypeOptions.findIndex(opt => opt.value === targetUser.UserType)
      
      that.setData({
        targetUser: targetUser,
        formData: {
          UserName: targetUser.UserName,
          Gender: targetUser.Gender,
          Birthday: targetUser.Birthday,
          UserType: targetUser.UserType,
          MaxSepTimes: targetUser.MaxSepTimes,
          MaxNoiseTimes: targetUser.MaxNoiseTimes
        },
        selectedUserTypeIndex: userTypeIndex >= 0 ? userTypeIndex : 1
      })
    } else {
      // 编辑其他用户（需要从用户列表获取）
      // 先获取所有用户列表
      post(apiConfig.endpoints.editUser, {}, {
        showLoading: true,
        loadingText: '加载中...',
        header: {
          'content-type': 'application/json'
        }
      }).then(res => {
        const userList = Array.isArray(res) ? res : []
        const targetUser = userList.find(u => u.Phone === phone)
        
        if (targetUser) {
          // 计算用户类型索引
          const userTypeIndex = that.data.userTypeOptions.findIndex(opt => opt.value === (targetUser.UserType || 2))
          
          that.setData({
            targetUser: {
              Phone: targetUser.Phone,
              UserName: targetUser.UserName || '',
              Gender: targetUser.Gender || '男',
              Birthday: targetUser.Birthday || '',
              UserType: targetUser.UserType || 2,
              MaxSepTimes: targetUser.MaxSepTimes || 10,
              MaxNoiseTimes: targetUser.MaxNoiseTimes || 10
            },
            formData: {
              UserName: targetUser.UserName || '',
              Gender: targetUser.Gender || '男',
              Birthday: targetUser.Birthday || '',
              UserType: targetUser.UserType || 2,
              MaxSepTimes: targetUser.MaxSepTimes || 10,
              MaxNoiseTimes: targetUser.MaxNoiseTimes || 10
            },
            selectedUserTypeIndex: userTypeIndex >= 0 ? userTypeIndex : 1
          })
        } else {
          wx.showToast({
            title: '用户不存在',
            icon: 'none'
          })
          setTimeout(() => {
            wx.navigateBack()
          }, 2000)
        }
      }).catch(err => {
        console.error("加载用户信息失败：", err)
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        })
      })
    }
  },

  /**
   * 输入用户名
   */
  onUserNameInput(e) {
    this.setData({
      'formData.UserName': e.detail.value
    })
  },

  /**
   * 选择性别
   */
  onGenderChange(e) {
    this.setData({
      'formData.Gender': this.data.genderOptions[e.detail.value]
    })
  },

  /**
   * 选择生日
   */
  onBirthdayChange(e) {
    this.setData({
      'formData.Birthday': e.detail.value
    })
  },

  /**
   * 选择用户类型（仅管理员）
   */
  onUserTypeChange(e) {
    if (!this.data.canEditUserType) {
      return
    }
    const selectedIndex = e.detail.value
    const selectedType = this.data.userTypeOptions[selectedIndex]
    this.setData({
      'formData.UserType': selectedType.value,
      selectedUserTypeIndex: selectedIndex
    })
  },

  /**
   * 输入分离次数配额（仅管理员）
   */
  onMaxSepTimesInput(e) {
    if (!this.data.canEditQuota) {
      return
    }
    this.setData({
      'formData.MaxSepTimes': parseInt(e.detail.value) || 0
    })
  },

  /**
   * 输入降噪次数配额（仅管理员）
   */
  onMaxNoiseTimesInput(e) {
    if (!this.data.canEditQuota) {
      return
    }
    this.setData({
      'formData.MaxNoiseTimes': parseInt(e.detail.value) || 0
    })
  },

  /**
   * 提交表单
   */
  onSubmit() {
    const that = this
    
    // 验证必填字段
    if (!that.data.formData.UserName || that.data.formData.UserName.trim() === '') {
      wx.showToast({
        title: '请输入用户名',
        icon: 'none'
      })
      return
    }
    
    // 显示加载提示
    wx.showLoading({
      title: '保存中...',
      mask: true
    })
    
    // 准备请求数据
    const currentUser = that.data.currentUser
    const requestData = {
      currentUserPhone: currentUser.Phone || currentUser.user_Phone,
      currentUserType: that.data.currentUserType,
      targetPhone: that.data.targetUser.Phone,
      UserName: that.data.formData.UserName.trim()
    }
    
    // 添加可选字段
    if (that.data.formData.Gender) {
      requestData.Gender = that.data.formData.Gender
    }
    
    if (that.data.formData.Birthday) {
      requestData.Birthday = that.data.formData.Birthday
    }
    
    // 仅管理员可以修改用户类型和配额
    if (that.data.canEditUserType) {
      requestData.UserType = that.data.formData.UserType
      requestData.MaxSepTimes = that.data.formData.MaxSepTimes
      requestData.MaxNoiseTimes = that.data.formData.MaxNoiseTimes
    }
    
    // 发送更新请求
    post(apiConfig.endpoints.updateUserInfo, requestData, {
      showLoading: false,
      header: {
        'content-type': 'application/json'
      }
    }).then(res => {
      wx.hideLoading()
      
      if (res.success) {
        wx.showToast({
          title: '保存成功',
          icon: 'success'
        })
        
        // 更新全局用户信息（如果是编辑自己）
        if (that.data.targetUser.Phone === (currentUser.Phone || currentUser.user_Phone)) {
          // 更新全局用户信息
          const updatedUserInfo = {
            ...currentUser,
            UserName: requestData.UserName,
            user_name: requestData.UserName,
            Gender: requestData.Gender || currentUser.Gender || currentUser.user_Gender,
            user_Gender: requestData.Gender || currentUser.Gender || currentUser.user_Gender,
            Birthday: requestData.Birthday || currentUser.Birthday || currentUser.user_Birthday,
            user_Birthday: requestData.Birthday || currentUser.Birthday || currentUser.user_Birthday
          }
          
          if (that.data.canEditUserType) {
            updatedUserInfo.UserType = requestData.UserType
            updatedUserInfo.user_UserType = requestData.UserType
            updatedUserInfo.MaxSepTimes = requestData.MaxSepTimes
            updatedUserInfo.user_MaxSepTimes = requestData.MaxSepTimes
            updatedUserInfo.MaxNoiseTimes = requestData.MaxNoiseTimes
            updatedUserInfo.user_MaxNoiseTimes = requestData.MaxNoiseTimes
          }
          
          app.globalData.userInfo = updatedUserInfo
        }
        
        // 延迟返回上一页
        setTimeout(() => {
          wx.navigateBack()
        }, 1500)
      } else {
        wx.showToast({
          title: res.message || '保存失败',
          icon: 'none',
          duration: 2000
        })
      }
    }).catch(err => {
      wx.hideLoading()
      console.error("更新用户信息失败：", err)
      wx.showToast({
        title: '保存失败，请重试',
        icon: 'none',
        duration: 2000
      })
    })
  }
})

