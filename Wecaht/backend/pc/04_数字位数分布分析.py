"""
数字位数分布分析可视化（交互式）
分析用户分解的数字位数分布情况
使用 Plotly 生成交互式图表
"""
import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from collections import Counter

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, History

app = create_app()

def generate_digit_distribution_chart():
    """生成数字位数分布分析图（交互式）"""
    # 确保导入所有必要的模块
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np
    from collections import Counter
    from app import create_app
    from models import db, History
    app = create_app()
    
    with app.app_context():
        # 获取所有历史记录
        histories = History.query.all()
        
        if not histories:
            print('没有历史记录数据，请先运行数据生成脚本')
            return
        
        # 统计数字位数分布
        digit_counts = [h.digit_count for h in histories if h.digit_count]
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('数字位数分布直方图', '位数范围分布', '位数与耗时关系', '各位数范围平均耗时'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 图1：位数分布直方图
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200]
        labels_bin = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', 
                     '61-70', '71-80', '81-90', '91-100', '101-120', '121-150', '151-200']
        
        hist, bin_edges = np.histogram(digit_counts, bins=bins)
        import plotly.colors as pc
        colors = pc.sample_colorscale('Plasma', [i/len(hist) for i in range(len(hist))])
        
        fig.add_trace(
            go.Bar(
                x=labels_bin,
                y=hist,
                marker=dict(
                    color=colors,
                    line=dict(color='black', width=0.5)
                ),
                text=hist,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>记录数: %{y}<extra></extra>',
                name='记录数'
            ),
            row=1, col=1
        )
        
        # 图2：位数分布饼图（简化版）
        digit_ranges = {
            '1-20位': sum(1 for d in digit_counts if 1 <= d <= 20),
            '21-50位': sum(1 for d in digit_counts if 21 <= d <= 50),
            '51-80位': sum(1 for d in digit_counts if 51 <= d <= 80),
            '81-120位': sum(1 for d in digit_counts if 81 <= d <= 120),
            '121-200位': sum(1 for d in digit_counts if 121 <= d <= 200)
        }
        
        labels_pie = [k for k, v in digit_ranges.items() if v > 0]
        values_pie = [v for k, v in digit_ranges.items() if v > 0]
        # 使用 Plotly 的定性颜色方案
        from plotly.colors import qualitative
        default_colors = qualitative.Plotly
        colors_pie = [default_colors[i % len(default_colors)] for i in range(len(labels_pie))]
        
        fig.add_trace(
            go.Pie(
                labels=labels_pie,
                values=values_pie,
                marker=dict(colors=colors_pie),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>记录数: %{value}<br>占比: %{percent}<extra></extra>',
                name='位数分布'
            ),
            row=1, col=2
        )
        
        # 图3：位数与耗时关系（散点图）
        digit_times = [(h.digit_count, h.elapsed_time) for h in histories 
                       if h.digit_count and h.elapsed_time]
        if digit_times:
            digits, times = zip(*digit_times)
            fig.add_trace(
                go.Scatter(
                    x=digits,
                    y=times,
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=digits,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="位数", x=1.15),
                        line=dict(color='black', width=0.5),
                        opacity=0.6
                    ),
                    hovertemplate='<b>位数: %{x}</b><br>耗时: %{y:.3f}秒<extra></extra>',
                    name='位数-耗时'
                ),
                row=2, col=1
            )
        
        # 图4：各位数范围的平均耗时
        range_avg_times = {}
        for range_name, (min_d, max_d) in [
            ('1-20', (1, 20)), ('21-50', (21, 50)), ('51-80', (51, 80)),
            ('81-120', (81, 120)), ('121-200', (121, 200))
        ]:
            range_times = [h.elapsed_time for h in histories 
                          if h.digit_count and min_d <= h.digit_count <= max_d and h.elapsed_time]
            if range_times:
                range_avg_times[range_name] = sum(range_times) / len(range_times)
        
        if range_avg_times:
            ranges = list(range_avg_times.keys())
            avg_times = list(range_avg_times.values())
            # 使用 RdBu 颜色方案（红-蓝，类似 coolwarm）
            colors_bar = pc.sample_colorscale('RdBu', [i/len(ranges) for i in range(len(ranges))])
            fig.add_trace(
                go.Bar(
                    x=ranges,
                    y=avg_times,
                    marker=dict(
                        color=colors_bar,
                        line=dict(color='black', width=1)
                    ),
                    text=[f'{t:.2f}s' for t in avg_times],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>平均耗时: %{y:.2f}秒<extra></extra>',
                    name='平均耗时'
                ),
                row=2, col=2
            )
        
        # 更新布局
        fig.update_layout(
            title_text='数字位数分布分析',
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            height=1000,
            font=dict(family="SimHei, Microsoft YaHei, Arial", size=12)
        )
        
        # 更新坐标轴
        fig.update_xaxes(title_text='数字位数范围', row=1, col=1, tickangle=-45)
        fig.update_yaxes(title_text='记录数', row=1, col=1)
        fig.update_xaxes(title_text='数字位数', row=2, col=1)
        fig.update_yaxes(title_text='耗时（秒）', row=2, col=1)
        fig.update_xaxes(title_text='位数范围', row=2, col=2)
        fig.update_yaxes(title_text='平均耗时（秒）', row=2, col=2)
        
        # 保存为HTML文件
        output_path = os.path.join(os.path.dirname(__file__), '04_数字位数分布分析.html')
        fig.write_html(output_path, config={'displayModeBar': True, 'locale': 'zh-CN'})
        
        print(f'✅ 交互式图表已保存到: {output_path}')
        print(f'   总记录数: {len(histories)}')
        print(f'   位数范围: {min(digit_counts)}-{max(digit_counts)}位')
        print(f'   提示: 在浏览器中打开HTML文件查看交互式图表')

if __name__ == '__main__':
    try:
        generate_digit_distribution_chart()
    except Exception as e:
        print(f'❌ 生成图表失败: {e}')
        import traceback
        traceback.print_exc()
