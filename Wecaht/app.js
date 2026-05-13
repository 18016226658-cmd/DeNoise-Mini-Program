// app.js
const { syncUserToDB } = require('./utils/dbManager.js');
const { safeSetStorage, safeGetStorage } = require('./utils/common.js');

App({
  onLaunch() {
    // 初始化管理员账户
    this.initAdminAccount();
    // 全局错误处理
    this.setupErrorHandler();
    // 检查登录状态
    this.checkLogin();
    // 初始化历史记录
    this.initHistory();
    // 检查用户生日
    this.checkUserBirthday();
  },

  // 初始化管理员账户
  initAdminAccount() {
    try {
      const users = safeGetStorage('users', {});
      const adminUsername = 'xqq';
      
      // 如果管理员账户不存在，则创建；如果存在，更新密码为123456
      if (!users[adminUsername]) {
        const adminUser = {
          username: adminUsername,
          password: '123456',  // 修改为123456以便登录
          level: 'admin',
          levelName: '管理员',
          maxDigits: 200,
          avatar: '',
          createTime: new Date().getTime(),
          lastLoginTime: null,
          loginCount: 0,
          description: '系统管理员账户'
        };
        
        users[adminUsername] = adminUser;
        safeSetStorage('users', users);
        
        // 同步到db
        syncUserToDB(adminUser);
        
        console.log('管理员账户已创建:', adminUsername);
      } else {
        // 如果账户已存在，更新密码为123456（确保密码正确）
        if (users[adminUsername].password !== '123456') {
          users[adminUsername].password = '123456';
          users[adminUsername].level = 'admin';
          users[adminUsername].levelName = '管理员';
          users[adminUsername].maxDigits = 200;
          safeSetStorage('users', users);
          syncUserToDB(users[adminUsername]);
          console.log('管理员账户密码已更新为123456');
        }
      }
    } catch (e) {
      console.error('初始化管理员账户失败:', e);
    }
  },

  // 设置全局错误处理
  setupErrorHandler() {
    // 捕获未处理的Promise错误
    wx.onError && wx.onError((error) => {
      console.error('全局错误:', error);
      // 可以在这里上报错误到服务器
    });

    // 捕获未处理的Promise rejection
    if (typeof Promise !== 'undefined' && Promise.reject) {
      const originalReject = Promise.reject;
      Promise.reject = function(reason) {
        console.error('未处理的Promise rejection:', reason);
        return originalReject.call(this, reason);
      };
    }
  },

  // 检查登录状态（不自动跳转，由页面自行处理）
  checkLogin() {
    const currentUser = wx.getStorageSync('currentUser');
    if (currentUser) {
      this.globalData.userInfo = currentUser;
      this.globalData.isLoggedIn = true;
    } else {
      this.globalData.isLoggedIn = false;
    }
    return this.globalData.isLoggedIn;
  },


  // 初始化历史记录
  initHistory() {
    const history = safeGetStorage('factorHistory', []);
    if (!Array.isArray(history)) {
      safeSetStorage('factorHistory', []);
      this.globalData.history = [];
    } else {
      this.globalData.history = history;
    }
  },

  // 获取用户信息
  getUserInfo() {
    return this.globalData.userInfo || safeGetStorage('currentUser', null);
  },

  // 更新用户信息（统一方法，确保全局变量和本地存储同步）
  updateUserInfo(userInfo) {
    try {
      // 统一字段名，确保兼容性（后端返回max_digits，前端可能使用maxDigits）
      const normalizedUserInfo = {
        ...userInfo,
        // 确保同时有max_digits和maxDigits
        max_digits: userInfo.max_digits || userInfo.maxDigits || 50,
        maxDigits: userInfo.max_digits || userInfo.maxDigits || 50,
        // 确保同时有level_name和levelName
        level_name: userInfo.level_name || userInfo.levelName || '普通用户',
        levelName: userInfo.level_name || userInfo.levelName || '普通用户'
      };
      
      // 更新全局变量（所有页面都能访问）
      this.globalData.userInfo = normalizedUserInfo;
      this.globalData.isLoggedIn = true;
      
      // 更新本地存储
      safeSetStorage('currentUser', normalizedUserInfo);
      
      // 同时更新users中的信息（兼容旧代码）
      const users = safeGetStorage('users', {});
      if (users[normalizedUserInfo.username]) {
        users[normalizedUserInfo.username] = normalizedUserInfo;
        safeSetStorage('users', users);
      }
      
      // 同步到db（如果需要）
      if (typeof syncUserToDB === 'function') {
        syncUserToDB(normalizedUserInfo);
      }
      
      console.log('用户信息已更新到全局变量:', {
        username: normalizedUserInfo.username,
        level: normalizedUserInfo.level || normalizedUserInfo.level_name,
        maxDigits: normalizedUserInfo.max_digits || normalizedUserInfo.maxDigits
      });
    } catch (e) {
      console.error('更新用户信息失败:', e);
    }
  },


  // 退出登录
  logout() {
    try {
      wx.removeStorageSync('currentUser');
      this.globalData.userInfo = null;
      this.globalData.isLoggedIn = false;
      wx.reLaunch({
        url: '/pages/login/login'
      });
    } catch (e) {
      console.error('退出登录失败:', e);
      wx.reLaunch({
        url: '/pages/login/login'
      });
    }
  },

  // 添加历史记录
  addHistory(record) {
    try {
      const history = this.globalData.history || [];
      history.unshift({
        ...record,
        id: Date.now(),
        time: new Date().toLocaleString()
      });
      // 最多保存100条记录，如果存储失败则减少到50条
      if (history.length > 100) {
        history.pop();
      }
      this.globalData.history = history;
      
      // 尝试保存，如果失败则清理旧记录
      if (!safeSetStorage('factorHistory', history)) {
        // 如果保存失败，只保留最近50条
        const reducedHistory = history.slice(0, 50);
        this.globalData.history = reducedHistory;
        safeSetStorage('factorHistory', reducedHistory);
      }
    } catch (e) {
      console.error('保存历史记录失败:', e);
      // 如果还是失败，清理部分历史
      try {
        const history = this.globalData.history || [];
        if (history.length > 20) {
          this.globalData.history = history.slice(0, 20);
          safeSetStorage('factorHistory', this.globalData.history);
        }
      } catch (cleanupError) {
        console.error('清理历史记录也失败:', cleanupError);
      }
    }
  },

  // 清除历史记录
  clearHistory() {
    try {
      this.globalData.history = [];
      safeSetStorage('factorHistory', []);
    } catch (e) {
      console.error('清除历史记录失败:', e);
    }
  },

  // 检查用户生日
  checkUserBirthday() {
    try {
      const currentUser = this.globalData.userInfo || safeGetStorage('currentUser', null);
      if (!currentUser) {
        return;
      }

      // 检查是否有出生日期信息
      if (!currentUser.birthYear || !currentUser.birthMonth) {
        return;
      }

      const today = new Date();
      const currentYear = today.getFullYear();
      const currentMonth = today.getMonth() + 1; // 月份从0开始，需要+1
      const currentDay = today.getDate();

      // 检查是否是用户生日（如果有日期信息，检查完整日期；否则只检查月份）
      const isBirthday = currentUser.birthMonth === currentMonth && 
                         (!currentUser.birthDay || currentUser.birthDay === currentDay);
      
      if (isBirthday) {
        // 检查今天是否已经显示过生日祝福（避免重复显示）
        const lastBirthdayCheck = safeGetStorage('lastBirthdayCheck', '');
        const todayStr = `${currentYear}-${currentMonth}-${currentDay}`;
        
        // 如果今天已经显示过，不再显示
        if (lastBirthdayCheck === todayStr) {
          return;
        }
        
        // 计算年龄
        let age = currentYear - currentUser.birthYear;
        // 如果还没到生日，年龄减1
        if (currentMonth < currentUser.birthMonth || 
            (currentMonth === currentUser.birthMonth && currentUser.birthDay && currentDay < currentUser.birthDay)) {
          age--;
        }
        
        // 显示生日祝福
        const birthdayText = currentUser.birthDay ? '今天是你的生日！' : '这个月是你的生日月！';
        wx.showModal({
          title: '🎉 生日快乐！',
          content: `亲爱的 ${currentUser.username}，\n\n${birthdayText}\n\n祝你${age}岁生日快乐！\n\n愿你在新的一岁里，\n身体健康，工作顺利，\n心想事成，万事如意！`,
          showCancel: false,
          confirmText: '谢谢',
          confirmColor: '#FF69B4'
        });

        // 记录今天已显示过生日祝福
        safeSetStorage('lastBirthdayCheck', todayStr);
      }
    } catch (e) {
      console.error('检查用户生日失败:', e);
    }
  },

  globalData: {
    userInfo: null,
    history: [],
    isLoggedIn: false
  }
});

