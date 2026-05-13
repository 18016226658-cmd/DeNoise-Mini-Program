// 用户信息工具类
const storage = require('./storage.js')
const app = getApp()

/**
 * 保存用户信息到全局和本地存储
 */
function saveUserInfo(userInfo) {
  // 保存到全局
  app.globalData.userInfo = {
    nickName: userInfo.user_name || userInfo.UserName,
    Phone: userInfo.user_Phone || userInfo.Phone,
    Password: userInfo.user_Password || userInfo.Password,
    Gender: userInfo.user_Gender || userInfo.Gender,
    Birthday: userInfo.user_Birthday || userInfo.Birthday,
    FaceImg: userInfo.user_FaceImg || userInfo.FaceImg,
    UserType: userInfo.user_UserType || userInfo.UserType
  }
  
  // 保存到本地存储
  storage.saveUserInfo(app.globalData.userInfo)
  
  return app.globalData.userInfo
}

/**
 * 从本地存储恢复用户信息
 */
function restoreUserInfo() {
  const userInfo = storage.getUserInfo()
  if (userInfo) {
    app.globalData.userInfo = userInfo
    return userInfo
  }
  return null
}

/**
 * 清除用户信息
 */
function clearUserInfo() {
  app.globalData.userInfo = null
  storage.removeStorage(storage.STORAGE_KEYS.USER_INFO)
}

/**
 * 获取当前用户信息
 */
function getCurrentUserInfo() {
  return app.globalData.userInfo || restoreUserInfo()
}

/**
 * 检查用户是否登录
 */
function isLoggedIn() {
  const userInfo = getCurrentUserInfo()
  return userInfo && userInfo.Phone
}

module.exports = {
  saveUserInfo,
  restoreUserInfo,
  clearUserInfo,
  getCurrentUserInfo,
  isLoggedIn
}

