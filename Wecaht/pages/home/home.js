// pages/home/home.js
const app = getApp();
const { checkLoginStatus } = require('../../utils/common.js');

Page({
  data: {
    userLevelName: '普通用户',
    maxDigits: 50
  },

  onLoad() {
    this.checkLogin();
    this.loadUserInfo();
  },

  onShow() {
    this.checkLogin();
    this.loadUserInfo();
  },

  // 检查登录状态
  checkLogin() {
    return checkLoginStatus();
  },

  // 加载用户信息（从后端获取最新信息）
  async loadUserInfo() {
    try {
      // 先从本地获取（快速显示）
      const localUserInfo = app.getUserInfo();
      if (localUserInfo) {
        this.setData({
          userLevelName: localUserInfo.level_name || localUserInfo.levelName || '普通用户',
          maxDigits: localUserInfo.max_digits || localUserInfo.maxDigits || 50
        });
      }
      
      // 从后端获取最新用户信息（确保等级改变后能及时更新）
      const { requestApi } = require('../../utils/common.js');
      let res = null; // 初始化为 null，确保不会是 undefined
      try {
        const apiResult = await requestApi({
          url: '/api/auth/user',
          method: 'GET',
          showLoading: false
        });
        // 确保 apiResult 不是 undefined
        res = apiResult || {
          success: false,
          message: '请求返回为空',
          data: null
        };
      } catch (apiError) {
        console.error('requestApi 调用异常:', apiError);
        res = {
          success: false,
          message: apiError?.message || '请求异常',
          data: null
        };
      }
      
      // 双重检查：确保 res 存在且格式正确
      if (!res) {
        console.error('res 为 null 或 undefined');
        res = {
          success: false,
          message: '响应数据为空',
          data: null
        };
      }
      
      // 确保 res 存在且格式正确
      if (typeof res === 'object' && res !== null && res.success && res.data) {
        const userInfo = res.data;
        // 使用统一方法更新用户信息（确保全局变量和本地存储同步）
        app.updateUserInfo(userInfo);
        
        // 更新页面数据
        this.setData({
          userLevelName: userInfo.level_name || '普通用户',
          maxDigits: userInfo.max_digits || 50
        });
      } else {
        // API返回了错误响应或格式不正确
        if (res && typeof res === 'object') {
          console.warn('获取用户信息失败:', res.message || '未知错误', res);
        } else {
          console.error('获取用户信息失败: res 格式不正确', res);
        }
      }
    } catch (e) {
      console.error('获取用户信息失败:', e);
      // 如果后端获取失败，使用本地数据
      const localUserInfo = app.getUserInfo();
      if (localUserInfo) {
        this.setData({
          userLevelName: localUserInfo.level_name || localUserInfo.levelName || '普通用户',
          maxDigits: localUserInfo.max_digits || localUserInfo.maxDigits || 50
        });
      }
    }
  },

  // 跳转到分解页面
  goToSplitter() {
    wx.switchTab({
      url: '/pages/splitter/splitter'
    });
  }
});

