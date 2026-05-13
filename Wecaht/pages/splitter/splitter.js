// pages/splitter/splitter.js
const app = getApp();
const { validateInput, getNumberType, getFactorizationLevel, millerRabin } = require('../../utils/algorithms.js');
// 增加与 Python 后端交互的统一请求方法
const { safeSetData, throttle, showError, showSuccess, monitorMemory, checkNetworkStatus, requestApi } = require('../../utils/common.js');

Page({
  data: {
    inputNumber: '',
    digitCount: 0,
    maxDigits: 50,
    errorText: '',
    canStart: false,
    inputNumberType: null,
    inputNumberTypeName: '',
    inputNumberTypeDesc: '',
    isCalculating: false,
    hasResult: false,
    progressStatus: '',
    progressPercent: 0,
    iterations: 0,
    originalNumber: '',
    originalNumberBigInt: null,
    factors: [],
    factorizationFormula: '',
    elapsedTime: 0,
    worker: null,
    timeoutId: null,
    startTime: 0,
    numberType: '',
    numberTypeName: '',
    numberTypeDesc: '',
    factorizationLevel: '',
    factorizationLevelName: '',
    factorizationLevelDesc: '',
    // 分解模式：standard 标准模式（优先完全分解），fast 快速部分分解模式
    mode: 'standard'
  },

  onLoad() {
    this.checkLogin();
    // 先从全局变量快速获取用户信息（避免延迟）
    const userInfo = app.getUserInfo();
    if (userInfo) {
      this.setData({
        maxDigits: userInfo.max_digits || userInfo.maxDigits || 50
      });
    }
    // 然后从后端获取最新信息（确保等级改变后能及时更新）
    this.loadUserInfo();
    // 监控内存
    this.startMemoryMonitor();
  },

  // 分解模式切换
  onModeChange(e) {
    const mode = e.detail.value || 'standard';
    this.setData({ mode });
  },

  onShow() {
    this.checkLogin();
    // 检查内存
    monitorMemory();
    // 先从全局变量快速获取用户信息（避免延迟）
    const userInfo = app.getUserInfo();
    if (userInfo) {
      this.setData({
        maxDigits: userInfo.max_digits || userInfo.maxDigits || 50
      });
    }
    // 然后从后端获取最新信息（确保等级改变后能及时更新）
    this.loadUserInfo();
  },

  onUnload() {
    this.stopFactorize();
    this.stopMemoryMonitor();
  },

  // 内存监控
  memoryMonitorInterval: null,
  startMemoryMonitor() {
    // 每30秒检查一次内存
    this.memoryMonitorInterval = setInterval(() => {
      monitorMemory();
    }, 30000);
  },

  stopMemoryMonitor() {
    if (this.memoryMonitorInterval) {
      clearInterval(this.memoryMonitorInterval);
      this.memoryMonitorInterval = null;
    }
  },

  // 检查登录状态
  checkLogin() {
    // 优先从全局变量获取用户信息
    const currentUser = app.getUserInfo();
    if (!currentUser) {
      wx.reLaunch({
        url: '/pages/login/login'
      });
      return false;
    }
    // 确保全局变量已设置
    if (!app.globalData.isLoggedIn || !app.globalData.userInfo) {
      app.globalData.isLoggedIn = true;
      app.globalData.userInfo = currentUser;
    }
    return true;
  },

  onHide() {
    // 页面隐藏时不停止计算，但清理超时
    if (this.data.timeoutId) {
      clearTimeout(this.data.timeoutId);
    }
  },

  // 加载用户信息（从后端获取最新信息）
  async loadUserInfo() {
    try {
      // 先从本地获取（快速显示）
      const localUserInfo = app.getUserInfo();
      if (localUserInfo) {
        this.setData({
          maxDigits: localUserInfo.max_digits || localUserInfo.maxDigits || 50
        });
      }
      
      // 从后端获取最新用户信息（确保等级改变后能及时更新）
      const res = await requestApi({
        url: '/api/auth/user',
        method: 'GET',
        showLoading: false // 不显示加载动画，避免影响用户体验
      });
      
      // 确保 res 存在且格式正确
      if (res && res.success && res.data) {
        const userInfo = res.data;
        // 使用统一方法更新用户信息（确保全局变量和本地存储同步）
        app.updateUserInfo(userInfo);
        
        // 更新页面数据
        this.setData({
          maxDigits: userInfo.max_digits || 50
        });
      } else if (res && !res.success) {
        // API返回了错误响应
        console.warn('获取用户信息失败:', res.message || '未知错误');
      }
    } catch (e) {
      console.error('获取用户信息失败:', e);
      // 如果后端获取失败，使用本地数据
      const localUserInfo = app.getUserInfo();
      if (localUserInfo) {
        this.setData({
          maxDigits: localUserInfo.max_digits || localUserInfo.maxDigits || 50
        });
      }
    }
  },

  // 输入变化
  onInputChange(e) {
    let value = e.detail.value;
    
    // 只允许0-9，过滤掉所有非数字字符
    value = value.replace(/[^0-9]/g, '');
    
    const digitCount = value.length;
    
    this.setData({
      inputNumber: value,
      digitCount: digitCount,
      inputNumberType: null,
      inputNumberTypeName: '',
      inputNumberTypeDesc: ''
    });

    // 验证输入
    const validation = validateInput(value);
    if (validation.valid && value.length > 0) {
      const num = validation.number;
      
      // 识别数字性质
      let numberType = null;
      if (num === 0n) {
        numberType = { type: 'zero', typeName: '非素非合', description: '0既不是素数也不是合数' };
      } else if (num === 1n) {
        numberType = { type: 'unit', typeName: '非素非合', description: '1既不是素数也不是合数' };
      } else {
        // 对于其他数字，先进行快速素性测试
        try {
          const isPrime = millerRabin(num, 3);
          if (isPrime) {
            numberType = { type: 'prime', typeName: '素数', description: '只能被1和自身整除的正整数' };
          } else {
            // 可能是合数，但需要分解才能确定
            // 对于小数字，可以尝试快速判断
            if (num <= 1000000n) {
              // 小数字可以快速判断
              numberType = { type: 'composite', typeName: '合数', description: '有多个因子的正整数' };
            } else {
              // 大数字需要分解才能确定
              numberType = { type: 'unknown', typeName: '未知', description: '需要分解后才能确定数字类型' };
            }
          }
        } catch (e) {
          console.error('判断数字类型失败:', e);
          numberType = { type: 'unknown', typeName: '未知', description: '无法判断数字类型' };
        }
      }
      
      if (numberType) {
        this.setData({
          inputNumberType: numberType.type,
          inputNumberTypeName: numberType.typeName,
          inputNumberTypeDesc: numberType.description
        });
      }
      
      // 0和1可以直接处理，不需要位数限制
      if (num === 0n || num === 1n) {
        this.setData({
          errorText: '',
          canStart: true
        });
      } else if (digitCount > this.data.maxDigits) {
        this.setData({
          errorText: `超过最大位数限制（${this.data.maxDigits}位）`,
          canStart: false
        });
      } else {
        this.setData({
          errorText: '',
          canStart: true
        });
      }
    } else {
      this.setData({
        errorText: validation.error || '',
        canStart: false,
        inputNumberType: null,
        inputNumberTypeName: '',
        inputNumberTypeDesc: ''
      });
    }
  },

  // 开始分解
  startFactorize() {
    // 检查是否正在计算
    if (this.data.isCalculating) {
      showError('正在计算中，请等待完成');
      return;
    }

    const validation = validateInput(this.data.inputNumber);
    if (!validation.valid) {
      showError(validation.error || '输入无效');
      return;
    }

    const num = validation.number;
    const numStr = num.toString();
    
    // 0和1特殊处理（本地即可完成）
    if (num === 0n) {
      this.handleSpecialNumber(0n, '0');
      return;
    }
    if (num === 1n) {
      this.handleSpecialNumber(1n, '1');
      return;
    }

    if (numStr.length > this.data.maxDigits) {
      showError(`超过最大位数限制（${this.data.maxDigits}位）`);
      return;
    }

    // 优先调用 Python 后端进行分解
    this.startBackendFactorize(numStr);
  },

  /**
   * 使用 Python 后端进行分解
   * @param {String} numStr 原始数字字符串
   */
  startBackendFactorize(numStr) {
    const mode = this.data.mode || 'standard';

    this.setData({
      isCalculating: true,
      hasResult: false,
      progressStatus: '请求后端计算中...',
      progressPercent: 10,
      iterations: 0,
      originalNumber: numStr,
      originalNumberBigInt: numStr,
      factors: [],
      factorizationFormula: '',
      elapsedTime: 0,
      errorText: '',
      startTime: Date.now()
    });
    
    // 设置超时处理（5分钟后如果还没响应，提示用户）
    const timeoutId = setTimeout(() => {
      if (this.data.isCalculating) {
        this.setData({
          progressStatus: '计算时间较长，请耐心等待...',
          progressPercent: 50
        });
        wx.showToast({
          title: '计算中，请稍候',
          icon: 'loading',
          duration: 2000
        });
      }
    }, 60000); // 1分钟后提示
    
    // 使用 async/await 方式调用，更清晰
    requestApi({
      url: '/api/factorize/factorize',
      method: 'POST',
      data: {
        number: numStr,
        mode: mode
      },
      showLoading: false  // 分解请求不显示默认的 loading，使用自定义进度
    }).then((res) => {
      // requestApi 返回的 res 已经是后端返回的 JSON 对象
      clearTimeout(timeoutId); // 清除超时提示
      
      console.log('分解响应:', res); // 调试日志
      
      // res 就是后端返回的 { success, data, message } 格式
      if (!res || !res.success) {
        this.setData({
          isCalculating: false,
          progressStatus: '计算失败',
          progressPercent: 0
        });
        showError(res?.message || '分解失败');
        return;
      }

      const result = res.data || {};
      console.log('分解结果:', result); // 调试日志
      
      const elapsedTime = result.elapsed_time || 0;

      // 后端返回的因子格式：[{ value: 'xxx', is_prime: true/false }]
      const factorsWithPrime = (result.factors || []).map(f => ({
        value: String(f.value || f),
        isPrime: !!f.is_prime
      }));

      console.log('处理后的因子:', factorsWithPrime); // 调试日志

      this.setData({
        isCalculating: false,
        hasResult: true,
        progressStatus: '分解完成（后端）',
        progressPercent: 100,
        factors: factorsWithPrime,
        factorizationFormula: result.formula || '',
        elapsedTime: elapsedTime,
        numberType: result.number_type,
        numberTypeName: result.number_type_name,
        numberTypeDesc: result.number_type_desc,
        factorizationLevel: result.factorization_level,
        factorizationLevelName: result.factorization_level_name,
        factorizationLevelDesc: result.factorization_level_desc
      });

      // 本地继续保存一份历史，便于小程序内"历史"页面使用
      try {
        this.saveToHistory();
      } catch (e) {
        console.error('本地保存历史失败:', e);
      }

      showSuccess('分解完成');
    }).catch((err) => {
      clearTimeout(timeoutId); // 清除超时提示
      
      console.error('分解请求异常:', err);
      
      this.setData({
        isCalculating: false,
        progressStatus: '计算失败',
        progressPercent: 0
      });
      
      // 检查是否是超时错误
      if (err && (err.errMsg && err.errMsg.includes('timeout') || err.message && err.message.includes('timeout'))) {
        showError('计算超时，请尝试更小的数字或使用快速模式');
      } else {
        showError(err?.message || '网络请求失败，请检查网络连接');
      }
    });
  },

  // 处理特殊数字（0和1）
  handleSpecialNumber(num, numStr) {
    const startTime = Date.now();
    let factors = [];
    let formula = '';
    let numberType = {};
    let factorizationLevel = {};

    // 保存BigInt到私有变量
    this._originalNumberBigInt = num;

    if (num === 0n) {
      factors = [0n];
      formula = '0';
      numberType = { type: 'zero', typeName: '非素非合', description: '0既不是素数也不是合数' };
      factorizationLevel = { level: 'complete', levelName: '完全分解', description: '0的分解已完成' };
    } else if (num === 1n) {
      factors = [1n];
      formula = '1';
      numberType = { type: 'unit', typeName: '非素非合', description: '1既不是素数也不是合数' };
      factorizationLevel = { level: 'complete', levelName: '完全分解', description: '1的分解已完成' };
    }

    const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(3);

    this.setData({
      isCalculating: false,
      hasResult: true,
      progressStatus: '分解完成',
      progressPercent: 100,
      originalNumber: numStr,
      originalNumberBigInt: num.toString(), // 转换为字符串存储
      factors: factors.map(f => ({
        value: f.toString(),
        isPrime: false
      })),
      factorizationFormula: formula,
      elapsedTime: elapsedTime,
      numberType: numberType.type,
      numberTypeName: numberType.typeName,
      numberTypeDesc: numberType.description,
      factorizationLevel: factorizationLevel.level,
      factorizationLevelName: factorizationLevel.levelName,
      factorizationLevelDesc: factorizationLevel.description
    });

    // 保存到历史
    this.saveToHistory();
  },

  // 停止分解（简化版：只停止前端状态，实际计算在后端）
  stopFactorize() {
    console.log('停止分解被调用');
    this.setData({
      isCalculating: false,
      progressStatus: '已停止',
      errorText: '用户已停止计算'
    });
    showError('计算已停止');
  },

  // 以下函数已废弃，不再使用（所有分解计算已迁移到 Python 后端）
  // checkWorkerSupport() { ... }
  // startWorkerFactorize() { ... }
  // handleFactorizeResult() { ... }
  // startMainThreadFactorize() { ... }
  
  // 使用Worker进行分解（已废弃）
  startWorkerFactorize_OLD(number) {
    // 根据数字大小动态调整超时时间
    const numStr = number.toString();
    const numDigits = numStr.length;
    let timeoutDuration = 30000; // 默认30秒
    
    if (numDigits <= 20) {
      timeoutDuration = 20000; // 20秒
    } else if (numDigits <= 50) {
      timeoutDuration = 30000; // 30秒
    } else if (numDigits <= 100) {
      timeoutDuration = 60000; // 60秒
    } else {
      timeoutDuration = 120000; // 120秒
    }
    
    const that = this;
    
    // 创建Worker，使用相对路径
    let worker;
    try {
      // 检查是否支持Worker
      if (typeof wx === 'undefined' || typeof wx.createWorker === 'undefined') {
        throw new Error('当前环境不支持Worker');
      }
      
      // 尝试创建Worker
      try {
        worker = wx.createWorker('workers/factorWorker.js');
      } catch (createError) {
        // 如果创建失败，回退到主线程计算
        console.warn('Worker创建失败，切换到主线程计算:', createError);
        that.startMainThreadFactorize(number);
        return;
      }
      
      if (!worker) {
        console.warn('Worker返回值为空，切换到主线程计算');
        that.startMainThreadFactorize(number);
        return;
      }
    } catch (e) {
      console.error('创建Worker失败:', e);
      // Worker创建失败，回退到主线程计算
      console.warn('Worker创建失败，切换到主线程计算');
      that.startMainThreadFactorize(number);
      return;
    }
    
    // 设置动态超时
    const timeout = setTimeout(() => {
      if (worker) {
        try {
          worker.terminate();
        } catch (e) {
          console.error('终止Worker失败:', e);
        }
      }
      safeSetData(that, {
        isCalculating: false,
        progressStatus: '计算超时',
        errorText: `计算时间超过${timeoutDuration/1000}秒，请尝试更小的数字`,
        worker: null,
        timeoutId: null
      });
      showError(`计算超时（${timeoutDuration/1000}秒），请尝试更小的数字`);
    }, timeoutDuration);

    // 节流更新进度（每500ms更新一次）
    const throttledProgressUpdate = throttle((data) => {
      safeSetData(that, {
        progressStatus: data.status || '计算中...',
        iterations: data.iterations || that.data.iterations,
        progressPercent: Math.min(95, (data.iterations || 0) / 1000)
      });
    }, 500);

    worker.onMessage((res) => {
      console.log('Worker消息:', res.type, res.data);
      
      if (res.type === 'error') {
        clearTimeout(timeout);
        try {
          worker.terminate();
        } catch (e) {
          console.error('终止Worker失败:', e);
        }
        safeSetData(that, {
          isCalculating: false,
          progressStatus: '计算失败',
          errorText: res.message || '计算过程中发生错误',
          worker: null,
          timeoutId: null
        });
        showError(res.message || '计算失败，请重试');
      } else if (res.type === 'progress') {
        throttledProgressUpdate(res.data);
      } else if (res.type === 'result') {
        clearTimeout(timeout);
        try {
          if (!res.data || !res.data.factors || !Array.isArray(res.data.factors)) {
            throw new Error('Worker返回的数据格式错误');
          }
          
          const factors = res.data.factors.map(f => {
            try {
              return BigInt(f);
            } catch (e) {
              console.error('转换因子失败:', f, e);
              return null;
            }
          }).filter(f => f !== null && f !== undefined);
          
          if (factors.length === 0) {
            throw new Error('没有找到因子');
          }
          
          // 确保传递正确的原始数字
          const originalNum = that._originalNumberBigInt || number;
          that.handleFactorizeResult(factors, originalNum);
        } catch (e) {
          console.error('处理结果失败:', e);
          safeSetData(that, {
            isCalculating: false,
            progressStatus: '结果处理失败',
            errorText: e.message || '处理分解结果时发生错误',
            worker: null,
            timeoutId: null
          });
          showError(e.message || '处理结果失败，请重试');
        } finally {
          try {
            worker.terminate();
          } catch (e) {
            console.error('终止Worker失败:', e);
          }
          that.setData({ worker: null, timeoutId: null });
        }
      } else {
        console.warn('未知的Worker消息类型:', res.type);
      }
    });

    worker.onError((error) => {
      clearTimeout(timeout);
      try {
        worker.terminate();
      } catch (e) {
        console.error('终止Worker失败:', e);
      }
      
      // 详细的错误信息
      let errorMsg = '计算线程错误';
      if (error && error.message) {
        errorMsg = error.message;
      } else if (error && typeof error === 'string') {
        errorMsg = error;
      }
      
      console.error('Worker错误:', error);
      
      // 如果错误是"not support"，切换到主线程计算
      if (errorMsg.includes('not support') || errorMsg.includes('不支持')) {
        console.warn('Worker不支持，切换到主线程计算');
        that.startMainThreadFactorize(number);
        return;
      }
      
      // 其他错误，显示错误信息
      safeSetData(that, {
        isCalculating: false,
        progressStatus: 'Worker错误',
        errorText: '计算线程发生错误，请重试',
        worker: null,
        timeoutId: null
      });
      
      showError(errorMsg || '计算线程错误，请重试');
      
      // 尝试清理内存
      monitorMemory();
    });

    try {
      worker.postMessage({
        type: 'factorize',
        data: {
          number: number.toString()
        }
      });
      this.setData({ worker, timeoutId: timeout });
    } catch (e) {
      clearTimeout(timeout);
      console.error('Worker启动失败:', e);
      // Worker启动失败，切换到主线程计算
      console.warn('Worker启动失败，切换到主线程计算');
      that.startMainThreadFactorize(number);
    }
  },

  // 处理分解结果
  handleFactorizeResult(factors, originalNumber) {
    const elapsedTime = ((Date.now() - this.data.startTime) / 1000).toFixed(3);
    
    // 获取原始数字（从私有变量或参数）
    let originalNum;
    if (originalNumber !== undefined && originalNumber !== null) {
      originalNum = originalNumber;
    } else if (this._originalNumberBigInt !== undefined && this._originalNumberBigInt !== null) {
      originalNum = this._originalNumberBigInt;
    } else {
      // 如果都没有，尝试从data中获取
      const numStr = this.data.originalNumber;
      if (numStr) {
        try {
          originalNum = BigInt(numStr);
        } catch (e) {
          console.error('无法从字符串转换BigInt:', e);
          showError('处理结果时发生错误：无法获取原始数字');
          safeSetData(this, {
            isCalculating: false,
            progressStatus: '处理失败',
            errorText: '无法获取原始数字'
          });
          return;
        }
      } else {
        showError('处理结果时发生错误：原始数字丢失');
        safeSetData(this, {
          isCalculating: false,
          progressStatus: '处理失败',
          errorText: '原始数字丢失'
        });
        return;
      }
    }
    
    // 验证结果
    let product = 1n;
    try {
      factors.forEach(f => {
        if (f !== null && f !== undefined) {
          product = product * f;
        }
      });
    } catch (e) {
      console.error('计算乘积失败:', e);
      showError('验证结果时发生错误');
      safeSetData(this, {
        isCalculating: false,
        progressStatus: '验证失败',
        errorText: '验证结果时发生错误'
      });
      return;
    }

    // 检查是否为部分分解
    const isPartialFactorization = product !== originalNum && factors.length > 0;
    let remaining = null;
    
    if (isPartialFactorization) {
      // 部分分解：计算剩余部分
      remaining = originalNum / product;
      console.log(`部分分解：已找到 ${factors.length} 个因子，剩余部分: ${remaining.toString()}`);
    } else if (product !== originalNum) {
      // 真正的验证失败
      showError('分解结果验证失败，请重试');
      safeSetData(this, {
        isCalculating: false,
        progressStatus: '分解失败',
        errorText: '分解结果验证失败，请重试'
      });
      return;
    }

    // 生成分解式
    const factorCounts = {};
    factors.forEach(f => {
      const key = f.toString();
      factorCounts[key] = (factorCounts[key] || 0) + 1;
    });

    let formula = '';
    for (const [factor, count] of Object.entries(factorCounts)) {
      if (formula) formula += ' × ';
      formula += factor;
      if (count > 1) {
        formula += '^' + count;
      }
    }
    
    // 如果是部分分解，在分解式中添加剩余部分
    if (isPartialFactorization && remaining) {
      formula += ` × [剩余部分: ${remaining.toString()}]`;
    }

    // 判断数字类型
    const numberType = getNumberType(originalNum, factors);
    
    // 判断分解程度
    const factorizationLevel = getFactorizationLevel(originalNum, factors);

    // 验证每个因子是否为素数
    const factorsWithPrime = factors.map(f => {
      try {
        if (f === 0n || f === 1n) {
          return { value: f.toString(), isPrime: false };
        }
        const isPrime = millerRabin(f, 3);
        return { value: f.toString(), isPrime: isPrime };
      } catch (e) {
        console.error('判断因子是否为素数失败:', f, e);
        return { value: f.toString(), isPrime: false };
      }
    });

    this.setData({
      isCalculating: false,
      hasResult: true,
      progressStatus: '分解完成',
      progressPercent: 100,
      factors: factorsWithPrime,
      factorizationFormula: formula,
      elapsedTime: elapsedTime,
      numberType: numberType.type,
      numberTypeName: numberType.typeName,
      numberTypeDesc: numberType.description,
      factorizationLevel: factorizationLevel.level,
      factorizationLevelName: factorizationLevel.levelName,
      factorizationLevelDesc: factorizationLevel.description
    });

    // 自动保存到历史
    this.saveToHistory();
  },

  // 使用主线程进行分解（Worker不可用时的备用方案）
  startMainThreadFactorize(number) {
    const that = this;
    const numStr = number.toString();
    const numDigits = numStr.length;
    const mode = this.data.mode || 'standard';
    
    // 根据数字大小和分解模式动态调整超时时间（总时间不超过3分钟）
    // standard：优先完全分解；fast：更快给出部分分解结果
    let timeoutDuration = 30000;
    if (mode === 'fast') {
      // 快速模式：整体时间更短
      if (numDigits <= 20) {
        timeoutDuration = 10000; // 10秒
      } else if (numDigits <= 40) {
        timeoutDuration = 30000; // 30秒
      } else if (numDigits <= 80) {
        timeoutDuration = 60000; // 60秒
      } else {
        timeoutDuration = 90000; // 最大约90秒
      }
    } else {
      // 标准模式：总时间不超过3分钟
      if (numDigits <= 20) {
        timeoutDuration = 20000; // ≤20位：20秒内力争完全分解
      } else if (numDigits <= 40) {
        timeoutDuration = 60000; // 21–40位：60秒
      } else if (numDigits <= 80) {
        timeoutDuration = 120000; // 41–80位：120秒（2分钟）
      } else {
        timeoutDuration = 180000; // >80位：180秒（3分钟封顶）
      }
    }
    
    const startTime = Date.now();
    let timeoutId = null;
    let isStopped = false;
    
    // 将isStopped存储到that上，以便stopFactorize可以访问
    that._isStopped = () => isStopped;
    that._setIsStopped = (value) => { isStopped = value; };
    
    // 设置超时：优先尝试返回“部分分解”结果，而不是直接报错
    timeoutId = setTimeout(() => {
      isStopped = true;
      
      // 从临时缓存中读取当前已分解的因子
      const partialFactors = that._partialFactors;
      
      if (partialFactors && Array.isArray(partialFactors) && partialFactors.length > 0) {
        console.warn('计算超时，使用部分分解结果返回给用户，因子数量:', partialFactors.length);
        try {
          // 使用当前因子作为结果，handleFactorizeResult 内部会判断是完全还是部分分解
          that.handleFactorizeResult(partialFactors, number);
          
          safeSetData(that, {
            isCalculating: false,
            progressStatus: '部分分解（计算超时，已返回当前最优结果）',
            errorText: '',
            timeoutId: null
          });
        } catch (e) {
          console.error('使用部分分解结果时发生错误:', e);
          safeSetData(that, {
            isCalculating: false,
            progressStatus: '计算超时',
            errorText: `计算时间超过${timeoutDuration/1000}秒，请尝试更小的数字`,
            timeoutId: null
          });
          showError(`计算超时（${timeoutDuration/1000}秒），请尝试更小的数字`);
        }
      } else {
        // 没有任何因子可用，只能按原逻辑提示超时
        safeSetData(that, {
          isCalculating: false,
          progressStatus: '计算超时',
          errorText: `计算时间超过${timeoutDuration/1000}秒，请尝试更小的数字`,
          timeoutId: null
        });
        showError(`计算超时（${timeoutDuration/1000}秒），请尝试更小的数字`);
      }
    }, timeoutDuration);
    
    this.setData({ timeoutId: timeoutId });
    
    // 使用节流更新进度
    let iterationCount = 0;
    const throttledProgressUpdate = throttle((data) => {
      if (isStopped) return;
      iterationCount = data.iterations || iterationCount;
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      const elapsedMinutes = Math.floor(elapsed / 60);
      const elapsedSeconds = elapsed % 60;
      const elapsedStr = elapsedMinutes > 0 ? `${elapsedMinutes}分${elapsedSeconds}秒` : `${elapsedSeconds}秒`;
      const timeoutMinutes = Math.floor(timeoutDuration / 60000);
      const timeoutSeconds = Math.floor((timeoutDuration % 60000) / 1000);
      const timeoutStr = timeoutMinutes > 0 ? `${timeoutMinutes}分${timeoutSeconds}秒` : `${timeoutSeconds}秒`;
      
      // 计算进度百分比（基于已用时间）
      const timeProgress = Math.min(90, (elapsed / (timeoutDuration / 1000)) * 100);
      
      safeSetData(that, {
        progressStatus: `${data.status || '计算中...'} (已用时: ${elapsedStr} / 超时: ${timeoutStr})`,
        iterations: iterationCount,
        progressPercent: Math.min(95, Math.max(timeProgress, iterationCount / 1000))
      });
    }, 500);
    
    // 进度回调
    const progressCallback = (data) => {
      if (isStopped) return;
      iterationCount = data.iterations || iterationCount;
      throttledProgressUpdate({
        status: data.status || '计算中...',
        iterations: iterationCount
      });
    };
    
    // 使用分块计算，避免阻塞UI（改为异步函数）
    const calculateInChunks = async () => {
      try {
        const { factorize, millerRabin, pollardRho, trialDivision, gcd } = require('../../utils/algorithms.js');
        
        // 原始数字（在本作用域内保存，供后续所有函数使用）
        const originalNum = number;
        
        // 处理特殊情况
        if (number === 0n) {
          clearTimeout(timeoutId);
          that.handleSpecialNumber(0n, '0');
          return;
        }
        if (number === 1n) {
          clearTimeout(timeoutId);
          that.handleSpecialNumber(1n, '1');
          return;
        }
        
        const factors = [];
        // 将当前因子数组引用缓存到页面实例上，供超时处理使用（部分分解）
        that._partialFactors = factors;
        
        // 检查是否已完全分解（借用PR文件的思路）
        const ifenough = (num) => {
          let product = 1n;
          for (const f of factors) {
            product = product * f;
          }
          if (product === num) {
            return 0; // 各因子之积 = 原数，已完全分解，结束
          }
          if (product > num) {
            return 1; // 各因子之积 > 原数，错误，结束
          }
          return 2; // 各因子之积 < 原数，还有因子没有分解出来，继续分解
        };
        
        // Pollard's Rho递归分解函数（异步版本，避免阻塞UI）
        const pollardRhoRecursiveAsync = async (num, originalNum) => {
          if (isStopped) return;
          if (num === 1n) return;
          
          // 检查是否已完全分解
          const enoughStatus = ifenough(originalNum);
          if (enoughStatus === 0) {
            return; // 已完全分解，退出
          }
          if (enoughStatus === 1) {
            console.error('错误：因子乘积大于原数');
            return;
          }
          
          // 先检查是否为素数（Miller-Rabin素性检测）
          // 对于大数字，增加Miller-Rabin测试轮数
          // 注意：num可能在试除法循环后改变，所以使用let而不是const
          let numDigits = num.toString().length;
          let mrRounds = numDigits > 100 ? 10 : (numDigits > 150 ? 15 : 5);
          if (millerRabin(num, mrRounds)) {
            factors.push(num);
            progressCallback({
              status: `发现素数因子: ${num}`,
              iterations: factors.length * 100
            });
            return;
          }
          
          // 如果是1，特殊处理
          if (num === 1n) {
            return;
          }
          
          // 先尝试试除法找小因子（循环直到找不到小因子，借用PR文件的思路）
          // 使用异步方式，定期让出控制权
          while (true) {
            if (isStopped) return;
            // 检查是否已完全分解
            const enoughStatus = ifenough(originalNum);
            if (enoughStatus === 0) {
              return; // 已完全分解
            }
            
            let trialFactor = trialDivision(num);
            if (trialFactor) {
              factors.push(trialFactor);
              num = num / trialFactor;
              // 更新numDigits，因为num已经改变
              numDigits = num.toString().length;
              progressCallback({
                status: `找到小因子: ${trialFactor}`,
                iterations: factors.length * 100
              });
              if (num === 1n) return; // 已完全分解
              // 检查是否已完全分解
              if (ifenough(originalNum) === 0) {
                return; // 已完全分解
              }
              // 每找到一个小因子后让出控制权（类似Python的processEvents）
              await new Promise(resolve => setTimeout(resolve, 0));
            } else {
              break; // 没有小因子了，继续其他方法
            }
          }
          
          // 再次检查是否为素数（可能在试除法后变成素数）
          // 对于大数字，增加Miller-Rabin测试轮数
          // numDigits已经在上面更新过了，这里只需要更新mrRounds
          numDigits = num.toString().length;
          mrRounds = numDigits > 100 ? 10 : (numDigits > 150 ? 15 : 5);
          if (millerRabin(num, mrRounds)) {
            factors.push(num);
            progressCallback({
              status: `发现素数因子: ${num}`,
              iterations: factors.length * 100
            });
            return;
          }
          
          // 使用Pollard's Rho算法找因子（异步分块执行，避免阻塞UI）
          // 初始化（借用PR文件的思路）
          let x = [];
          let i = 1;
          x.push(-1n);
          x.push(BigInt(Math.floor(Math.random() * Number(num - 1n)) + 1)); // 随机数
          let y = x[1];
          let k = 2n;
          
          // 检查循环或达到最大迭代次数（优化支持200位，增加迭代次数以提高成功率）
          // numDigits已经在上面更新过了，这里只需要更新maxIterations
          numDigits = num.toString().length;
          let maxIterations;
          if (numDigits <= 20) {
            maxIterations = 100000; // 增加：50000 -> 100000
          } else if (numDigits <= 40) {
            maxIterations = 500000; // 新增：40位以内
          } else if (numDigits <= 50) {
            maxIterations = 1000000; // 增加：200000 -> 1000000
          } else if (numDigits <= 70) {
            maxIterations = 2000000; // 新增：70位以内
          } else if (numDigits <= 100) {
            maxIterations = 5000000; // 增加：500000 -> 5000000
          } else if (numDigits <= 150) {
            maxIterations = 10000000; // 增加：1000000 -> 10000000
          } else {
            maxIterations = 20000000; // 增加：2000000 -> 20000000
          }
          
          // 分块大小：每次处理一定数量的迭代后让出控制权（类似Python的processEvents）
          // Python版本在每次循环迭代后都调用processEvents，我们每处理一定数量迭代后让出控制权
          // 优化：对于大数字，使用更大的块以提高处理速度，但仍保持UI响应
          const chunkSize = numDigits > 150 ? 100 : (numDigits > 100 ? 200 : (numDigits > 50 ? 500 : 1000)); // 优化块大小
          
          // 异步执行循环，定期让出控制权
          const pollardRhoLoop = async () => {
            return new Promise((resolve) => {
              const processChunk = async () => {
                if (isStopped) {
                  resolve(false);
                  return;
                }
                
                let iterationsInChunk = 0;
                
                while (iterationsInChunk < chunkSize) {
                  if (isStopped) {
                    resolve(false);
                    return;
                  }
                  
                  // 检查是否已完全分解（Python版本在循环中每次都检查）
                  let enoughStatus = ifenough(originalNum);
                  if (enoughStatus === 0) {
                    resolve(true); // 已完全分解
                    return;
                  }
                  if (enoughStatus === 1) {
                    console.error('错误：因子乘积大于原数');
                    resolve(false);
                    return;
                  }
                  
                  i++;
                  iterationsInChunk++;
                  
                  // x[i] = (x[i-1]^2 - 1) % n
                  const xPrev = x[i - 1];
                  const xSquared = xPrev * xPrev;
                  x.push((xSquared - 1n) % num);
                  if (x[i] < 0n) {
                    x[i] = x[i] + num;
                  }
                  
                  // 计算最大公约数
                  const diff = (y > x[i]) ? (y - x[i]) : (x[i] - y);
                  let d = gcd(diff, num);
                  
                  if (d > 1n && d < num) {
                    // 找到因子，递归分解（异步）
                    const s = num / d;
                    progressCallback({
                      status: `找到因子: ${d}`,
                      iterations: factors.length * 100
                    });
                    // 异步递归分解，必须等待完成
                    (async () => {
                      try {
                        // 先分解d，再分解s
                        await pollardRhoRecursiveAsync(d, originalNum);
                        // 让出控制权
                        await new Promise(resolve => setTimeout(resolve, 0));
                        await pollardRhoRecursiveAsync(s, originalNum);
                        // 再次让出控制权
                        await new Promise(resolve => setTimeout(resolve, 0));
                        // 检查是否已完全分解
                        const finalStatus = ifenough(originalNum);
                        if (finalStatus === 0) {
                          resolve(true);
                        } else {
                          resolve(false);
                        }
                      } catch (e) {
                        console.error('递归分解失败:', e);
                        resolve(false);
                      }
                    })();
                    return;
                  }
                  
                  // 判环（Brent变体）
                  if (BigInt(i) === k) {
                    y = x[i];
                    k = k * 2n;
                  }
                  
                  // 检查循环（Python版本逻辑：x.index(x[i], 0, i + 1) != i）
                  // 这意味着如果x[i]在x[0]到x[i]之间出现过（不是第一次出现），就退出
                  let foundCycle = false;
                  // 优化：对于大数字，只检查最近的值；对于小数字，检查所有值
                  const checkRange = i > 1000 ? 500 : i; // 大数字只检查最近500个值
                  const startIndex = Math.max(0, i - checkRange);
                  for (let j = startIndex; j < i; j++) {
                    if (x[j] === x[i]) {
                      foundCycle = true;
                      break;
                    }
                  }
                  
                  // 再次检查是否已完全分解（在循环检测后，Python版本在循环中每次都检查）
                  enoughStatus = ifenough(originalNum);
                  if (enoughStatus === 0 || enoughStatus === 1) {
                    // 已完全分解或出错，退出循环
                    if (enoughStatus === 0) {
                      resolve(true);
                    } else {
                      resolve(false);
                    }
                    return;
                  }
                  
                  if (foundCycle || i >= maxIterations) {
                    // 达到最大迭代次数或发现循环，再次检查是否为素数
                    const mrRounds = numDigits > 100 ? 15 : (numDigits > 150 ? 20 : 10);
                    if (millerRabin(num, mrRounds)) {
                      factors.push(num);
                      progressCallback({
                        status: `发现素数因子: ${num}`,
                        iterations: factors.length * 100
                      });
                    } else {
                      // 无法分解，可能是大素数
                      factors.push(num);
                      progressCallback({
                        status: `无法进一步分解: ${num}（可能是大素数）`,
                        iterations: factors.length * 100
                      });
                    }
                    resolve(true);
                    return;
                  }
                  
                  // 定期报告进度
                  if (i % 1000 === 0) {
                    progressCallback({
                      status: `计算中... (迭代: ${i})`,
                      iterations: i
                    });
                  }
                }
                
                // 处理完一个块后，让出控制权给UI线程（类似Python的processEvents）
                setTimeout(() => {
                  processChunk().catch(e => {
                    console.error('处理块失败:', e);
                    resolve(false);
                  });
                }, 0);
              };
              
              processChunk().catch(e => {
                console.error('处理块失败:', e);
                resolve(false);
              });
            });
          };
          
          // 等待循环完成
          await pollardRhoLoop();
        };
        
        // 确保所有因子都是素数的函数（异步）
        // 完全自包含的实现，不依赖外部函数，避免作用域问题
        const ensurePrimeFactors = async function(factorList) {
          console.log('ensurePrimeFactors 开始执行，因子列表长度:', factorList.length);
          
          // 内部递归分解函数，完全自包含
          // 使用函数声明而不是函数表达式，确保提升
          async function decomposeToPrimes(nonPrimeFactor) {
            if (isStopped) return;
            if (nonPrimeFactor === 1n) return;
            
            // 先检查是否为素数
            const fDigits = nonPrimeFactor.toString().length;
            const mrRounds = fDigits > 100 ? 10 : (fDigits > 150 ? 15 : 5);
            if (millerRabin(nonPrimeFactor, mrRounds)) {
              // 已经是素数，直接添加到factors
              if (!factors.includes(nonPrimeFactor)) {
                factors.push(nonPrimeFactor);
              }
              return;
            }
            
            // 不是素数，需要分解
            // 记录分解前的因子数量
            const factorsBefore = factors.length;
            
            // 使用pollardRhoRecursiveAsync分解非素数因子
            await pollardRhoRecursiveAsync(nonPrimeFactor, originalNum);
            
            // 让出控制权
            await new Promise(resolve => setTimeout(resolve, 0));
            
            if (isStopped) return;
            
            // 从factors中提取新添加的因子（在factorsBefore之后的）
            const newFactors = factors.slice(factorsBefore);
            
            // 检查新因子是否都是素数，如果不是，继续递归分解
            for (const newF of newFactors) {
              if (isStopped) return;
              if (newF === 1n) continue;
              
              const newFDigits = newF.toString().length;
              const newFMrRounds = newFDigits > 100 ? 10 : (newFDigits > 150 ? 15 : 5);
              if (!millerRabin(newF, newFMrRounds)) {
                // 如果新因子也不是素数，继续递归分解
                console.log('新因子仍非素数，继续递归分解:', newF.toString());
                await decomposeToPrimes(newF);
                // 让出控制权
                await new Promise(resolve => setTimeout(resolve, 0));
              }
            }
          }
          
          // 遍历所有因子，确保都是素数
          for (const f of factorList) {
            if (isStopped) return;
            if (f === 1n) continue;
            
            // 检查是否为素数
            const fDigits = f.toString().length;
            const mrRounds = fDigits > 100 ? 10 : (fDigits > 150 ? 15 : 5);
            if (!millerRabin(f, mrRounds)) {
              // 如果不是素数，继续分解
              console.log('发现非素数因子，继续分解:', f.toString());
              progressCallback({
                status: `继续分解非素数因子: ${f}`,
                iterations: factors.length * 100
              });
              // 使用内部定义的递归函数
              await decomposeToPrimes(f);
              // 让出控制权
              await new Promise(resolve => setTimeout(resolve, 0));
            }
          }
          
          console.log('ensurePrimeFactors 执行完成');
        };
        
        // 重复分解直到完全分解（异步版本，借用PR文件的repeat思路）
        // 对于大数字，如果在一定时间内不能完全分解，返回部分分解结果
        const repeat = async (n) => {
          // 根据模式设置部分分解检查点时间
          // standard：约60秒，fast：约30秒
          const partialFactorizeTimeout = (mode === 'fast') ? 30000 : 60000;
          const partialFactorizeStartTime = Date.now();
          let isPartialFactorize = false; // 标记是否进入部分分解模式
          
          // 根据数字大小动态调整最大尝试次数
          let maxAttempts;
          if (numDigits <= 20) {
            maxAttempts = 5;
          } else if (numDigits <= 50) {
            maxAttempts = 10;
          } else if (numDigits <= 100) {
            maxAttempts = 20;
          } else {
            maxAttempts = 30; // 大数字增加尝试次数
          }
          let attempts = 0;
          
          // 用于存储部分分解的最佳结果（因子数量最多）
          let bestPartialFactors = [];
          let bestPartialProduct = 1n;
          
          while (attempts < maxAttempts) {
            if (isStopped) return;
            
            // 检查是否超过1分钟（仅对大数字，50位以上）
            if (numDigits > 40 && !isPartialFactorize) {
              const elapsed = Date.now() - partialFactorizeStartTime;
              if (elapsed >= partialFactorizeTimeout) {
                console.log('1分钟内未完全分解，切换到部分分解模式');
                isPartialFactorize = true;
                progressCallback({
                  status: '1分钟内未完全分解，继续寻找更多因子...',
                  iterations: factors.length * 100
                });
              }
            }
            
            attempts++;
            factors.length = 0; // 清空因子列表（Python版本：Factor[:] = []）
            await pollardRhoRecursiveAsync(n, n);
            
            // 让出控制权（类似Python的processEvents）
            await new Promise(resolve => setTimeout(resolve, 0));
            
            const enoughStatus = ifenough(n);
            if (enoughStatus === 0) {
              // 已完全分解，排序并返回（Python版本：Factor.sort(reverse=False)）
              factors.sort((a, b) => {
                if (a < b) return -1;
                if (a > b) return 1;
                return 0;
              });
              break;
            }
            
            if (enoughStatus === 1) {
              // 错误：因子乘积大于原数
              console.error('错误：因子乘积大于原数');
              break;
            }
            
            // 如果未完全分解（enoughStatus === 2），继续尝试
            if (enoughStatus === 2) {
              // 计算当前部分分解的乘积
              let product = 1n;
              for (const f of factors) {
                product = product * f;
              }
              
              // 如果当前部分分解的因子数量更多，保存为最佳部分分解
              if (factors.length > bestPartialFactors.length || 
                  (factors.length === bestPartialFactors.length && product > bestPartialProduct)) {
                bestPartialFactors = [...factors];
                bestPartialProduct = product;
              }
              
              // 如果进入部分分解模式，继续尝试找到更多因子
              if (isPartialFactorize) {
                progressCallback({
                  status: `部分分解模式：已找到 ${factors.length} 个因子，继续寻找... (尝试 ${attempts}/${maxAttempts})`,
                  iterations: factors.length * 100
                });
                
                // 计算剩余部分，继续分解
                const remaining = n / product;
                if (remaining > 1n && remaining !== n) {
                  await pollardRhoRecursiveAsync(remaining, n);
                  // 让出控制权
                  await new Promise(resolve => setTimeout(resolve, 0));
                  
                  // 更新最佳部分分解
                  product = 1n;
                  for (const f of factors) {
                    product = product * f;
                  }
                  if (factors.length > bestPartialFactors.length || 
                      (factors.length === bestPartialFactors.length && product > bestPartialProduct)) {
                    bestPartialFactors = [...factors];
                    bestPartialProduct = product;
                  }
                }
              } else {
                progressCallback({
                  status: `继续分解剩余部分... (尝试 ${attempts}/${maxAttempts})`,
                  iterations: factors.length * 100
                });
                // 计算剩余部分
                const remaining = n / product;
                if (remaining > 1n && remaining !== n) {
                  await pollardRhoRecursiveAsync(remaining, n);
                  // 让出控制权
                  await new Promise(resolve => setTimeout(resolve, 0));
                }
              }
            }
            
            // 再次检查
            const finalStatus = ifenough(n);
            if (finalStatus === 0) {
              factors.sort((a, b) => {
                if (a < b) return -1;
                if (a > b) return 1;
                return 0;
              });
              break;
            }
            
            // 如果进入部分分解模式，且已经找到一些因子，可以提前返回
            if (isPartialFactorize && bestPartialFactors.length > 0) {
              // 继续尝试几次，看能否找到更多因子
              if (attempts >= maxAttempts || (Date.now() - partialFactorizeStartTime) >= partialFactorizeTimeout * 2) {
                // 使用最佳部分分解结果
                factors.length = 0;
                factors.push(...bestPartialFactors);
                factors.sort((a, b) => {
                  if (a < b) return -1;
                  if (a > b) return 1;
                  return 0;
                });
                console.log(`部分分解完成，找到 ${factors.length} 个因子`);
                break;
              }
            }
            
            // 如果仍然未完全分解，继续下一次尝试
            if (attempts >= maxAttempts) {
              // 如果有部分分解结果，使用最佳结果
              if (bestPartialFactors.length > 0 && factors.length < bestPartialFactors.length) {
                factors.length = 0;
                factors.push(...bestPartialFactors);
                factors.sort((a, b) => {
                  if (a < b) return -1;
                  if (a > b) return 1;
                  return 0;
                });
                console.log(`达到最大尝试次数，使用部分分解结果，找到 ${factors.length} 个因子`);
              } else {
                console.warn(`达到最大尝试次数(${maxAttempts})，可能无法完全分解`);
              }
              break;
            }
          }
        };
        
        // 开始分解（异步）
        await repeat(number);
        
        if (isStopped) return;
        
        clearTimeout(timeoutId);
        
        // 最终验证：确保所有因子都是素数
        // ensurePrimeFactors 已经在函数中定义，这里直接使用
        if (typeof ensurePrimeFactors === 'undefined') {
          console.error('错误：ensurePrimeFactors 未定义！');
          throw new Error('ensurePrimeFactors 未定义');
        }
        await ensurePrimeFactors(factors);
        
        // 使用factors作为最终结果（ensurePrimeFactors已经将所有非素数因子分解为素数）
        const resultFactors = factors.filter(f => f !== 1n);
        
        // 验证结果
        let product = 1n;
        resultFactors.forEach(f => {
          product = product * f;
        });
        
        // 检查是否为部分分解
        const isPartialFactorization = product !== number && resultFactors.length > 0;
        
        if (product !== number && !isPartialFactorization) {
          // 如果乘积不等于原数且没有找到任何因子，才是真正的失败
          console.error('分解结果验证失败:', { 
            product: product.toString(), 
            number: number.toString(),
            factors: resultFactors.map(f => f.toString())
          });
          safeSetData(that, {
            isCalculating: false,
            progressStatus: '分解失败',
            errorText: '分解结果验证失败',
            timeoutId: null
          });
          showError('分解结果验证失败，请重试');
          return;
        }
        
        // 如果是部分分解，计算剩余部分
        if (isPartialFactorization) {
          const remaining = number / product;
          console.log(`部分分解：已找到 ${resultFactors.length} 个因子，剩余部分: ${remaining.toString()}`);
          progressCallback({
            status: `部分分解完成：找到 ${resultFactors.length} 个因子，剩余部分: ${remaining.toString()}`,
            iterations: resultFactors.length * 100
          });
        }
        
        // 排序因子
        resultFactors.sort((a, b) => {
          if (a < b) return -1;
          if (a > b) return 1;
          return 0;
        });
        
        // 最终验证：确保所有因子都是素数
        // 对于大数字，增加Miller-Rabin测试轮数
        const originalDigits = number.toString().length;
        const mrRounds = originalDigits > 100 ? 10 : (originalDigits > 150 ? 15 : 5);
        const allPrime = resultFactors.every(f => {
          if (f === 0n || f === 1n) return true;
          return millerRabin(f, mrRounds);
        });
        if (!allPrime) {
          console.warn('警告：部分因子可能不是素数', resultFactors.map(f => f.toString()));
        }
        
        console.log('分解完成，因子数量:', resultFactors.length, '所有因子都是素数:', allPrime);
        
        // 处理结果
        that.handleFactorizeResult(resultFactors, number);
        that.setData({ timeoutId: null });
      } catch (e) {
        if (isStopped) {
          console.log('计算已停止，忽略错误');
          return;
        }
        clearTimeout(timeoutId);
        console.error('主线程计算失败:', e);
        console.error('错误堆栈:', e.stack);
        // 设置停止标志
        isStopped = true;
        if (that._setIsStopped) {
          that._setIsStopped(true);
        }
        safeSetData(that, {
          isCalculating: false,
          progressStatus: '计算失败',
          errorText: e.message || '计算过程中发生错误',
          timeoutId: null
        });
        showError(e.message || '计算失败，请重试');
      } finally {
        // 确保清理资源
        if (timeoutId) {
          clearTimeout(timeoutId);
        }
        // 清除停止标志和临时缓存的引用
        if (that._isStopped) {
          delete that._isStopped;
        }
        if (that._setIsStopped) {
          delete that._setIsStopped;
        }
        if (that._partialFactors) {
          delete that._partialFactors;
        }
      }
    };
    
    // 对于大数字，使用更细粒度的分块计算，避免阻塞UI
    // 在下一个事件循环中开始计算
    if (numDigits > 100) {
      // 大数字使用更小的延迟，分多次执行
      setTimeout(() => {
        calculateInChunks();
      }, 50);
    } else {
      setTimeout(calculateInChunks, 100);
    }
  },

  // 停止分解
  stopFactorize() {
    console.log('停止分解被调用');
    
    // 停止Worker
    if (this.data.worker) {
      try {
        this.data.worker.terminate();
      } catch (e) {
        console.error('终止Worker失败:', e);
      }
      this.setData({
        worker: null,
        isCalculating: false,
        progressStatus: '已停止'
      });
    }
    
    // 清除超时
    if (this.data.timeoutId) {
      clearTimeout(this.data.timeoutId);
      this.setData({ timeoutId: null });
    }
    
    // 设置停止标志（如果存在）
    if (this._setIsStopped) {
      this._setIsStopped(true);
      console.log('已设置isStopped为true');
    }
    
    // 更新UI状态
    this.setData({
      isCalculating: false,
      progressStatus: '已停止',
      errorText: '用户已停止计算'
    });
    
    console.log('停止分解完成');
  },

  // 保存到历史
  saveToHistory() {
    if (!this.data.hasResult) return;

    try {
      // 获取当前用户信息
      const userInfo = app.getUserInfo();
      let userInfoForHistory = {
        username: '未知',
        gender: '未知',
        age: '未知',
        birthYear: '未知',
        birthMonth: '未知',
        birthDay: '未知',
        job: '未知'
      };
      
      if (userInfo) {
        userInfoForHistory.username = userInfo.username || '未知';
        userInfoForHistory.gender = userInfo.genderName || userInfo.gender || '未知';
        
        // 优先使用出生日期，如果没有则使用年龄
        if (userInfo.birthYear && userInfo.birthMonth) {
          userInfoForHistory.birthYear = userInfo.birthYear;
          userInfoForHistory.birthMonth = userInfo.birthMonth;
          if (userInfo.birthDay) {
            userInfoForHistory.birthDay = userInfo.birthDay;
          }
          // 计算年龄
          const currentDate = new Date();
          const currentYear = currentDate.getFullYear();
          const currentMonth = currentDate.getMonth() + 1;
          const currentDay = currentDate.getDate();
          let age = currentYear - userInfo.birthYear;
          if (currentMonth < userInfo.birthMonth || 
              (currentMonth === userInfo.birthMonth && (userInfo.birthDay ? currentDay < userInfo.birthDay : currentDate.getDate() < 1))) {
            age--;
          }
          userInfoForHistory.age = age;
        } else if (userInfo.age) {
          userInfoForHistory.age = userInfo.age;
        }
        
        userInfoForHistory.job = userInfo.job || '未知';
      }

      // 检查存储空间
      if (!monitorMemory()) {
        // 如果内存紧张，只保存关键信息
        const record = {
          number: this.data.originalNumber,
          factors: this.data.factors.map(f => f.value).slice(0, 10), // 只保存前10个因子
          formula: this.data.factorizationFormula.substring(0, 200), // 限制长度
          time: new Date().toLocaleString(),
          elapsedTime: this.data.elapsedTime,
          numberType: this.data.numberTypeName,
          factorizationLevel: this.data.factorizationLevelName,
          user: userInfoForHistory
        };
        app.addHistory(record);
      } else {
        const record = {
          number: this.data.originalNumber,
          factors: this.data.factors.map(f => f.value),
          formula: this.data.factorizationFormula,
          time: new Date().toLocaleString(),
          elapsedTime: this.data.elapsedTime,
          numberType: this.data.numberTypeName,
          factorizationLevel: this.data.factorizationLevelName,
          user: userInfoForHistory
        };
        app.addHistory(record);
      }
      showSuccess('已保存到历史');
    } catch (e) {
      console.error('保存历史失败:', e);
      showError('保存历史失败，存储空间可能不足');
    }
  },

  // 复制结果
  copyResult() {
    const text = `原数：${this.data.originalNumber}\n数字类型：${this.data.numberTypeName}\n分解程度：${this.data.factorizationLevelName}\n因子：${this.data.factors.map(f => f.value).join(', ')}\n分解式：${this.data.factorizationFormula}\n耗时：${this.data.elapsedTime}秒`;
    wx.setClipboardData({
      data: text,
      success: () => {
        showSuccess('已复制到剪贴板');
      },
      fail: () => {
        showError('复制失败');
      }
    });
  }
});

