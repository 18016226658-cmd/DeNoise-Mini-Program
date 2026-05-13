"""
用户等级分布分析可视化（交互式）
分析不同等级用户的使用情况
使用 Plotly 生成交互式图表
"""
import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, History

app = create_app()

def generate_level_distribution_chart():
    """生成用户等级分布分析图（交互式）"""
    # 确保导入所有必要的模块
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np
    from collections import defaultdict
    from app import create_app
    from models import db, User, History
    app = create_app()
    
    with app.app_context():
        # 获取所有用户（除管理员）
        users = User.query.filter(User.username != 'xqq').all()
        
        if not users:
            print('没有用户数据，请先运行数据生成脚本')
            return
        
        # 统计各等级用户数和历史记录数
        level_stats = defaultdict(lambda: {'count': 0, 'histories': 0, 'avg_time': 0})
        
        for user in users:
            level = user.level
            level_stats[level]['count'] += 1
            
            # 获取该用户的历史记录
            histories = History.query.filter_by(user_id=user.id).all()
            level_stats[level]['histories'] += len(histories)
            
            if histories:
                avg_time = sum(h.elapsed_time for h in histories) / len(histories)
                level_stats[level]['avg_time'] += avg_time
        
        # 计算平均耗时
        for level in level_stats:
            if level_stats[level]['count'] > 0:
                level_stats[level]['avg_time'] /= level_stats[level]['count']
        
        # 准备数据
        level_names = {
            'normal': '普通用户',
            'vip': 'VIP用户',
            'svip': 'SVIP用户'
        }
        
        labels = [level_names.get(level, level) for level in level_stats.keys()]
        user_counts = [level_stats[level]['count'] for level in level_stats.keys()]
        history_counts = [level_stats[level]['histories'] for level in level_stats.keys()]
        avg_times = [level_stats[level]['avg_time'] for level in level_stats.keys()]
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('用户数量分布', '各等级历史记录数', '各等级平均分解耗时', '用户数与记录数对比'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 图1：用户数量分布（饼图）
        colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        fig.add_trace(
            go.Pie(
                labels=labels,
                values=user_counts,
                marker=dict(colors=colors1),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>用户数: %{value}<br>占比: %{percent}<extra></extra>',
                name='用户数'
            ),
            row=1, col=1
        )
        
        # 图2：历史记录数分布（柱状图）
        import plotly.colors as pc
        colors2 = pc.sample_colorscale('Viridis', [i/len(labels) for i in range(len(labels))])
        fig.add_trace(
            go.Bar(
                x=labels,
                y=history_counts,
                marker=dict(
                    color=colors2,
                    line=dict(color='black', width=1)
                ),
                text=history_counts,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>历史记录数: %{y}<extra></extra>',
                name='历史记录数'
            ),
            row=1, col=2
        )
        
        # 图3：平均耗时（折线图）
        fig.add_trace(
            go.Scatter(
                x=labels,
                y=avg_times,
                mode='lines+markers',
                marker=dict(size=12, color='#FF6B6B'),
                line=dict(width=3, color='#FF6B6B'),
                fill='tonexty',
                fillcolor='rgba(255, 107, 107, 0.3)',
                text=[f'{t:.2f}s' for t in avg_times],
                textposition='top center',
                hovertemplate='<b>%{x}</b><br>平均耗时: %{y:.2f}秒<extra></extra>',
                name='平均耗时'
            ),
            row=2, col=1
        )
        
        # 图4：综合对比（分组柱状图）
        x = np.arange(len(labels))
        fig.add_trace(
            go.Bar(
                x=labels,
                y=user_counts,
                name='用户数',
                marker=dict(color='#4ECDC4', line=dict(color='black', width=1)),
                hovertemplate='<b>%{x}</b><br>用户数: %{y}<extra></extra>',
                offsetgroup=1
            ),
            row=2, col=2
        )
        fig.add_trace(
            go.Bar(
                x=labels,
                y=[h/10 for h in history_counts],
                name='记录数/10',
                marker=dict(color='#45B7D1', line=dict(color='black', width=1)),
                hovertemplate='<b>%{x}</b><br>记录数/10: %{y:.1f}<extra></extra>',
                offsetgroup=2
            ),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title_text='用户等级分布分析',
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            height=1000,
            font=dict(family="SimHei, Microsoft YaHei, Arial", size=12)
        )
        
        # 更新坐标轴
        fig.update_yaxes(title_text='历史记录数', row=1, col=2)
        fig.update_yaxes(title_text='平均耗时（秒）', row=2, col=1)
        fig.update_yaxes(title_text='数量', row=2, col=2)
        
        # 保存为HTML文件
        output_path = os.path.join(os.path.dirname(__file__), '03_用户等级分布分析.html')
        fig.write_html(output_path, config={'displayModeBar': True, 'locale': 'zh-CN'})
        
        print(f'✅ 交互式图表已保存到: {output_path}')
        for level, name in level_names.items():
            if level in level_stats:
                print(f'   {name}: {level_stats[level]["count"]}个用户, {level_stats[level]["histories"]}条记录')
        print(f'   提示: 在浏览器中打开HTML文件查看交互式图表')

if __name__ == '__main__':
    try:
        generate_level_distribution_chart()
    except Exception as e:
        print(f'❌ 生成图表失败: {e}')
        import traceback
        traceback.print_exc()
