# 管理员功能设置说明

## 1. 初始化管理员账号

运行以下命令初始化管理员账号：

```bash
cd backend
python init_admin.py
```

管理员账号信息：
- **手机号**: 180162226658
- **密码**: zy6658
- **用户类型**: 管理员 (UserType=1)

## 2. 功能说明

### 用户信息页面 (`/subpackages/user/pages/UserInfo/UserInfo`)
- **普通用户**: 只能查看自己的信息
- **管理员**: 可以查看所有用户信息和访问数据可视化界面

### 管理员可视化界面 (`/subpackages/user/pages/AdminVisualization/AdminVisualization`)
- **仅管理员可访问**
- 包含4个图表：
  1. **日期-降噪次数** (折线图)
  2. **周次-降噪次数** (饼图)
  3. **一天中时间-降噪次数** (折线图)
  4. **活跃用户-降噪次数** (柱状图)

## 3. 权限控制

- **UserType = 1**: 管理员，可以查看所有用户信息和数据可视化
- **UserType = 2**: 普通用户，只能查看自己的信息
- **UserType = 3**: 游客，只能查看自己的信息

## 4. API接口

### `/api/getStatistics` (POST)
- **功能**: 获取降噪数据统计
- **权限**: 仅管理员
- **返回**: 
  ```json
  {
    "success": true,
    "data": {
      "dateData": [{"date": "2024-01-01", "count": 10}, ...],
      "weekData": [{"week": "周一", "count": 5}, ...],
      "timeData": [{"hour": 0, "count": 2}, ...],
      "userData": [{"userName": "用户1", "userId": "13800138000", "count": 20}, ...]
    }
  }
  ```

## 5. 页面访问

在首页或其他页面添加跳转到用户信息页面的按钮：

```javascript
wx.navigateTo({
  url: '/subpackages/user/pages/UserInfo/UserInfo'
})
```

