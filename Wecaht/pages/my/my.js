// pages/my/my.js
const app = getApp();
const { getAllUsersData, exportUsersData } = require('../../utils/dbManager.js');
const { checkLoginStatus, showError, showSuccess } = require('../../utils/common.js');

Page({
  data: {
    username: '',
    userLevelName: '普通用户',
    maxDigits: 50,
    canCloudCompute: false,
    userAvatar: '',
    isAdmin: false
  },

  onLoad() {
    this.checkLogin();
    this.loadUserInfo();
  },

  onShow() {
    this.checkLogin();
    this.loadUserInfo();
    // 从后端获取最新用户信息（确保等级改变后能及时更新）
    this.refreshUserInfo();
  },

  // 检查登录状态
  checkLogin() {
    return checkLoginStatus();
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = app.getUserInfo();
    if (userInfo) {
      const levelConfig = this.getLevelConfig(userInfo.level);
      const isAdmin = userInfo.level === 'admin';
      
      console.log('加载用户信息:', {
        username: userInfo.username,
        level: userInfo.level,
        isAdmin: isAdmin
      });
      
      this.setData({
        username: userInfo.username || '用户',
        userLevelName: userInfo.level_name || userInfo.levelName || levelConfig.name,
        maxDigits: userInfo.max_digits || userInfo.maxDigits || levelConfig.maxDigits,
        canCloudCompute: levelConfig.canCloudCompute,
        userAvatar: userInfo.avatar || '',
        isAdmin: isAdmin
      });
    } else {
      // 如果没有用户信息，重置isAdmin
      this.setData({
        isAdmin: false
      });
    }
  },

  // 从后端刷新用户信息
  async refreshUserInfo() {
    try {
      const { requestApi } = require('../../utils/common.js');
      const res = await requestApi({
        url: '/api/auth/user',
        method: 'GET',
        showLoading: false
      });
      
      // 确保 res 存在且格式正确
      if (res && res.success && res.data) {
        const userInfo = res.data;
        // 使用统一方法更新用户信息（确保全局变量和本地存储同步）
        app.updateUserInfo(userInfo);
        
        // 重新加载用户信息到页面
        this.loadUserInfo();
      } else if (res && !res.success) {
        // API返回了错误响应
        console.warn('刷新用户信息失败:', res.message || '未知错误');
      }
    } catch (e) {
      console.error('刷新用户信息失败:', e);
    }
  },

  // 获取等级配置
  getLevelConfig(level) {
    const configs = {
      normal: { name: '普通用户', maxDigits: 50, canCloudCompute: false },
      vip: { name: 'VIP用户', maxDigits: 80, canCloudCompute: false },
      svip: { name: 'SVIP用户', maxDigits: 120, canCloudCompute: false },
      admin: { name: '管理员', maxDigits: 200, canCloudCompute: true }
    };
    return configs[level] || configs.normal;
  },

  // 用户管理（仅管理员）
  manageUsers() {
    const currentUser = app.getUserInfo();
    if (!currentUser || currentUser.level !== 'admin') {
      showError('只有管理员可以访问此功能');
      return;
    }

    // 跳转到用户管理页面
    wx.navigateTo({
      url: '/pages/admin/admin'
    });
  },

  // 更换头像
  changeAvatar() {
    const that = this;
    
    // 检查存储空间
    try {
      const info = wx.getStorageInfoSync();
      if (info.currentSize / info.limitSize > 0.9) {
        wx.showModal({
          title: '存储空间不足',
          content: '存储空间已使用超过90%，建议先清理历史记录',
          showCancel: true,
          success: (res) => {
            if (res.confirm) {
              // 继续上传
              that.doChooseImage();
            }
          }
        });
        return;
      }
    } catch (e) {
      console.error('检查存储空间失败:', e);
    }
    
    this.doChooseImage();
  },

  // 选择图片
  doChooseImage() {
    const that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: function(res) {
        const tempFilePath = res.tempFilePaths[0];
        
        // 检查文件大小（限制2MB）
        wx.getFileInfo({
          filePath: tempFilePath,
          success: (fileInfo) => {
            if (fileInfo.size > 2 * 1024 * 1024) {
              showError('图片大小不能超过2MB');
              return;
            }
            
            // 显示加载提示
            wx.showLoading({
              title: '保存中...',
              mask: true
            });

            // 将临时文件保存为永久文件
            wx.saveFile({
              tempFilePath: tempFilePath,
              success: function(saveRes) {
                const savedFilePath = saveRes.savedFilePath;
                
                // 更新用户头像
                const currentUser = app.getUserInfo();
                if (currentUser) {
                  const userInfo = {
                    ...currentUser,
                    avatar: savedFilePath
                  };
                  app.updateUserInfo(userInfo);
                  that.setData({
                    userAvatar: savedFilePath
                  });
                  wx.hideLoading();
                  showSuccess('头像更新成功');
                } else {
                  wx.hideLoading();
                }
              },
              fail: function(err) {
                wx.hideLoading();
                let errorMsg = '保存失败';
                if (err.errMsg && err.errMsg.includes('exceed')) {
                  errorMsg = '存储空间不足，请清理后重试';
                }
                showError(errorMsg);
              }
            });
          },
          fail: (err) => {
            showError('获取文件信息失败');
            console.error('getFileInfo失败:', err);
          }
        });
      },
      fail: function(err) {
        if (err.errMsg && !err.errMsg.includes('cancel')) {
          showError('选择图片失败');
        }
        // 用户取消选择不提示
      }
    });
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          app.logout();
        }
      }
    });
  },

  // 查看关于
  viewAbout() {
    wx.showModal({
      title: '关于系统',
      content: '基于微信小程序的大整数分解系统\n\n版本：1.0.0\n\n采用Pollard\'s Rho算法和Miller-Rabin素性测试，支持大整数分解计算。',
      showCancel: false,
      confirmText: '知道了'
    });
  },

  // 查看帮助
  viewHelp() {
    wx.showModal({
      title: '使用帮助',
      content: '1. 在"分解"页面输入要分解的大整数\n2. 点击"开始分解"按钮开始计算\n3. 查看实时进度和分解结果\n4. 结果会自动保存到历史记录\n5. 可以在"历史"页面查看所有记录\n6. 支持0和1的特殊分解\n7. 显示数字类型和分解程度',
      showCancel: false,
      confirmText: '知道了'
    });
  },

  // 导出用户数据
  exportUserData() {
    const data = getAllUsersData();
    const jsonStr = JSON.stringify(data, null, 2);
    
    // 复制到剪贴板
    wx.setClipboardData({
      data: jsonStr,
      success: () => {
        wx.showModal({
          title: '数据已复制',
          content: `用户数据已复制到剪贴板，共${data.users.length}个用户。\n\n可在db/users.json文件中查看完整数据。`,
          showCancel: false,
          confirmText: '知道了'
        });
      },
      fail: () => {
        wx.showModal({
          title: '数据导出',
          content: `用户数据（JSON格式）：\n\n${jsonStr.substring(0, 500)}${jsonStr.length > 500 ? '...' : ''}`,
          showCancel: false,
          confirmText: '知道了'
        });
      }
    });
  }
});

