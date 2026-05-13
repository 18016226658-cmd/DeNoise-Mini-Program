const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

Page({
  /**
   * 页面的初始数据
   */
  data: {
    // list 为当前用户列表 ，通过onLoad() ，从后台 Mysql的 users中读取 数据
    list: [
      // { "id": 0, "Phone": "13812345678", "statu": true, "UserName": "Sumeng", "Password": "123456" , "Gender": "男", "Birthday": "1964-09-04" , "RegisterTime": "2024-02-22 18:48:39"},
      //  { "id": 1, "Phone": "13333333333", "statu": false, "UserName": "Lisi",  "Password": "123456" , "Gender": "女", "Birthday": "1999-09-09", "RegisterTime": "2024-02-22 19:12:36"},
      //   { "id": 2, "Phone": "18051094982", "statu": true, "UserName": "苏梦",  "Password": "123456" , "Gender": "女", "Birthday": "1999-09-09", "RegisterTime": "2024-02-22 19:15:51"},
      //   { "id": 3, "Phone": "13999999999", "statu": true, "UserName": "139",  "Password": "123456" , "Gender": "女", "Birthday": "2020-10-11", "RegisterTime": "2024-02-23 21:04:15"},
        // { "id": 4, "Phone": "18051096769", "statu": false, "UserName": "杨洁",  "Password": "123456", "Gender": "女" , "Birthday": "2020-10-10", "RegisterTime": "2024-02-23 22:08:51"},
        // { "id": 5, "Phone": "13999999998", "statu": true, "UserName": "小明",  "Password": "123456" , "Gender": "男", "Birthday": "2010-10-11", "RegisterTime": "2024-02-26 12:11:37"},
        // { "id": 6, "Phone": "13555555555", "statu": true, "UserName": "13555", "Password": "123456" , "Gender": "男", "Birthday": "2020-10-10", "RegisterTime": "2024-03-05 20:11:19"},
        ] ,
    selColor: '#999',
    selList: [],
    iconStatu: false,
    // DeliconStatu: false,
    // DelList:[] ,
    UserTypeList:[],  //存放 UserType
    UserIDList:[],    //存放 UserID
    // Delarr:[] ,
    UserTypeArr:[] ,
    UserIDArr:[] ,
    UserType: 2 ,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this ;
    // 加载 Mysql 的users中的注册用户，到 list 列表中
    post(apiConfig.endpoints.dispUser, {
      //  无数据要传递给 后端 DispUser
    }, {
      showLoading: true,
      loadingText: '加载中...',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      }
    }).then(res => {
      console.log(" ====== 后端返回的注册用户表（users） 信息- （res）========")
      console.log(res) 
      // console.log(res.data.length)  
      
      if (res.data == "1") {
        console.log("注册表 users 为空！")
        console.log(that.data.list)
      } else if (res.data == "2") {
        console.log("读取 users 失败！")
        console.log(that.data.list)
      } else {
        console.log("注册表 users 非空！！！")
        console.log(that.data.list)
        that.setData({
          list: res.data,    // 将后端返回的注册用户表（users）信息保存到 list 中  ，实现同步
        })

        // 初始化 selStatu 为 false
        var dataList = that.data.list;
        dataList.map(function (value) {
          value.selStatu = false;
        })
        that.setData({
          list: dataList
        })
      }
    }).catch(err => {
      console.error("加载用户列表失败：", err)
      // 错误已在 request.js 中处理
    })
  },

  //编辑用户等级
  EditUserType(e){
    var that = this ;
    console.log(e)
    if (this.data.iconStatu){
      console.log("EditUserType---1")
      console.log(e.currentTarget.dataset)
      console.log(e.currentTarget.dataset.id)
      let myid = e.currentTarget.dataset.id
      console.log(this.data.list[myid])
      console.log(this.data.list[myid].UserType)
      this.data.list[myid].UserType = this.data.UserType
      this.setData({
        // list[myid].UserType :3 ,
      })
         
    }
        
  },



  // 选中要删除的用户
  toggleSel(e) {
    if (this.data.iconStatu) {
      let selArr = this.data.selList;
      let selId = e.target.dataset.id || e.currentTarget.dataset.id;
      let dataList = this.data.list;
      let index = this.data.selList.indexOf(selId);
      if (index < 0) {
        selArr.push(e.target.dataset.id);
        dataList.map((value) => {
          if (value.id == selId) {
            value.selStatu = true
           }
        })
      } else {
        dataList.map((value) => {
          if (value.id == selId) {
            value.selStatu = false
          }
        })
        selArr.splice(index, 1)
      }
      this.setData({
        selList: selArr,
        list: dataList
      })
    }
  },

//显示选中图标
// EditUserIcon() {
//   this.setData({
//     DeliconStatu: !this.data.DeliconStatu
//   })
// },

// 输入用户等级,根据这个数值，点击那个用户，那个用户的等级类型就修改为 对应的数值
UserTypeInput(e){
  console.log("============================ e ============================")
  console.log(e.detail.value)
  this.setData({
    UserType:e.detail.value ,

  })
  console.log(this.data.UserType)


},
  //显示选中图标
   showSelIcon() {
     console.log("显示选中图标")
     this.setData({
       iconStatu: !this.data.iconStatu
     })
   },

   // 保存修改后的用户类型 ：根据小程序前端列表数据 更新 MySQL 后端 Users 注册表中的 UserType
   SaveUserType() {
     var that = this ;
     let arr = this.data.list;        // 去除要删除的数据后的数据，开始为原始数据（没有删除）
     let arr0 = this.data.list;       // 保存原始记录
    //  let selArr = this.data.selList;  // 用户选择要删除的 id号 
    
     //  去除要删除的数据后的数据 
    //  for (let i = 0; i < selArr.length; i++) {
    //    arr = arr.filter((value,index) => {
    //      return value.id != selArr[i]
    //    })
    //  }
    
    //  要删除的数据 Delarr 计算 二个列表（数组）的差 
      // var set1 = new Set(arr0);
      // var set2 = new Set(arr);  
      // var diff = [...arr0.filter(x => !set2.has(x)), ...arr.filter(x => !set1.has(x))];
      
     // 计算要更新的用户的 UserType
     let NewUserType = []
     let NewUserID = []
     for (let i = 0; i < arr.length; i++) {
      NewUserType.push(arr[i].UserType)         //将要删除的人的手机号 压入：NewUserType
      NewUserID.push(arr[i].UserID)         //将要删除的人的手机号 压入： NewUserID
      }
    

      console.log(NewUserType )
      console.log(NewUserID )

     this.setData({
      UserTypeArr:NewUserType,   //要更新的 用户的类型 保存在 UserTypeArr中
      UserIDArr:NewUserID,   //要更新的 用户的类型 保存在 UserTypeArr中
     })

     // 修改选择字体标记 为  false
     for (let i = 0; i < arr.length; i++) {
       arr[i].selStatu = false
     }
     this.setData({
       list: arr,
       selList: [],
     })


     //执行数据库中注册用户表（users）同步删除
     post(apiConfig.endpoints.saveUserType, {
        UserTypeList: that.data.UserTypeArr,    //UserTypeList 要更新的 用户类型列表 UserType
        UserIDList: that.data.UserIDArr,       //UserIDList 所有用户 UserID 列表
      }, {
        showLoading: true,
        loadingText: '保存中...',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }
      }).then(res => {
        console.log("更新成功")
        wx.showToast({
          title: '更新成功',
          icon: 'success'
        })
      }).catch(err => {
        console.error("更新失败：", err)
        // 错误已在 request.js 中处理
      }) 
        // 重新加载一次数据
        // this.onLoad();  
     }, //delItem

 })  //Page({
 


