// 柱状图
function barOption(data) {
	// 图表内容配置项
	const option = {
		xAxis: {
			// 隐藏x轴刻度线
			axisTick: {
				show: false
			},
			data: data.xData
		},
		yAxis: {
			// 隐藏y轴网格线
			splitLine: {
				show: false
			},
			// 隐藏y轴数值
			axisLabel: {
				show: false
			},
		},
		grid: {
			top: '10%',
			right: '3%',
			left: '3%',
			bottom: '22%'
		},
		series: [{
      type: 'bar',
			barWidth: '20', // 柱的宽度
			data: data.yData,
			// 柱的数值显示
			label: {
				show: true,
				position: 'top',
			},
			itemStyle: {
				color: '#3FD0AA',
				barBorderRadius: 2,
				borderWidth: 1,
				shadowColor: '#3FD0AA',
				borderType: 'dashed'
			}
		}],
		// Echarts 横向滚动
		// dataZoom: [{
		// 	type: 'slider',
		// 	show: true,
		// 	xAxisIndex: [0],
		// 	startValue: 0,
		// 	endValue: 7,
		// 	height: '5%', // 滚动条高度
		// 	bottom: '5%',
		// 	left: '2%',
		// 	right: '3%'
		// }]
	}
	return option
}

// 其他图表的配置...

module.exports = {
	barOption
}
