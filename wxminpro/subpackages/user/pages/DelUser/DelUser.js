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
    DeliconStatu: false,
    DelList:[] ,
    Delarr:[] ,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this ;
    // 加载 Mysql 的users中的注册用户，到 list 列表中
    post('/api/DispUser', {
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
      
      if (res === "1") {
        console.log("注册表 users 为空！")
        console.log(that.data.list)
      } else if (res === "2") {
        console.log("读取 users 失败！")
        console.log(that.data.list)
      } else if (res !== "2" && res !== "1") {
        console.log("注册表 users 非空！！！")
        console.log(that.data.list)
        that.setData({
          list: Array.isArray(res) ? res : [],    // 将后端返回的注册用户表（users）信息保存到 list 中  ，实现同步
        })
      }
    }).catch(err => {
      console.error("加载用户列表失败：", err)
      // 错误已在 request.js 中处理
    })


        ////////////////////////////////////////
        // fail: err => {
        //   if (errorCallback){
        //     errorCallback(err);
        //   }else{
        //     wx.showToast({
        //       title: '读取用户注册表失败！',
        //       icon: 'none',
        //       duration: 1500,
        //       mask: false
        //     })
        //   }
        // },
        // complete: () => {
        //   if (completeCallback) {
        //     completeCallback();
        //   }
        // }
      

        //////////////////////////////////////////// 
    
    let dataList = this.data.list;
    dataList.map(function (value) {
      value.selStatu = false;
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
      this.data.list[myid].UserType = 4
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
EditUserIcon() {
  this.setData({
    DeliconStatu: !this.data.DeliconStatu
  })
},


  //显示选中图标
   showSelIcon() {
     this.setData({
       iconStatu: !this.data.iconStatu
     })
   },

   // 删除用户 ：实现 小程序前端列表删除 和 MySQL 后端 Users 注册表同步删除
   delItem() {
     var that = this ;
     let arr = this.data.list;        // 去除要删除的数据后的数据，开始为原始数据（没有删除）
     let arr0 = this.data.list;       // 保存原始记录
     let selArr = this.data.selList;  // 用户选择要删除的 id号 
    
     //  去除要删除的数据后的数据 
     for (let i = 0; i < selArr.length; i++) {
       arr = arr.filter((value,index) => {
         return value.id != selArr[i]
       })
     }
    
    //  要删除的数据 Delarr 计算 二个列表（数组）的差 
      var set1 = new Set(arr0);
      var set2 = new Set(arr);  
      var diff = [...arr0.filter(x => !set2.has(x)), ...arr.filter(x => !set1.has(x))];
      
     // 计算要删除的用户的 手机号码
     let DelPhone = []
     for (let i = 0; i < diff.length; i++) {
         DelPhone.push(diff[i].Phone)         //将要删除的人的手机号 压入： DelPhone
      }
    
      console.log(DelPhone )

     this.setData({
        Delarr:DelPhone,   //要删除的 用户的手机号 保存在 Delarr中
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
     post(apiConfig.endpoints.delUser, {
        DelList: that.data.Delarr,    //DelList 要删除的 手机号列表
      }, {
        showLoading: true,
        loadingText: '删除中...',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }
      }).then(res => {
        console.log("删除成功")
        wx.showToast({
          title: '删除成功',
          icon: 'success'
        })
      }).catch(err => {
        console.error("删除失败：", err)
        // 错误已在 request.js 中处理
      }) 
        // 重新加载一次数据
        // this.onLoad();  
     }, //delItem

 })  //Page({
 
