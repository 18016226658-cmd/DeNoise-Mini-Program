// utils/common.js
// 公共工具函数

// 后端基础地址（开发阶段本机调试用：http://127.0.0.1:5000）
// 真机/局域网联调时，请改成你电脑在局域网中的 IP，例如：http://10.60.32.34:5000
const BASE_URL = 'http://127.0.0.1:5000';

/**
 * 获取当前登录用户对应的后端 token（这里直接用用户名）
 */
function getAuthToken() {
  try {
    const currentUser = wx.getStorageSync('currentUser');
    return currentUser && currentUser.username ? currentUser.username : '';
  } catch (e) {
    return '';
  }
}

/**
 * 统一封装后端请求（返回Promise，支持async/await）
 * @param {Object} options - { url, method, data, showLoading }
 * @returns {Promise} 返回Promise，resolve时返回 { success, data, message } 格式
 */
function requestApi(options = {}) {
  const {
    url,
    method = 'GET',
    data = {},
    showLoading = true
  } = options;

  // 确保总是返回 Promise，并且 resolve 的值永远不是 undefined
  if (!url) {
    console.error('requestApi: url 不能为空');
    return Promise.resolve({
      success: false,
      message: 'url 不能为空',
      data: null
    });
  }

  // 确保 BASE_URL 存在
  if (!BASE_URL) {
    console.error('requestApi: BASE_URL 未配置');
    return Promise.resolve({
      success: false,
      message: 'BASE_URL 未配置',
      data: null
    });
  }

  return new Promise((resolve, reject) => {
    try {
      if (showLoading) {
        wx.showLoading({ title: '请求中...', mask: true });
      }

      // 对于分解请求，设置更长的超时时间（5分钟）
      const timeout = (url.includes('/factorize/factorize')) ? 300000 : 60000;

      wx.request({
        url: BASE_URL + url,
        method,
        data,
        timeout: timeout,  // 设置超时时间（毫秒）
        header: {
          'Content-Type': 'application/json',
          'Authorization': getAuthToken()
        },
        success: (res) => {
          if (showLoading) {
            wx.hideLoading();
          }

          // 检查HTTP状态码
          if (res && res.statusCode >= 200 && res.statusCode < 300) {
            // 成功：返回后端数据（通常格式为 { success, data, message }）
            // 确保返回的数据格式正确
            const result = res.data || {};
            // 确保 result 是对象
            if (typeof result !== 'object' || result === null) {
              console.warn('requestApi: 后端返回的数据格式不正确', result);
              resolve({
                success: false,
                message: '后端返回数据格式错误',
                data: null
              });
              return;
            }
            // 如果后端返回的数据没有 success 字段，添加默认值
            if (typeof result.success === 'undefined') {
              result.success = true;
            }
            resolve(result);
          } else {
            // HTTP错误状态码
            console.error('requestApi HTTP错误:', res?.statusCode, res?.data);
            const errorMsg = res?.data?.message || `请求失败 (${res?.statusCode || 'unknown'})`;
            showError(errorMsg);
            // 返回错误格式的数据，而不是 reject
            resolve({
              success: false,
              message: errorMsg,
              data: null
            });
          }
        },
        fail: (err) => {
          console.error('requestApi 请求失败:', err);
          if (showLoading) {
            wx.hideLoading();
          }
          const errorMsg = err?.errMsg || '网络请求失败，请检查网络或稍后重试';
          showError(errorMsg);
          // 返回错误格式的数据，而不是 reject，这样 await 不会抛出异常
          resolve({
            success: false,
            message: errorMsg,
            data: null
          });
        }
      });
    } catch (error) {
      if (showLoading) {
        wx.hideLoading();
      }
      console.error('requestApi 异常:', error);
      // 返回错误格式的数据
      resolve({
        success: false,
        message: error?.message || '请求异常',
        data: null
      });
    }
  });
}

/**
 * 检查登录状态
 * @returns {Boolean} 是否已登录
 */
function checkLoginStatus() {
  const app = getApp();
  if (!app || !app.globalData || !app.globalData.isLoggedIn) {
    const currentUser = wx.getStorageSync('currentUser');
    if (!currentUser) {
      wx.reLaunch({
        url: '/pages/login/login'
      });
      return false;
    } else {
      app.globalData.isLoggedIn = true;
      app.globalData.userInfo = currentUser;
    }
  }
  return true;
}

/**
 * 安全设置数据（带错误处理）
 * @param {Object} page - 页面对象
 * @param {Object} data - 要设置的数据
 * @param {Function} callback - 回调函数
 */
function safeSetData(page, data, callback) {
  try {
    if (page && typeof page.setData === 'function') {
      page.setData(data, callback);
    } else {
      console.error('safeSetData: 无效的页面对象');
    }
  } catch (e) {
    console.error('setData错误:', e);
    wx.showToast({
      title: '数据更新失败',
      icon: 'none',
      duration: 2000
    });
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {Number} delay - 延迟时间（毫秒）
 * @returns {Function} 节流后的函数
 */
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      return func.apply(this, args);
    }
  };
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {Number} delay - 延迟时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

/**
 * 格式化时间
 * @param {Date|Number} date - 日期对象或时间戳
 * @returns {String} 格式化后的时间字符串
 */
function formatTime(date) {
  if (!date) return '';
  const d = date instanceof Date ? date : new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');
  const second = String(d.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 安全存储数据（增强版，处理存储空间不足）
 * @param {String} key - 存储键
 * @param {*} data - 要存储的数据
 * @returns {Boolean} 是否成功
 */
function safeSetStorage(key, data) {
  try {
    // 检查存储空间
    const info = wx.getStorageInfoSync();
    const dataSize = JSON.stringify(data).length;
    
    // 如果数据较大，先尝试清理
    if (dataSize > 100000) { // 大于100KB
      cleanupStorage();
    }
    
    wx.setStorageSync(key, data);
    return true;
  } catch (e) {
    console.error('存储数据失败:', e);
    
    // 处理存储空间不足
    if (e.errMsg && e.errMsg.includes('exceed')) {
      // 清理历史记录
      cleanupStorage();
      try {
        wx.setStorageSync(key, data);
        return true;
      } catch (retryError) {
        console.error('清理后重试存储失败:', retryError);
        showError('存储空间不足，请清理历史记录');
        return false;
      }
    }
    
    // 尝试清理空间
    try {
      cleanupStorage();
      wx.setStorageSync(key, data);
      return true;
    } catch (retryError) {
      console.error('重试存储失败:', retryError);
      showError('存储失败，请检查存储空间');
      return false;
    }
  }
}

/**
 * 清理存储空间
 */
function cleanupStorage() {
  try {
    const info = wx.getStorageInfoSync();
    const keys = info.keys || [];
    
    // 保护的关键键
    const protectedKeys = ['currentUser', 'users', 'allUsersDB'];
    
    // 清理历史记录（保留最近50条）
    if (keys.includes('factorHistory')) {
      try {
        const history = wx.getStorageSync('factorHistory') || [];
        if (history.length > 50) {
          wx.setStorageSync('factorHistory', history.slice(0, 50));
        }
      } catch (e) {
        console.error('清理历史记录失败:', e);
      }
    }
    
    // 清理其他非关键数据
    keys.forEach(k => {
      if (!protectedKeys.includes(k) && k !== 'factorHistory') {
        try {
          wx.removeStorageSync(k);
        } catch (e) {
          // 忽略删除失败
        }
      }
    });
  } catch (e) {
    console.error('清理存储空间失败:', e);
  }
}

/**
 * 安全获取存储数据
 * @param {String} key - 存储键
 * @param {*} defaultValue - 默认值
 * @returns {*} 存储的数据或默认值
 */
function safeGetStorage(key, defaultValue = null) {
  try {
    return wx.getStorageSync(key) || defaultValue;
  } catch (e) {
    console.error('获取存储数据失败:', e);
    return defaultValue;
  }
}

/**
 * 显示错误提示
 * @param {String} message - 错误消息
 * @param {Number} duration - 显示时长（毫秒）
 */
function showError(message, duration = 2000) {
  wx.showToast({
    title: message || '操作失败',
    icon: 'none',
    duration: duration
  });
}

/**
 * 显示成功提示
 * @param {String} message - 成功消息
 * @param {Number} duration - 显示时长（毫秒）
 */
function showSuccess(message, duration = 2000) {
  wx.showToast({
    title: message || '操作成功',
    icon: 'success',
    duration: duration
  });
}

/**
 * 检查网络状态
 * @returns {Promise<Boolean>} 是否有网络
 */
function checkNetworkStatus() {
  return new Promise((resolve) => {
    wx.getNetworkType({
      success: (res) => {
        resolve(res.networkType !== 'none');
      },
      fail: () => {
        resolve(false);
      }
    });
  });
}

/**
 * 监控内存使用（简单版本）
 */
function monitorMemory() {
  try {
    const info = wx.getStorageInfoSync();
    const used = info.currentSize || 0;
    const limit = info.limitSize || 10240; // 默认10MB
    
    // 如果使用超过80%，清理空间
    if (used / limit > 0.8) {
      cleanupStorage();
      return true;
    }
    return false;
  } catch (e) {
    console.error('监控内存失败:', e);
    return false;
  }
}

module.exports = {
  BASE_URL,
  requestApi,
  getAuthToken,
  checkLoginStatus,
  safeSetData,
  throttle,
  debounce,
  formatTime,
  safeSetStorage,
  safeGetStorage,
  showError,
  showSuccess,
  cleanupStorage,
  checkNetworkStatus,
  monitorMemory
};

