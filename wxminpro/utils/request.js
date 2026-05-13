// ============================================
// 统一的HTTP请求工具类
// ============================================
// 功能：封装微信小程序的网络请求，提供统一的请求接口
// 特点：
//   1. 自动处理URL拼接（baseURL + endpoint）
//   2. 统一错误处理和用户提示
//   3. 支持JSON和form-urlencoded两种数据格式
//   4. 自动显示/隐藏加载提示
//   5. 统一的超时和错误处理

const apiConfig = require('../config/api.js')  // 导入API配置（baseURL、endpoints等）

/**
 * 统一的请求方法（核心函数）
 * ===========================
 * @param {Object} options 请求配置对象
 *   - url {String}: API端点路径（如：'/api/Login'）或完整URL
 *   - method {String}: HTTP方法（GET、POST等），默认'GET'
 *   - data {Object}: 请求数据，默认{}
 *   - header {Object}: 自定义请求头，默认{}
 *   - timeout {Number}: 超时时间（毫秒），默认30000
 *   - showLoading {Boolean}: 是否显示加载提示，默认true
 *   - loadingText {String}: 加载提示文字，默认'加载中...'
 * @returns {Promise} 返回Promise对象
 *   - resolve: 请求成功时返回响应数据（res.data）
 *   - reject: 请求失败时返回错误对象
 * 
 * 使用示例:
 *   request({
 *     url: '/api/Login',
 *     method: 'POST',
 *     data: { Phone: '13800138000', Password: '123456' },
 *     header: { 'content-type': 'application/x-www-form-urlencoded' }
 *   }).then(res => {
 *     console.log('登录成功', res)
 *   }).catch(err => {
 *     console.error('登录失败', err)
 *   })
 */
function request(options) {
  return new Promise((resolve, reject) => {
    const {
      url,
      method = 'GET',
      data = {},
      header = {},
      timeout = apiConfig.timeout
    } = options

    // 构建完整URL
    const fullURL = url.startsWith('http') ? url : `${apiConfig.baseURL}${url}`

    // 设置默认请求头
    const defaultHeader = {
      'content-type': 'application/json'
    }

    // 合并请求头
    const finalHeader = Object.assign({}, defaultHeader, header)

    // 显示加载提示
    if (options.showLoading !== false) {
      wx.showLoading({
        title: options.loadingText || '加载中...',
        mask: true
      })
    }

    // 根据Content-Type决定数据格式
    let requestData = data
    if (method !== 'GET') {
      if (finalHeader['content-type'] && finalHeader['content-type'].includes('application/x-www-form-urlencoded')) {
        // form-urlencoded 格式，直接传递对象
        requestData = data
      } else {
        // JSON 格式
        requestData = JSON.stringify(data)
      }
    }

    wx.request({
      url: fullURL,
      method: method,
      data: requestData,
      header: finalHeader,
      timeout: timeout,
      success: (res) => {
        wx.hideLoading()
        
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          const errorMsg = res.data?.message || `请求失败，状态码：${res.statusCode}`
          wx.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 2000
          })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('请求失败：', err)
        
        let errorMsg = '网络错误，请检查网络连接'
        if (err.errMsg) {
          if (err.errMsg.includes('timeout')) {
            errorMsg = '请求超时，请稍后重试'
          } else if (err.errMsg.includes('fail')) {
            errorMsg = '网络连接失败'
          }
        }
        
        wx.showToast({
          title: errorMsg,
          icon: 'none',
          duration: 2000
        })
        reject(err)
      }
    })
  })
}

/**
 * GET请求快捷方法
 * ===============
 * @param {String} url API端点路径
 * @param {Object} data 请求参数（会转换为URL查询字符串）
 * @param {Object} options 其他请求选项（header、timeout等）
 * @returns {Promise}
 * 
 * 使用示例:
 *   get('/api/GetUserInfo', { userId: 123 })
 *     .then(res => console.log(res))
 */
function get(url, data = {}, options = {}) {
  return request({
    url,
    method: 'GET',
    data,
    ...options
  })
}

/**
 * POST请求快捷方法
 * ================
 * @param {String} url API端点路径
 * @param {Object} data 请求数据（JSON或form格式）
 * @param {Object} options 其他请求选项
 *   - header: 可设置Content-Type（'application/json'或'application/x-www-form-urlencoded'）
 * @returns {Promise}
 * 
 * 使用示例:
 *   // JSON格式
 *   post('/api/Login', { Phone: '13800138000', Password: '123456' }, {
 *     header: { 'content-type': 'application/json' }
 *   })
 *   
 *   // Form格式
 *   post('/api/Login', { Phone: '13800138000', Password: '123456' }, {
 *     header: { 'content-type': 'application/x-www-form-urlencoded' }
 *   })
 */
function post(url, data = {}, options = {}) {
  return request({
    url,
    method: 'POST',
    data,
    ...options
  })
}

/**
 * 文件上传方法
 * ============
 * @param {String} filePath 本地文件路径（通过wx.chooseImage等API获取）
 * @param {String} url 上传接口路径
 * @param {Object} formData 额外的表单数据（可选）
 * @param {Object} options 上传选项
 *   - name {String}: 文件字段名，默认'file'
 *   - header {Object}: 自定义请求头
 * @returns {Promise} 返回上传结果
 * 
 * 使用示例:
 *   // 上传头像
 *   wx.chooseImage({
 *     success: (res) => {
 *       uploadFile(res.tempFilePaths[0], '/api/ReceiveFaceImg')
 *         .then(result => console.log('上传成功', result))
 *         .catch(err => console.error('上传失败', err))
 *     }
 *   })
 */
function uploadFile(filePath, url, formData = {}, options = {}) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: url.startsWith('http') ? url : `${apiConfig.baseURL}${url}`,
      filePath: filePath,
      name: options.name || 'file',
      formData: formData,
      header: options.header || {
        'Content-Type': 'multipart/form-data'
      },
      success: (res) => {
        try {
          const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data
          resolve(data)
        } catch (e) {
          resolve(res.data)
        }
      },
      fail: (err) => {
        console.error('文件上传失败：', err)
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

module.exports = {
  request,
  get,
  post,
  uploadFile
}

