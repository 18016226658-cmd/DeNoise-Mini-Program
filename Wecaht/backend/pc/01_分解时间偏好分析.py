"""
分解时间偏好分析可视化（交互式）
分析用户在不同时间段的使用偏好
使用 Plotly 生成交互式图表
"""
import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from collections import defaultdict
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, History

app = create_app()

def generate_time_preference_chart():
    """生成分解时间偏好分析图（交互式）"""
    # 确保导入所有必要的模块
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np
    from collections import defaultdict
    from app import create_app
    from models import db, History
    app = create_app()
    
    with app.app_context():
        # 获取所有历史记录
        histories = History.query.all()
        
        if not histories:
            print('没有历史记录数据，请先运行数据生成脚本')
            return
        
        # 按小时统计使用次数
        hour_stats = defaultdict(int)
        for history in histories:
            if history.create_time:
                hour = history.create_time.hour
                hour_stats[hour] += 1
        
        # 准备数据
        hours = list(range(24))
        counts = [hour_stats[h] for h in hours]
        hour_labels = [f'{h:02d}:00' for h in hours]
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('24小时使用分布', '时间段使用分布'),
            specs=[[{"type": "bar"}], [{"type": "pie"}]],
            vertical_spacing=0.15
        )
        
        # 图1：24小时使用分布（柱状图）
        # 使用 plotly 的颜色方案
        import plotly.colors as pc
        colors_bar = pc.sample_colorscale('Viridis', [i/23 for i in range(24)])
        
        fig.add_trace(
            go.Bar(
                x=hour_labels,
                y=counts,
                marker=dict(
                    color=colors_bar,
                    line=dict(color='black', width=0.5)
                ),
                text=counts,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>使用次数: %{y}<extra></extra>',
                name='使用次数'
            ),
            row=1, col=1
        )
        
        # 图2：时间段分类统计（饼图）
        time_periods = {
            '凌晨(0-5点)': sum(counts[0:6]),
            '上午(6-11点)': sum(counts[6:12]),
            '下午(12-17点)': sum(counts[12:18]),
            '晚上(18-23点)': sum(counts[18:24])
        }
        
        labels = list(time_periods.keys())
        values = list(time_periods.values())
        colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors_pie),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>使用次数: %{value}<br>占比: %{percent}<extra></extra>',
                name='时间段分布'
            ),
            row=2, col=1
        )
        
        # 更新布局
        fig.update_layout(
            title_text='分解时间偏好分析',
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            height=900,
            font=dict(family="SimHei, Microsoft YaHei, Arial", size=12)
        )
        
        # 更新x轴
        fig.update_xaxes(title_text='时间（小时）', row=1, col=1, tickangle=-45)
        fig.update_yaxes(title_text='使用次数', row=1, col=1)
        
        # 保存为HTML文件
        output_path = os.path.join(os.path.dirname(__file__), '01_分解时间偏好分析.html')
        fig.write_html(output_path, config={'displayModeBar': True, 'locale': 'zh-CN'})
        
        print(f'✅ 交互式图表已保存到: {output_path}')
        print(f'   总记录数: {len(histories)}')
        print(f'   最活跃时段: {max(time_periods.items(), key=lambda x: x[1])[0]}')
        print(f'   提示: 在浏览器中打开HTML文件查看交互式图表')

if __name__ == '__main__':
    try:
        generate_time_preference_chart()
    except Exception as e:
        print(f'❌ 生成图表失败: {e}')
        import traceback
        traceback.print_exc()
