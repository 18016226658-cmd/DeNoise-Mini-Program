// pages/admin/admin.js
const app = getApp();
const { checkLoginStatus, showError, showSuccess, requestApi } = require('../../utils/common.js');

Page({
  data: {
    userList: [],
    totalUsers: 0,
    normalCount: 0,
    vipCount: 0,
    svipCount: 0,
    adminCount: 0,
    filterLevel: 'all'
  },

  onLoad() {
    this.checkAdmin();
    this.loadUsers();
  },

  onShow() {
    this.checkAdmin();
    this.loadUsers();
  },

  // 检查管理员权限（前端快速判断 + 后端再次校验）
  checkAdmin() {
    const currentUser = app.getUserInfo();
    if (!currentUser || currentUser.level !== 'admin') {
      showError('只有管理员可以访问此页面');
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      return false;
    }
    return true;
  },

  // 加载用户列表（从后端获取）
  async loadUsers() {
    if (!this.checkAdmin()) return;

    const level = this.data.filterLevel || 'all';

    try {
      const res = await requestApi({
        url: '/api/admin/users',
        method: 'GET',
        data: {
          level: level
        },
        showLoading: false
      });

      // 确保 res 存在且格式正确
      if (!res || typeof res !== 'object') {
        console.error('获取用户列表失败: res 格式不正确', res);
        showError('获取用户列表失败：服务器返回数据格式错误');
        return;
      }

      if (!res.success) {
        showError(res.message || '获取用户列表失败');
        return;
      }

      const payload = res.data || {};
      const users = payload.users || [];
      const stats = payload.stats || {};

      this.setData({
        userList: users,
        totalUsers: stats.total || users.length,
        normalCount: stats.normal || 0,
        vipCount: stats.vip || 0,
        svipCount: stats.svip || 0,
        adminCount: stats.admin || 0
      });
    } catch (error) {
      console.error('加载用户列表异常:', error);
      showError(error.message || '获取用户列表失败');
    }
  },

  // 设置筛选
  setFilter(e) {
    const level = e.currentTarget.dataset.level;
    this.setData({
      filterLevel: level
    });
    this.loadUsers();
  },

  // 查看用户详情（使用当前列表数据）
  viewUserDetail(e) {
    const username = e.currentTarget.dataset.username;
    const user = (this.data.userList || []).find(u => u.username === username);

    if (!user) {
      showError('用户不存在');
      return;
    }

    // 构建用户详情信息
    let detailContent = `用户名：${user.username}\n`;
    detailContent += `用户等级：${user.level_name || user.level || '未知'}\n`;
    detailContent += `最大分解位数：${user.max_digits || 50}位\n`;
    
    if (user.gender_name || user.gender) {
      detailContent += `性别：${user.gender_name || (user.gender === 'male' ? '男' : user.gender === 'female' ? '女' : '其他')}\n`;
    }
    
    if (user.birth_year && user.birth_month) {
      if (user.birth_day) {
        detailContent += `出生日期：${user.birth_year}年${user.birth_month}月${user.birth_day}日\n`;
      } else {
        detailContent += `出生年月：${user.birth_year}年${user.birth_month}月\n`;
      }
      if (user.age) {
        detailContent += `年龄：${user.age}岁\n`;
      }
    } else if (user.age) {
      detailContent += `年龄：${user.age}岁\n`;
    }
    
    if (user.job) {
      detailContent += `工作：${user.job}\n`;
    }
    
    if (user.create_time) {
      detailContent += `注册时间：${user.create_time}\n`;
    }
    
    if (user.last_login_time) {
      detailContent += `最后登录：${user.last_login_time}\n`;
    }
    
    detailContent += `登录次数：${user.login_count || 0}次`;

    wx.showModal({
      title: '用户详情',
      content: detailContent,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 编辑用户（调用后端修改等级）
  editUser(e) {
    const username = e.currentTarget.dataset.username;
    const user = (this.data.userList || []).find(u => u.username === username);

    if (!user) {
      showError('用户不存在');
      return;
    }

    // 显示修改等级选项
    const levels = [
      { level: 'normal', name: '普通用户', maxDigits: 50 },
      { level: 'vip', name: 'VIP用户', maxDigits: 80 },
      { level: 'svip', name: 'SVIP用户', maxDigits: 120 },
      { level: 'admin', name: '管理员', maxDigits: 200 }
    ];

    const items = levels.map(l => l.name);

    wx.showActionSheet({
      itemList: items,
      success: (res) => {
        const selected = levels[res.tapIndex];
        
        // 确认修改
        wx.showModal({
          title: '确认修改',
          content: `确定要将用户"${username}"的等级修改为"${selected.name}"吗？`,
          success: (modalRes) => {
            if (modalRes.confirm) {
              (async () => {
                try {
                  const resp = await requestApi({
                    url: `/api/admin/users/${user.id}/level`,
                    method: 'PUT',
                    data: {
                      level: selected.level
                    },
                    showLoading: true
                  });

                  if (!resp || typeof resp !== 'object' || !resp.success) {
                    showError(resp?.message || '用户等级修改失败');
                    return;
                  }

                  // 如果被修改的是当前登录用户，需要更新全局变量
                  const currentUser = app.getUserInfo();
                  if (currentUser && currentUser.username === username) {
                    // 更新全局变量和本地存储
                    const updatedUser = resp.data || user;
                    wx.setStorageSync('currentUser', updatedUser);
                    app.globalData.userInfo = updatedUser;
                    app.updateUserInfo(updatedUser);
                    
                    // 提示用户需要刷新页面以看到新的权限
                    wx.showModal({
                      title: '权限已更新',
                      content: '您的用户等级已更新，部分页面可能需要刷新才能看到新的权限。',
                      showCancel: false,
                      confirmText: '知道了'
                    });
                  }

                  showSuccess('用户等级修改成功');
                  this.loadUsers();
                } catch (error) {
                  console.error('修改用户等级异常:', error);
                  showError(error.message || '用户等级修改失败');
                }
              })();
            }
          }
        });
      }
    });
  },

});

