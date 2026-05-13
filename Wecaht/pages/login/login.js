// pages/login/login.js
const app = getApp();
// 后端相关工具：统一请求方法 + 提示
const { requestApi, showError, showSuccess } = require('../../utils/common.js');

Page({
  data: {
    showRegister: false,
    loginUsername: '',
    loginPassword: '',
    showLoginPassword: false,
    rememberPassword: false,
    registerUsername: '',
    registerPassword: '',
    showRegisterPassword: false,
    registerPasswordConfirm: '',
    showRegisterPasswordConfirm: false,
    registerGender: '',
    genderIndex: 0,
    genderOptions: [
      { value: 'male', label: '男' },
      { value: 'female', label: '女' },
      { value: 'other', label: '其他' }
    ],
    registerBirthYear: '',
    registerBirthMonth: '',
    registerBirthDay: '',
    birthYearMonthDayIndex: [0, 0, 0],
    birthYearMonthDay: (function() {
      // 直接在data中初始化，确保数据立即可用
      const years = [];
      const months = [];
      const days = [];
      
      // 年份：1949-2049
      for (let year = 1949; year <= 2049; year++) {
        years.push(year + '年');
      }
      
      // 月份：1-12
      for (let month = 1; month <= 12; month++) {
        months.push(month + '月');
      }
      
      // 日期：1-31（默认）
      for (let day = 1; day <= 31; day++) {
        days.push(day + '日');
      }
      
      return [years, months, days];
    })(),
    selectedUserType: 0,
    userTypes: [
      { level: 'normal', name: '普通用户', maxDigits: 50 }
    ]
  },

  onLoad() {
    // 检查是否已登录
    this.checkLoginStatus();
    // 加载记住的密码
    this.loadRememberedPassword();
    // 初始化值数组（用于获取实际数值）
    this.initValueArrays();
  },

  // 初始化值数组（用于在选择时获取实际数值）
  initValueArrays() {
    const yearValues = [];
    const monthValues = [];
    const dayValues = [];
    
    // 年份值：1949-2049
    for (let year = 1949; year <= 2049; year++) {
      yearValues.push(year);
    }
    
    // 月份值：1-12
    for (let month = 1; month <= 12; month++) {
      monthValues.push(month);
    }
    
    // 日期值：1-31（默认）
    for (let day = 1; day <= 31; day++) {
      dayValues.push(day);
    }
    
    // 保存值数组供选择时使用
    this._birthYearValues = yearValues;
    this._birthMonthValues = monthValues;
    this._birthDayValues = dayValues;
  },

  // 根据年月获取该月的天数
  getDaysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
  },

  // 更新日期数组（当年月变化时）
  updateDaysArray(year, month) {
    const days = [];
    const dayValues = [];
    const daysInMonth = this.getDaysInMonth(year, month);
    
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day + '日');
      dayValues.push(day);
    }
    
    // 更新值数组
    this._birthDayValues = dayValues;
    
    // 更新显示数组
    const birthYearMonthDay = [...this.data.birthYearMonthDay];
    birthYearMonthDay[2] = days;
    
    this.setData({
      birthYearMonthDay: birthYearMonthDay
    });
  },

  // 检查登录状态
  checkLoginStatus() {
    // 优先从全局变量获取用户信息
    const currentUser = app.getUserInfo();
    if (currentUser) {
      // 已登录，跳转到首页
      wx.switchTab({
        url: '/pages/home/home'
      });
    }
  },

  // 加载记住的密码
  loadRememberedPassword() {
    try {
      const remembered = wx.getStorageSync('rememberedLogin');
      if (remembered && remembered.username) {
        this.setData({
          loginUsername: remembered.username,
          loginPassword: remembered.password || '',
          rememberPassword: true
        });
      }
    } catch (e) {
      console.error('加载记住密码失败:', e);
    }
  },

  // 登录用户名输入
  onLoginUsernameInput(e) {
    this.setData({
      loginUsername: e.detail.value
    });
  },

  // 登录密码输入
  onLoginPasswordInput(e) {
    this.setData({
      loginPassword: e.detail.value
    });
  },

  // 记住密码切换
  onRememberPasswordChange(e) {
    this.setData({
      rememberPassword: e.detail.value
    });
  },

  // 切换登录密码显示/隐藏
  toggleLoginPassword(e) {
    if (e) {
      e.stopPropagation && e.stopPropagation();
    }
    const currentState = this.data.showLoginPassword;
    console.log('切换密码显示状态:', currentState, '->', !currentState);
    this.setData({
      showLoginPassword: !currentState
    });
  },

  // 切换注册密码显示/隐藏
  toggleRegisterPassword(e) {
    if (e) {
      e.stopPropagation && e.stopPropagation();
    }
    this.setData({
      showRegisterPassword: !this.data.showRegisterPassword
    });
  },

  // 切换确认密码显示/隐藏
  toggleRegisterPasswordConfirm(e) {
    if (e) {
      e.stopPropagation && e.stopPropagation();
    }
    this.setData({
      showRegisterPasswordConfirm: !this.data.showRegisterPasswordConfirm
    });
  },

  // 注册用户名输入
  onRegisterUsernameInput(e) {
    this.setData({
      registerUsername: e.detail.value
    });
  },

  // 注册密码输入
  onRegisterPasswordInput(e) {
    this.setData({
      registerPassword: e.detail.value
    });
  },

  // 注册确认密码输入
  onRegisterPasswordConfirmInput(e) {
    this.setData({
      registerPasswordConfirm: e.detail.value
    });
  },

  // 性别选择
  onGenderChange(e) {
    const index = parseInt(e.detail.value);
    const selected = this.data.genderOptions[index];
    this.setData({
      genderIndex: index,
      registerGender: selected.label
    });
  },

  // 出生日期选择
  onBirthYearMonthDayChange(e) {
    const index = e.detail.value;
    
    // 确保索引有效
    if (!index || index.length < 3 || 
        !this._birthYearValues || !this._birthMonthValues || !this._birthDayValues) {
      console.error('出生日期选择器数据无效:', { index });
      return;
    }
    
    // 从值数组中获取实际值
    const selectedYear = this._birthYearValues[index[0]];
    const selectedMonth = this._birthMonthValues[index[1]];
    const selectedDay = this._birthDayValues[index[2]];
    
    this.setData({
      birthYearMonthDayIndex: index,
      registerBirthYear: selectedYear,
      registerBirthMonth: selectedMonth,
      registerBirthDay: selectedDay
    });
  },

  // 出生日期列变化
  onBirthYearMonthDayColumnChange(e) {
    const column = e.detail.column;
    const index = e.detail.value;
    const birthYearMonthDayIndex = [...this.data.birthYearMonthDayIndex];
    birthYearMonthDayIndex[column] = index;
    
    // 如果年份或月份变化，需要更新日期数组
    if (column === 0 || column === 1) {
      // 确保值数组已初始化
      if (!this._birthYearValues || !this._birthMonthValues) {
        this.initValueArrays();
      }
      
      let year, month;
      
      if (column === 0) {
        // 年份变化
        year = this._birthYearValues[index] || 2000;
        month = this._birthMonthValues[birthYearMonthDayIndex[1]] || 1;
      } else {
        // 月份变化
        year = this._birthYearValues[birthYearMonthDayIndex[0]] || 2000;
        month = this._birthMonthValues[index] || 1;
      }
      
      // 更新日期数组
      this.updateDaysArray(year, month);
      
      // 如果当前选择的日期超过了新月份的天数，需要调整
      const daysInMonth = this.getDaysInMonth(year, month);
      if (birthYearMonthDayIndex[2] >= daysInMonth) {
        birthYearMonthDayIndex[2] = daysInMonth - 1;
      }
    }
    
    this.setData({
      birthYearMonthDayIndex: birthYearMonthDayIndex
    });
  },

  // 工作输入
  onRegisterJobInput(e) {
    this.setData({
      registerJob: e.detail.value
    });
  },

  // 切换到注册
  switchToRegister() {
    this.setData({
      showRegister: true,
      loginUsername: '',
      loginPassword: '',
      registerGender: '',
      genderIndex: 0,
      registerBirthYear: '',
      registerBirthMonth: '',
      registerBirthDay: '',
      birthYearMonthDayIndex: [0, 0, 0],
      registerJob: ''
    });
  },

  // 切换到登录
  switchToLogin() {
    this.setData({
      showRegister: false,
      registerUsername: '',
      registerPassword: '',
      registerPasswordConfirm: '',
      registerGender: '',
      genderIndex: 0,
      registerBirthYear: '',
      registerBirthMonth: '',
      registerBirthDay: '',
      birthYearMonthDayIndex: [0, 0, 0],
      registerJob: '',
      selectedUserType: 0
    });
  },

  // 处理登录
  async handleLogin() {
    const { loginUsername, loginPassword } = this.data;

    console.log('尝试登录:', { username: loginUsername, passwordLength: loginPassword ? loginPassword.length : 0 });

    if (!loginUsername || !loginPassword) {
      showError('请输入用户名和密码');
      return;
    }

    try {
      // 调用 Python 后端登录接口
      const res = await requestApi({
        url: '/api/auth/login',
        method: 'POST',
        data: {
          username: loginUsername,
          password: loginPassword
        },
        showLoading: true
      });

      // 确保 res 存在且格式正确
      if (!res || typeof res !== 'object') {
        showError('登录失败：服务器返回数据格式错误');
        return;
      }

      if (!res.success) {
        showError(res.message || '登录失败');
        return;
      }

      const payload = res.data || {};
      const user = payload.user;
      if (!user) {
        showError('登录返回数据异常');
        return;
      }

      // 使用统一方法更新用户信息（确保全局变量和本地存储同步）
      app.updateUserInfo(user);

      // 处理记住密码
      if (this.data.rememberPassword) {
        try {
          wx.setStorageSync('rememberedLogin', {
            username: loginUsername,
            password: loginPassword
          });
        } catch (e) {
          console.error('保存记住密码失败:', e);
        }
      } else {
        try {
          wx.removeStorageSync('rememberedLogin');
        } catch (e) {
          console.error('清除记住密码失败:', e);
        }
      }

      showSuccess('登录成功');

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/home/home'
        });
      }, 1500);
    } catch (error) {
      console.error('登录异常:', error);
      showError(error.message || '登录失败，请稍后重试');
    }
  },



  // 处理注册
  async handleRegister() {
    const { registerUsername, registerPassword, registerPasswordConfirm, registerGender, registerBirthYear, registerBirthMonth, registerBirthDay, registerJob, selectedUserType, userTypes } = this.data;

    // 获取当前日期（用于验证和计算年龄）
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;

    // 验证用户名
    if (!registerUsername || registerUsername.length < 3 || registerUsername.length > 20) {
      wx.showToast({
        title: '用户名长度为3-20个字符',
        icon: 'none'
      });
      return;
    }

    // 验证密码
    if (!registerPassword || registerPassword.length < 6) {
      wx.showToast({
        title: '密码至少6位',
        icon: 'none'
      });
      return;
    }

    if (registerPassword !== registerPasswordConfirm) {
      wx.showToast({
        title: '两次密码不一致',
        icon: 'none'
      });
      return;
    }

    // 验证性别
    if (!registerGender) {
      wx.showToast({
        title: '请选择性别',
        icon: 'none'
      });
      return;
    }

    // 验证出生日期
    if (!registerBirthYear || !registerBirthMonth || !registerBirthDay) {
      wx.showToast({
        title: '请选择出生日期',
        icon: 'none'
      });
      return;
    }
    
    // 验证出生日期合理性（不能是未来）
    const currentDay = currentDate.getDate();
    if (registerBirthYear > currentYear || 
        (registerBirthYear === currentYear && registerBirthMonth > currentMonth) ||
        (registerBirthYear === currentYear && registerBirthMonth === currentMonth && registerBirthDay > currentDay)) {
      wx.showToast({
        title: '出生日期不能是未来',
        icon: 'none'
      });
      return;
    }
    
    // 验证日期有效性（检查日期是否在该月有效范围内）
    const daysInMonth = this.getDaysInMonth(registerBirthYear, registerBirthMonth);
    if (registerBirthDay > daysInMonth) {
      wx.showToast({
        title: '选择的日期无效',
        icon: 'none'
      });
      return;
    }

    // 验证工作
    if (!registerJob || registerJob.trim() === '') {
      wx.showToast({
        title: '请输入工作',
        icon: 'none'
      });
      return;
    }

    // 创建新用户（默认只能注册普通用户）——交给后端处理
    const selectedType = userTypes[selectedUserType] || userTypes[0];
    const genderValue = this.data.genderOptions[this.data.genderIndex].value;
    
    // 调用 Python 后端注册接口
    try {
      const res = await requestApi({
        url: '/api/auth/register',
        method: 'POST',
        data: {
          username: registerUsername,
          password: registerPassword,
          password_confirm: registerPasswordConfirm,
          gender: genderValue,
          gender_name: registerGender,
          birth_year: registerBirthYear,
          birth_month: registerBirthMonth,
          birth_day: registerBirthDay,
          job: registerJob.trim()
        },
        showLoading: true
      });

      // 确保 res 存在且格式正确
      if (!res || typeof res !== 'object') {
        showError('注册失败：服务器返回数据格式错误');
        return;
      }

      if (!res.success) {
        showError(res.message || '注册失败');
        return;
      }

      const payload = res.data || {};
      const newUser = payload.user;
      if (!newUser) {
        showError('注册返回数据异常');
        return;
      }

      // 使用统一方法更新用户信息（确保全局变量和本地存储同步）
      app.updateUserInfo(newUser);

      showSuccess('注册成功');

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/home/home'
        });
      }, 1500);
    } catch (error) {
      console.error('注册异常:', error);
      showError(error.message || '注册失败，请稍后重试');
    }
  }
});

