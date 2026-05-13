// utils/dbManager.js
// 用户数据管理工具

/**
 * 同步用户数据到db存储
 */
function syncUserToDB(userInfo) {
  try {
    // 获取所有用户数据
    const allUsers = wx.getStorageSync('allUsersDB') || [];
    
    // 查找并更新用户
    const userIndex = allUsers.findIndex(u => u.username === userInfo.username);
    if (userIndex >= 0) {
      allUsers[userIndex] = {
        ...allUsers[userIndex],
        ...userInfo,
        updateTime: new Date().toLocaleString()
      };
    } else {
      allUsers.push({
        ...userInfo,
        createTime: userInfo.createTime || new Date().getTime(),
        updateTime: new Date().toLocaleString()
      });
    }

    // 保存到本地存储
    wx.setStorageSync('allUsersDB', allUsers);
    
    // 同时保存到可导出的JSON格式
    const dbData = {
      users: allUsers,
      updateTime: new Date().toLocaleString(),
      version: "1.0.0"
    };
    wx.setStorageSync('dbExport', JSON.stringify(dbData, null, 2));
    
    return true;
  } catch (e) {
    console.error('同步用户数据失败:', e);
    return false;
  }
}

/**
 * 初始化预设用户到db
 */
function initPresetUsersToDB() {
  const presetUsers = [
    {
      username: 'normal',
      password: '123456',
      level: 'normal',
      levelName: '普通用户',
      maxDigits: 50,
      avatar: '',
      createTime: new Date().getTime(),
      lastLoginTime: null,
      loginCount: 0,
      description: '普通用户账户，最大支持50位整数分解'
    },
    {
      username: 'vip',
      password: '123456',
      level: 'vip',
      levelName: 'VIP用户',
      maxDigits: 80,
      avatar: '',
      createTime: new Date().getTime(),
      lastLoginTime: null,
      loginCount: 0,
      description: 'VIP用户账户，最大支持80位整数分解'
    },
    {
      username: 'svip',
      password: '123456',
      level: 'svip',
      levelName: 'SVIP用户',
      maxDigits: 120,
      avatar: '',
      createTime: new Date().getTime(),
      lastLoginTime: null,
      loginCount: 0,
      description: 'SVIP用户账户，最大支持120位整数分解'
    },
    {
      username: 'admin',
      password: '123456',
      level: 'admin',
      levelName: '管理员',
      maxDigits: 200,
      avatar: '',
      createTime: new Date().getTime(),
      lastLoginTime: null,
      loginCount: 0,
      description: '管理员账户，最大支持200位整数分解，支持云端协同计算'
    }
  ];

  const allUsers = wx.getStorageSync('allUsersDB') || [];
  presetUsers.forEach(preset => {
    const exists = allUsers.find(u => u.username === preset.username);
    if (!exists) {
      allUsers.push(preset);
    }
  });

  wx.setStorageSync('allUsersDB', allUsers);
  
  const dbData = {
    users: allUsers,
    updateTime: new Date().toLocaleString(),
    version: "1.0.0"
  };
  wx.setStorageSync('dbExport', JSON.stringify(dbData, null, 2));
}

/**
 * 获取所有用户数据（用于导出）
 */
function getAllUsersData() {
  const allUsers = wx.getStorageSync('allUsersDB') || [];
  return {
    users: allUsers,
    updateTime: new Date().toLocaleString(),
    version: "1.0.0"
  };
}

/**
 * 导出用户数据为JSON字符串
 */
function exportUsersData() {
  const data = getAllUsersData();
  return JSON.stringify(data, null, 2);
}

module.exports = {
  syncUserToDB,
  initPresetUsersToDB,
  getAllUsersData,
  exportUsersData
};

