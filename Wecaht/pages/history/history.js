// pages/history/history.js
const app = getApp();
const { checkLoginStatus, requestApi, showError } = require('../../utils/common.js');

Page({
  data: {
    historyList: [],
    historyCount: 0,
    successCount: 0,
    totalCount: 0,
    completeCount: 0
  },

  onLoad() {
    this.checkLogin();
    this.loadHistory();
    this.loadStats();
  },

  onShow() {
    this.checkLogin();
    this.loadHistory();
    this.loadStats();
  },

  // 检查登录状态
  checkLogin() {
    return checkLoginStatus();
  },

  // 加载历史记录
  async loadHistory() {
    try {
      // 从 Python 后端获取历史记录（当前用户 / 管理员可查看全部）
      const res = await requestApi({
        url: '/api/history/list',
        method: 'GET',
        data: {
          page: 1,
          per_page: 100
        },
        showLoading: false
      });

      // 确保 res 存在且格式正确
      if (!res || typeof res !== 'object') {
        console.error('获取历史记录失败: res 格式不正确', res);
        return;
      }

      if (!res.success) {
        showError(res.message || '获取历史记录失败');
        return;
      }

      const payload = res.data || {};
      const histories = payload.histories || [];

      this.setData({
        historyList: histories,
        historyCount: histories.length,
        successCount: histories.filter(h => h.factorization_level === 'complete').length
      });
    } catch (error) {
      console.error('加载历史记录异常:', error);
      showError(error.message || '获取历史记录失败');
    }
  },

  // 获取历史统计信息
  async loadStats() {
    try {
      const res = await requestApi({
        url: '/api/history/stats',
        method: 'GET',
        showLoading: false
      });

      // 确保 res 存在且格式正确
      if (!res || typeof res !== 'object') {
        console.warn('获取统计信息失败: res 格式不正确', res);
        return;
      }

      if (!res.success) {
        console.warn('获取统计信息失败:', res.message || '未知错误');
        return;
      }

      const payload = res.data || {};
      this.setData({
        totalCount: payload.total_count || 0,
        completeCount: payload.success_count || 0
      });
    } catch (error) {
      console.error('加载统计信息异常:', error);
    }
  },

  // 查看详情
  viewDetail(e) {
    const index = e.currentTarget.dataset.index;
    const item = this.data.historyList[index];
    
    // 构建用户信息字符串
    let userInfoStr = '';
    if (item.user) {
      userInfoStr = `\n\n用户信息：\n姓名：${item.user.username}\n性别：${item.user.gender}`;
      
      // 显示出生日期或年龄
      if (item.user.birthYear && item.user.birthMonth) {
        if (item.user.birthDay) {
          userInfoStr += `\n出生日期：${item.user.birthYear}年${item.user.birthMonth}月${item.user.birthDay}日`;
        } else {
          userInfoStr += `\n出生年月：${item.user.birthYear}年${item.user.birthMonth}月`;
        }
        if (item.user.age && item.user.age !== '未知') {
          userInfoStr += `\n年龄：${item.user.age}岁`;
        }
      } else if (item.user.age && item.user.age !== '未知') {
        userInfoStr += `\n年龄：${item.user.age}岁`;
      }
      
      userInfoStr += `\n工作：${item.user.job}`;
    }
    
    wx.showModal({
      title: '分解详情',
      content: `原数：${item.number}\n\n因子：${(item.factors || []).join(', ')}\n\n分解式：${item.formula || (item.factors || []).join(' × ')}\n\n时间：${item.create_time || ''}\n耗时：${item.elapsed_time || 0}秒${userInfoStr}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 清空历史
  async clearHistory() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有历史记录吗？此操作不可恢复。',
      success: async (res) => {
        if (res.confirm) {
          try {
            const resp = await requestApi({
              url: '/api/history/clear',
              method: 'POST',
              showLoading: true
            });

            if (!resp || typeof resp !== 'object' || !resp.success) {
              showError(resp?.message || '清空历史失败');
              return;
            }

            this.loadHistory();
            this.loadStats();
            wx.showToast({
              title: '已清空',
              icon: 'success'
            });
          } catch (error) {
            console.error('清空历史记录异常:', error);
            showError(error.message || '清空历史失败');
          }
        }
      }
    });
  }
});

