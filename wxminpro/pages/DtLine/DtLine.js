
const app = getApp()
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')
// import { CubeShapeSchema } from 'XrFrame/components';
import * as echarts from '../../ec-canvas/echarts';// 引入图表
import wordCloud from   "../../echarts-wordcloud/wordCloud";
var option=[];//图表配置项 声明
// 初始化图表函数  开始
let chart2 = null; 
function initChart2(canvas, width, height, dpr) {
  chart2 = echarts.init(canvas, null, {
    width: width,
    height: height,
    devicePixelRatio: dpr
  })
  canvas.setChart(chart2)
  return chart2;
}

wordCloud({
  createCanvas: function () {
    return wx.createOffscreenCanvas({
      type: "2d",
    });
  },
});

// 初始化图表函数  结束
Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    index:0,
    ec2: {
      onInit: initChart2
    },
    histogramData1:[],
    histogramData2:[],
    histogramData3:[],
    arr22:[],
    datas22:[],
    Pie2:[],
    Date_Data1:[],
    Date_Data2:[],
    Week_Data1:[],
    Week_Data2:[],
    Hour_Data1:[],
    Hour_Data2:[],
    Xb_Data1:[],
    Xb_Data2:[],
    NL_Data1:[],
    NL_Data2:[],
    Pie_Data3:[],
    QG_Data1:[],
    QG_Data2:[],
    WC1:{},
    WC2:{},
    WC3:{},
   
    TDate_Data1:[],
    TDate_Data2:[],
    TWeek_Data1:[],
    TWeek_Data2:[],
    THour_Data1:[],
    THour_Data2:[],
    TXb_Data1:[],
    TXb_Data2:[],
    TNL_Data1:[],
    TNL_Data2:[],
    TPie_Data3:[],

    TQG_Data1:[],
    TQG_Data2:[],
    TWC1:{},
    TWC2:{},
    TWC3:{},

    // 用户注册信息
    UserID : 1001 ,
    UserName : '王小明',
    Gender : '男',
    Birthday : '2001-10-11',
    FaceImg:'/static/image/header.png',
    UserType:2 ,  // 注册用户类型  1：管理员   2：Vip用户   3：普通用户
    
  },

// 词云图
myWordCloud(){
  console.log("聊天记录词云图分析（WordCloud)")
  var keywords =this.data.WC1;   //通过进入页面，执行fun()从后台Python读取数据返回的聊天问题数据集合
  // 常量定义，用于测试
  // var keywords = {
  //   visualMap: 22199,
  //   continuous: 10288,
  //   contoller: 620,
  //   series: 274470,
  //   gauge: 12311,
  //   detail: 1206,
  //   piecewise: 4885,
  //   textStyle: 32294,
  //   markPoint: 18574,
  //   pie: 38929,
  //   roseType: 969,
  //   label: 37517,
  //   emphasis: 12053,
  //   yAxis: 57299,
  //   name: 15418,
  //   type: 22905,
  //   gridIndex: 5146,
  //   normal: 49487,
  //   itemStyle: 33837,
  //   min: 4500,
  //   silent: 5744,
  //   animation: 4840,
  //   offsetCenter: 232,
  //   inverse: 3706,
  //   borderColor: 4812,
  //   markLine: 16578,
  //   line: 76970,
  //   radiusAxis: 6704,
  //   radar: 15964,
  //   data: 60679,
  //   dataZoom: 24347,
  //   tooltip: 43420,
  //   toolbox: 25222,
  //   geo: 16904,
  //   parallelAxis: 4029,
  //   parallel: 5319,
  //   max: 3393,
  //   bar: 43066,
  //   heatmap: 3110,
  //   map: 20285,
  //   animationDuration: 3425,
  //   animationDelay: 2431,
  //   splitNumber: 5175,
  //   axisLine: 12738,
  //   lineStyle: 19601,
  //   splitLine: 7133,
  //   axisTick: 8831,
  //   axisLabel: 17516,
  //   pointer: 590,
  //   color: 23426,
  //   title: 38497,
  //   formatter: 15214,
  //   slider: 7236,
  //   legend: 66514,
  //   grid: 28516,
  //   smooth: 1295,
  //   smoothMonotone: 696,
  //   sampling: 757,
  //   feature: 12815,
  //   saveAsImage: 2616,
  //   polar: 6279,
  //   calculable: 879,
  //   backgroundColor: 9419,
  //   excludeComponents: 130,
  //   show: 20620,
  //   text: 2592,
  //   icon: 2782,
  //   dimension: 478,
  //   inRange: 1060,
  //   animationEasing: 2983,
  //   animationDurationUpdate: 2259,
  //   animationDelayUpdate: 2236,
  //   animationEasingUpdate: 2213,
  //   xAxis: 89459,
  //   angleAxis: 5469,
  //   showTitle: 484,
  //   dataView: 2754,
  //   restore: 932,
  //   timeline: 10104,
  //   range: 477,
  //   value: 5732,
  //   precision: 878,
  //   target: 1433,
  //   zlevel: 5361,
  //   symbol: 8718,
  //   interval: 7964,
  //   symbolSize: 5300,
  //   showSymbol: 1247,
  //   inside: 8913,
  //   xAxisIndex: 3843,
  //   orient: 4205,
  //   boundaryGap: 5073,
  //   nameGap: 4896,
  //   zoomLock: 571,
  //   hoverAnimation: 2307,
  //   legendHoverLink: 3553,
  //   stack: 2907,
  //   throttle: 466,
  //   connectNulls: 897,
  //   clipOverflow: 826,
  //   startValue: 551,
  //   minInterval: 3292,
  //   opacity: 3097,
  //   splitArea: 4775,
  //   filterMode: 635,
  //   end: 409,
  //   left: 6475,
  //   funnel: 2238,
  //   lines: 6403,
  //   baseline: 431,
  //   align: 2608,
  //   coord: 897,
  //   nameTextStyle: 7477,
  //   width: 4338,
  //   shadowBlur: 4493,
  //   effect: 929,
  //   period: 225,
  //   areaColor: 631,
  //   borderWidth: 3654,
  //   nameLocation: 4418,
  //   position: 11723,
  //   containLabel: 1701,
  //   scatter: 10718,
  //   areaStyle: 5310,
  //   scale: 3859,
  //   pieces: 414,
  //   categories: 1000,
  //   selectedMode: 3825,
  //   itemSymbol: 273,
  //   effectScatter: 7147,
  //   fontStyle: 3376,
  //   fontSize: 3386,
  //   margin: 1034,
  //   iconStyle: 2257,
  //   link: 1366,
  //   axisPointer: 5245,
  //   showDelay: 896,
  //   graph: 22194,
  //   subtext: 1442,
  //   selected: 2881,
  //   barCategoryGap: 827,
  //   barGap: 1094,
  //   barWidth: 1521,
  //   coordinateSystem: 3622,
  //   barBorderRadius: 284,
  //   z: 4014,
  //   polarIndex: 1456,
  //   shadowOffsetX: 3046,
  //   shadowColor: 3771,
  //   shadowOffsetY: 2475,
  //   height: 1988,
  //   barMinHeight: 575,
  //   lang: 131,
  //   symbolRotate: 2752,
  //   symbolOffset: 2549,
  //   showAllSymbol: 942,
  //   transitionDuration: 993,
  //   bottom: 3724,
  //   fillerColor: 229,
  //   nameMap: 1249,
  //   barMaxWidth: 747,
  //   radius: 2103,
  //   center: 2425,
  //   magicType: 3276,
  //   labelPrecision: 248,
  //   option: 654,
  //   seriesIndex: 935,
  //   controlPosition: 121,
  //   itemGap: 3188,
  //   padding: 3481,
  //   shadowStyle: 347,
  //   boxplot: 1394,
  //   labelFormatter: 264,
  //   realtime: 631,
  //   dataBackgroundColor: 239,
  //   showDetail: 247,
  //   showDataShadow: 217,
  //   x: 684,
  //   valueDim: 499,
  //   onZero: 931,
  //   right: 3255,
  //   clockwise: 1035,
  //   itemWidth: 1732,
  //   trigger: 3840,
  //   axis: 379,
  //   selectedOffset: 670,
  //   startAngle: 1293,
  //   minAngle: 590,
  //   top: 4637,
  //   avoidLabelOverlap: 870,
  //   labelLine: 3785,
  //   sankey: 2933,
  //   endAngle: 213,
  //   start: 779,
  //   roam: 1738,
  //   fontWeight: 2828,
  //   fontFamily: 2490,
  //   subtextStyle: 2066,
  //   indicator: 853,
  //   sublink: 708,
  //   zoom: 1038,
  //   subtarget: 659,
  //   length: 1060,
  //   itemSize: 505,
  //   controlStyle: 452,
  //   yAxisIndex: 2529,
  //   edgeLabel: 1188,
  //   radiusAxisIndex: 354,
  //   scaleLimit: 1313,
  //   geoIndex: 535,
  //   regions: 1892,
  //   itemHeight: 1290,
  //   nodes: 644,
  //   candlestick: 3166,
  //   crossStyle: 466,
  //   edges: 369,
  //   links: 3277,
  //   layout: 846,
  //   barBorderColor: 721,
  //   barBorderWidth: 498,
  //   treemap: 3865,
  //   y: 367,
  //   valueIndex: 704,
  //   showLegendSymbol: 482,
  //   mapValueCalculation: 492,
  //   optionToContent: 264,
  //   handleColor: 187,
  //   handleSize: 271,
  //   showContent: 1853,
  //   angleAxisIndex: 406,
  //   endValue: 327,
  //   triggerOn: 1720,
  //   contentToOption: 169,
  //   buttonColor: 71,
  //   rotate: 1144,
  //   hoverLink: 335,
  //   outOfRange: 491,
  //   textareaColor: 58,
  //   textareaBorderColor: 58,
  //   textColor: 60,
  //   buttonTextColor: 66,
  //   category: 336,
  //   hideDelay: 786,
  //   alwaysShowContent: 1267,
  //   extraCssText: 901,
  //   effectType: 277,
  //   force: 1820,
  //   rippleEffect: 723,
  //   edgeSymbolSize: 329,
  //   showEffectOn: 271,
  //   gravity: 199,
  //   edgeLength: 193,
  //   layoutAnimation: 152,
  //   length2: 169,
  //   enterable: 957,
  //   dim: 83,
  //   readOnly: 143,
  //   levels: 444,
  //   textGap: 256,
  //   pixelRatio: 84,
  //   nodeScaleRatio: 232,
  //   draggable: 249,
  //   brushType: 158,
  //   radarIndex: 152,
  //   large: 182,
  //   edgeSymbol: 675,
  //   largeThreshold: 132,
  //   leafDepth: 73,
  //   childrenVisibleMin: 73,
  //   minSize: 35,
  //   maxSize: 35,
  //   sort: 90,
  //   funnelAlign: 61,
  //   source: 336,
  //   nodeClick: 200,
  //   curveness: 350,
  //   areaSelectStyle: 104,
  //   parallelIndex: 52,
  //   initLayout: 359,
  //   trailLength: 116,
  //   boxWidth: 20,
  //   back: 53,
  //   rewind: 110,
  //   zoomToNodeRatio: 80,
  //   squareRatio: 60,
  //   parallelAxisDefault: 358,
  //   checkpointStyle: 440,
  //   nodeWidth: 49,
  //   color0: 62,
  //   layoutIterations: 56,
  //   nodeGap: 54,
  //   "color(Array": 76,
  //   "<string>)": 76,
  //   repulsion: 276,
  //   tiled: 105,
  //   currentIndex: 145,
  //   axisType: 227,
  //   loop: 97,
  //   playInterval: 112,
  //   borderColor0: 23,
  //   gap: 43,
  //   autoPlay: 123,
  //   showPlayBtn: 25,
  //   breadcrumb: 119,
  //   colorMappingBy: 85,
  //   id: 18,
  //   blurSize: 85,
  //   minOpacity: 50,
  //   maxOpacity: 54,
  //   prevIcon: 12,
  //   children: 21,
  //   shape: 98,
  //   nextIcon: 12,
  //   showNextBtn: 17,
  //   stopIcon: 21,
  //   visibleMin: 83,
  //   visualDimension: 97,
  //   colorSaturation: 56,
  //   colorAlpha: 66,
  //   emptyItemWidth: 10,
  //   inactiveOpacity: 4,
  //   activeOpacity: 4,
  //   showPrevBtn: 19,
  //   playIcon: 26,
  //   ellipsis: 19,
  //   gapWidth: 19,
  //   borderColorSaturation: 10,
  //   handleIcon: 2,
  //   handleStyle: 6,
  //   borderType: 1,
  //   constantSpeed: 1,
  //   polyline: 2,
  //   blendMode: 1,
  //   dataBackground: 1,
  //   textAlign: 1,
  //   textBaseline: 1,
  //   brush: 3,
  // };

  var data = [];
  for (var name in keywords) {
    data.push({
      name: name,
      // value: Math.sqrt(keywords[name]),
      value: keywords[name],
    });
   
  }

/////////////////////////////////////////////////////

  const option = {
    series: [{
      type: 'wordCloud',
      sizeRange: [4, 150],
        // sizeRange: [12, 50],
     
      gridSize: 0,
      // gridSize: 20,
    
       // rotationRange: [0, 0],
      rotationRange: [-45, 0, 45, 90],
      // shape: 'circle',
      shape: "pentagon",  //五角大楼
      maskImageUrl: "/pages/DtLine/logo.png",     //用某个图形状展示词云图
      width: '100%',
      height: '100%',
      drawOutOfBound: false,
      // wait: 500,
      keepAspect: true,
      textStyle: {
        fontWeight: "bold",
        color: function () {
          return (
            "rgb(" +
            [
              Math.round(Math.random() * 200) + 50,
              Math.round(Math.random() * 50),
              Math.round(Math.random() * 50) + 50,
            ].join(",") +
            ")"
          );
        },
      },
      emphasis: {
        textStyle: {
          color: "#528",
        },
      },

      // data: data,
      data: data.sort(function (a, b) {
        return b.value - a.value;      // 根据 data.value 降序
        // return a.value - b.value;   // 根据 data.value 升序
      }),

    
  }]
}

  chart2.setOption(option,true);
  this.setData({
    index:7,
})
},
//////////////////////////////////////

  // 饼状图 点击事件
  pie(){
        console.log("聊天数量按照星期分布情况（pie)")
        option = {
          title: {
            text: '聊天数量按星期分布',
            left: 'center',
          },
          tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b} : {c}\n {d}%",
          },
          legend: {
            top: '85%',
            left: 'center',
            // orient: 'vertical',  //垂直
          },
          series: [
            {
              name: '收益明细',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                normal: {
                  show:true,
                  formatter: '{d}%' , // b=名称 c=数值 d=百分比 \n换行 
                  fontSize:10,
                  
                },
                show: false,
                // position: 'center' ,
                position: 'inner',
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '40',
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              // data:this.data.histogramData3,
              data:this.data.Pie_Data3,
            }
          ]
        };
      chart2.setOption(option,true);
      this.setData({
      index:6,
    }) 
  },
   

  // 折线图 点击事件 聊天数量按照日期分布情况（line)
  lineA(){
    console.log(" 聊天数量按照日期分布情况（line1)")
     option = {
      title: {
        text: '聊天数量按日期分布',
        left: 'center',
      },
      xAxis: {
        type: 'category',
        data: this.data.Date_Data1,
        name:'日期',//坐标轴名称
        nameLocation:'center',//坐标轴名称显示位置,可选start, middle/center,end
        nameTextStyle:{},//坐标轴名称的文字样式
        nameGap:30, //坐标轴名称与轴线之间的距离
      },
      yAxis: {
        type: 'value'
      },
      series: [
       
        {
          label: { //数据显示
            show: true,
            color:'inherit',
      position:'top',
            fontSize: 10,
          },
          data: this.data.Date_Data2,
          type: 'line'
        }
      ]
    }
    chart2.setOption(option,true);
        this.setData({
      index:1,
    })
      },

  // 折线图 点击事件  聊天聊天情感分析 （line)
  lineB(){
    console.log(" 聊天情感分析（line2)")
    option = {
      title: {
        text: '聊天情感分析',
        left: 'center',
      },
     xAxis: {
       type: 'category',
       data: this.data.QG_Data1,
       name:'聊天序号',//坐标轴名称
       nameLocation:'center',//坐标轴名称显示位置,可选start, middle/center,end
       nameTextStyle:{},//坐标轴名称的文字样式
       nameGap:30, //坐标轴名称与轴线之间的距离
     },
     yAxis: {
       type: 'value'
     },
     series: [
      
       {
         label: { //数据显示
           show: true,
           color:'inherit',
          position:'top',
           fontSize: 10,
         },
         data: this.data.QG_Data2,
         type: 'line'
       }
     ]
   }
   chart2.setOption(option,true);
       this.setData({
     index:2,
   })
     },

// 折线图 点击事件  聊天数量按照一天里的时间点分布情况  （line)
lineC(){
  console.log("  聊天数量按照一天里的时间点分布情况（line3)")
  option = {
    title: {
      text: '聊天数量按时间点分布',
      left: 'center',
    },
   xAxis: {
     type: 'category',
     data: this.data.Hour_Data1,
     name:'小时',//坐标轴名称
     nameLocation:'center',//坐标轴名称显示位置,可选start, middle/center,end
     nameTextStyle:{},//坐标轴名称的文字样式
     nameGap:30, //坐标轴名称与轴线之间的距离
    //  axisLine:{ 
    //     symbol:['none', 'arrow'], //默认 'none'。两端显示 'arrow'，末端显示 ['none', 'arrow']
    //     } ,
   },
   yAxis: {
     type: 'value',
     name:'次数',//坐标轴名称
   },
   series: [
    
     {
       label: { //数据显示
         show: true,
         color:'inherit',
   position:'top',
         fontSize: 10,
       },
       data: this.data.Hour_Data2,
       type: 'line'
     }
   ]
 }
 chart2.setOption(option,true);
     this.setData({
   index:3,
 })
   },


  // 柱状图 点击事件 聊天数量按照性别点分布情况 (bar)
  barA(){
    console.log("聊天数量按照性别分布情况（bar1)")
    option = {
      title: {
        text: '聊天数量按性别分布',
        left: 'center',
      },
      xAxis: {
        type: 'category',
        data:this.data.Xb_Data1,
        name:'性别',//坐标轴名称
        nameLocation:'center',//坐标轴名称显示位置,可选start, middle/center,end
        nameTextStyle:{},//坐标轴名称的文字样式
        nameGap:30, //坐标轴名称与轴线之间的距离
      },
      yAxis: {
        type: 'value'
      },
      
      series: [{
        label: { //数据显示
          show: true,
          color:'inherit',
    position:'top',
          fontSize: 10,
        },

        data: this.data.Xb_Data2,
        type: 'bar',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(180, 180, 180, 0.2)'
        }
      },
    ]
    }
    chart2.setOption(option,true);
      this.setData({
        index:4,
   })

  },

   // 柱状图 点击事件 聊天数量按照年龄分布情况 (bar)
   barB(){
    console.log("聊天数量按照年龄分布情况（bar2)")
    option = {
      title: {
        text: '聊天数量按年龄分布',
        left: 'center',
      },
      xAxis: {
        type: 'category',
        data:this.data.NL_Data1,
        name:'年龄（岁）',//坐标轴名称
        nameLocation:'center',//坐标轴名称显示位置,可选start, middle/center,end
        nameTextStyle:{},//坐标轴名称的文字样式
        nameGap:30, //坐标轴名称与轴线之间的距离
      },
      yAxis: {
        type: 'value'
      },
      
      series: [{
        label: { //数据显示
          show: true,
          color:'inherit',
    position:'top',
          fontSize: 10,
        },

        data: this.data.NL_Data2,
        type: 'bar',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(180, 180, 180, 0.2)'
        }
      },
    ]
    }
    chart2.setOption(option,true);
      this.setData({
        index:5,
   })

  },

//日报 数据获取  函数
fun(){
  let that=this;
  
  post(apiConfig.endpoints.dtVisual, {}, {
    showLoading: true,
    loadingText: '加载数据中...',
    timeout: 5000
  }).then(res => {
    if (res) {
      that.setData({
        Date_Data1: res.user_Data11 || [],
        Date_Data2: res.user_Data12 || [],
        Week_Data1: res.user_Data21 || [],
        Week_Data2: res.user_Data22 || [],
        Hour_Data1: res.user_Data31 || [],
        Hour_Data2: res.user_Data32 || [],
        Xb_Data1: res.user_Data41 || [],
        Xb_Data2: res.user_Data42 || [],
        NL_Data1: res.user_Data51 || [],
        NL_Data2: res.user_Data52 || [],
        Pie_Data3: res.user_Data53 || [],
        QG_Data1: res.user_Data61 || [],
        QG_Data2: res.user_Data62 || [],
        WC1: res.user_WC1 || {},         //从后端实际获取 聊天问题词云图词典数据
        //测试用常量定义的聊天问题词云图词典数据

        // WC1: {                     
        //   visualMap: 22199,
        //   continuous: 10288,
        //   contoller: 620,
        //   series: 274470,
        //   gauge: 12311,
        //   detail: 1206,
        //   piecewise: 4885,
        //   textStyle: 32294,
        //   markPoint: 18574,
        //   pie: 38929,
        //   roseType: 969,
        //   label: 37517,
        //   emphasis: 12053,
        //   yAxis: 57299,
        //   name: 15418,
        //   type: 22905,
        //   gridIndex: 5146,
        //   normal: 49487,
        //   itemStyle: 33837,
        //   min: 4500,
        //   silent: 5744,
        //   animation: 4840,
        //   offsetCenter: 232,
        //   inverse: 3706,
        //   borderColor: 4812,
        //   markLine: 16578,
        //   line: 76970,
        //   radiusAxis: 6704,
        //   radar: 15964,
        //   data: 60679,
        //   dataZoom: 24347,
        //   tooltip: 43420,
        //   toolbox: 25222,
        //   geo: 16904,
        //   parallelAxis: 4029,
        //   parallel: 5319,
        //   max: 3393,
        //   bar: 43066,
        //   heatmap: 3110,         
        // },
      })


      console.log("============== arr2 datas2 Pie ==================")
      console.log(that.data.TDate_Data1)
      console.log(that.data.TDate_Data2)
      console.log(that.data.TWeek_Data1)
      console.log(that.data.TWeek_Data2)
      console.log(that.data.THour_Data1)
      console.log(that.data.THour_Data2)
      console.log(that.data.TXb_Data1)
      console.log(that.data.TXb_Data2)
      console.log(that.data.TNL_Data1)
      console.log(that.data.TNL_Data2)
      console.log(that.data.TPie_Data3)
      console.log(that.data.TQG_Data1)
      console.log(that.data.TQG_Data2)

      //  X轴数据
      let arr11 = res.user_Data11;   //Date
      let arr21 = res.user_Data21;   //Week
      let arr31 = res.user_Data31;   //Hour
      let arr41 = res.user_Data41;   //Xb
      let arr51 = res.user_Data51;   //NL
      let arr61 = res.user_Data61;   //NL

      // Y轴数据
      let datas12 = res.user_Data12;  
      let datas22 = res.user_Data22; 
      let datas32 = res.user_Data32; 
      let datas42 = res.user_Data42; 
      let datas52 = res.user_Data52; 
      let datas62 = res.user_Data62; 

      //   饼图数据
      let Pie = res.user_Data53; 
      //   词云图数据
      // let  WC1 =  res.data.user_Data62; 
      // let  WC1 =  res.data.user_Data72; 

    // 显示Echarts图表类型信息，可以去Echarts官网复制粘贴
    //  默认输出 line1 图的配置项

      option = {
        xAxis: {
          type: 'category',
          // data: this.data.Date_Data1,
          data: res.user_Data11,
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            label: { //数据显示
              show: true,
              color:'inherit',
              position:'top',
              fontSize: 10,
            },
            data: res.user_Data12,
            type: 'line'
          }
        ]
      }
      
      // 输出到页面
      chart2.setOption(option);
      // 数据获取 结束
      that.setData({
        Date_Data1: arr11,
        Date_Data2: datas12,
        Week_Data1: arr21,
        Week_Data2: datas22,
        Hour_Data1: arr31,
        Hour_Data2: datas32,
        Xb_Data1: arr41,
        Xb_Data2: datas42,
        NL_Data1: arr51,
        NL_Data2: datas52,
        Pie_Data3: Pie,
        QG_Data1: arr61,
        QG_Data2: datas62,
      })
    }  // 关闭 if (res) 块
  }).catch(err => {
    console.error('请求失败：', err)
    // 错误已在 request.js 中处理
  })
},
  /**
   * 生命周期函数--监听页面加载
   */
  // onLoad(options) {

  // },

  onLoad() {
      console.log("==============userInfo==========  1111 ")   
      // const app=getApp()
      const userInfo = app.globalData.userInfo
      
      // 如果用户未登录，使用默认值
      if (!userInfo) {
        console.log('用户未登录，使用默认用户信息')
        this.setData({
          userInfo: {},
          UserName: this.data.UserName || '王小明',
          UserID: this.data.UserID || 1001,
          Gender: this.data.Gender || '男',
          Birthday: this.data.Birthday || '2001-10-11',
          FaceImg: this.data.FaceImg || '/static/image/header.png',
          UserType: this.data.UserType || 2
        })
        return
      }
      
      // 用户已登录，使用实际用户信息
      this.setData({
        userInfo: userInfo,
        UserName: userInfo.UserName || userInfo.nickName || this.data.UserName || '王小明',
        Gender: userInfo.Gender || this.data.Gender || '男',
        Birthday: userInfo.Birthday || this.data.Birthday || '2001-10-11',
        UserID: userInfo.Phone || userInfo.UserID || this.data.UserID || 1001,
        FaceImg: userInfo.FaceImg || this.data.FaceImg || '/static/image/header.png',
        UserType: userInfo.UserType || this.data.UserType || 2
      })
      console.log("==============userInfo========== 22222")   
      console.log(this.data.userInfo)  
      console.log(this.data.UserType)  
  },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    this.echartsComponet = this.selectComponent('#echarts2');
    this.fun();
  },

  /**
   * 生命周期函数--监听页面显示
   */
  // onShow() {

  // },

  onShow(){
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})

