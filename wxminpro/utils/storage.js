// 统一的存储工具类
const STORAGE_KEYS = {
  USER_INFO: 'userInfo',
  AUDIO_INFO: 'audioInfo',
  DE_NOISE_INFO: 'deNoiseInfo',
  USER_AUDIO_INFO: 'userAudioInfo'
}

/**
 * 存储数据
 * @param {string} key 键名
 * @param {any} data 数据
 */
function setStorage(key, data) {
  try {
    wx.setStorageSync(key, data)
    return true
  } catch (e) {
    console.error('存储失败：', e)
    return false
  }
}

/**
 * 获取数据
 * @param {string} key 键名
 * @param {any} defaultValue 默认值
 */
function getStorage(key, defaultValue = null) {
  try {
    const value = wx.getStorageSync(key)
    return value !== '' ? value : defaultValue
  } catch (e) {
    console.error('获取存储失败：', e)
    return defaultValue
  }
}

/**
 * 删除数据
 * @param {string} key 键名
 */
function removeStorage(key) {
  try {
    wx.removeStorageSync(key)
    return true
  } catch (e) {
    console.error('删除存储失败：', e)
    return false
  }
}

/**
 * 清空所有数据
 */
function clearStorage() {
  try {
    wx.clearStorageSync()
    return true
  } catch (e) {
    console.error('清空存储失败：', e)
    return false
  }
}

/**
 * 保存用户信息
 */
function saveUserInfo(userInfo) {
  return setStorage(STORAGE_KEYS.USER_INFO, userInfo)
}

/**
 * 获取用户信息
 */
function getUserInfo() {
  return getStorage(STORAGE_KEYS.USER_INFO, null)
}

/**
 * 保存音频信息
 */
function saveAudioInfo(audioInfo) {
  return setStorage(STORAGE_KEYS.AUDIO_INFO, audioInfo)
}

/**
 * 获取音频信息
 */
function getAudioInfo() {
  return getStorage(STORAGE_KEYS.AUDIO_INFO, null)
}

module.exports = {
  STORAGE_KEYS,
  setStorage,
  getStorage,
  removeStorage,
  clearStorage,
  saveUserInfo,
  getUserInfo,
  saveAudioInfo,
  getAudioInfo
}

