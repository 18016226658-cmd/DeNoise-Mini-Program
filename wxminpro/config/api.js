// ============================================
// API配置文件
// ============================================
// 功能：统一管理所有API端点和服务器地址
// 说明：所有API调用都应使用此文件中定义的endpoints，避免硬编码

// ============================================
// 1. 环境配置
// ============================================
const config = {
  // 开发环境配置
  development: {
    baseURL: 'http://127.0.0.1:5000',  // 本地开发服务器地址（改回5000）
    timeout: 30000                      // 请求超时时间（30秒）
  },
  // 生产环境配置
  production: {
    baseURL: 'https://your-production-domain.com',  // ⚠️ 请修改为实际生产服务器地址
    timeout: 30000
  }
}

// ============================================
// 2. 选择当前环境
// ============================================
// 根据环境变量选择配置（可以在project.config.json中配置）
// 开发时使用'development'，发布时改为'production'
const env = 'development' // 或从环境变量获取：process.env.NODE_ENV
const apiConfig = config[env]

// ============================================
// 3. 导出配置
// ============================================
module.exports = {
  baseURL: apiConfig.baseURL,    // 服务器基础URL
  timeout: apiConfig.timeout,    // 请求超时时间
  // ============================================
  // API端点定义（所有接口路径）
  // ============================================
  endpoints: {
    // ============================================
    // 用户相关接口
    // ============================================
    login: '/api/Login',                    // 用户登录（手机号+密码）
    loginAudio: '/api/LoginAudio',          // 音频系统登录
    register: '/api/Register',              // 用户注册
    registerAudio: '/api/RegisterAudio',    // 音频系统注册
    editUser: '/api/EditUser',              // 获取用户列表（管理员功能）
    updateUserInfo: '/api/UpdateUserInfo',   // 更新用户信息
    delUser: '/api/DelUser',               // 删除用户
    saveUserType: '/api/SaveUserType',      // 保存用户类型（修改用户权限）
    receiveFaceImg: '/api/ReceiveFaceImg',  // 接收头像图片上传
    dispUser: '/api/DispUser',             // 显示用户列表
    
    // ============================================
    // 音频降噪相关接口
    // ============================================
    uploadAudio: '/api/uploadAudio',        // 上传音频文件到服务器
    getAudioInfo: '/api/getAudioInfo',      // 获取音频文件信息（时长、大小、格式等）
    deNoiseAudio: '/api/DeNoiseAudio',      // 音频降噪处理
    downloadDeNoise: '/api/DownloadDeNoise', // 下载降噪后的音频文件
    getDeNoiseHistory: '/api/getDeNoiseHistory', // 获取降噪历史记录
    playAudio: '/api/audio/play',           // 播放音频文件（用于试听）
    
    // ============================================
    // 音频分离相关接口
    // ============================================
    separateAudio: '/api/separateAudio',    // 音频分离（人声/伴奏分离）
    downloadAudio: '/api/downloadAudio',    // 下载分离后的音频文件
    soundRecordFile: '/api/SoundRecordFile', // 上传录音文件
    
    // ============================================
    // 其他接口
    // ============================================
    formPost: '/api/FormPost',             // 表单提交（电话登录验证码等）
    getCode: '/api/GetCode',                // 获取验证码
    getStatistics: '/api/getStatistics',      // 获取统计数据（原始 JSON，暂保留）
    getStatisticsImages: '/api/getStatisticsImages', // 获取可视化图片路径（管理员功能）
    regenerateVisualization: '/api/regenerateVisualization' // 重新生成可视化图表（管理员功能）
  }
}
