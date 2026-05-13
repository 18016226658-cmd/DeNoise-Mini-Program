"""
职业词云图可视化（交互式）
生成职业分布的词云图和统计图
使用 Plotly 生成交互式图表
"""
import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import numpy as np

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, History

app = create_app()

def generate_job_wordcloud():
    """生成职业词云图（交互式）"""
    # 确保导入所有必要的模块
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np
    from collections import Counter
    from wordcloud import WordCloud
    from app import create_app
    from models import db, User, History
    app = create_app()
    
    with app.app_context():
        # 获取所有用户及其使用次数
        users = User.query.filter(User.username != 'xqq').all()
        
        if not users:
            print('没有用户数据，请先运行数据生成脚本')
            return
        
        # 统计每个职业的使用次数
        job_usage = Counter()
        for user in users:
            if user.job:
                # 获取该用户的历史记录数
                history_count = History.query.filter_by(user_id=user.id).count()
                # 如果没有历史记录，至少计数1次
                job_usage[user.job] += max(history_count, 1)
        
        if not job_usage:
            print('没有职业数据')
            return
        
        # 创建图表（只显示柱状图，词云图单独保存）
        fig = go.Figure()
        
        # 图1：职业使用统计（柱状图）
        jobs = list(job_usage.keys())
        counts = list(job_usage.values())
        
        # 按使用次数排序
        sorted_data = sorted(zip(jobs, counts), key=lambda x: x[1], reverse=True)
        jobs_sorted = [x[0] for x in sorted_data]
        counts_sorted = [x[1] for x in sorted_data]
        
        # 使用 Plotly 的定性颜色方案
        import plotly.colors as pc
        from plotly.colors import qualitative
        # 使用 Plotly 的默认定性颜色，如果不够则循环使用
        default_colors = qualitative.Plotly
        colors = [default_colors[i % len(default_colors)] for i in range(len(jobs_sorted))]
        
        fig.add_trace(
            go.Bar(
                y=jobs_sorted,
                x=counts_sorted,
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='black', width=0.5)
                ),
                text=counts_sorted,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>使用次数: %{x}<extra></extra>',
                name='使用次数'
            )
        )
        
        # 生成词云图并保存为单独文件
        wordcloud_text = []
        for job, count in job_usage.items():
            wordcloud_text.extend([job] * count)
        
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SimHei.ttf')
        if not os.path.exists(font_path):
            font_path = None
        
        try:
            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color='white',
                font_path=font_path,
                max_words=100,
                colormap='viridis',
                relative_scaling=0.5,
                random_state=42
            ).generate(' '.join(wordcloud_text))
            
            # 保存词云图为PNG
            wordcloud_path = os.path.join(os.path.dirname(__file__), '02_职业词云图_词云.png')
            wordcloud.to_file(wordcloud_path)
            print(f'   词云图已保存到: {wordcloud_path}')
        except Exception as e:
            print(f'   ⚠️ 生成词云图失败: {e}')
        
        # 更新布局
        fig.update_layout(
            title_text='职业使用统计',
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            height=600,
            xaxis_title='使用次数',
            yaxis_title='职业',
            font=dict(family="SimHei, Microsoft YaHei, Arial", size=12)
        )
        
        # 保存为HTML文件
        output_path = os.path.join(os.path.dirname(__file__), '02_职业词云图.html')
        fig.write_html(output_path, config={'displayModeBar': True, 'locale': 'zh-CN'})
        
        print(f'✅ 交互式图表已保存到: {output_path}')
        print(f'   职业种类: {len(job_usage)}')
        print(f'   最活跃职业: {jobs_sorted[0]} ({counts_sorted[0]}次)')
        print(f'   提示: 在浏览器中打开HTML文件查看交互式图表')

if __name__ == '__main__':
    try:
        generate_job_wordcloud()
    except ImportError:
        print('❌ 缺少wordcloud库，请安装: pip install wordcloud')
    except Exception as e:
        print(f'❌ 生成图表失败: {e}')
        import traceback
        traceback.print_exc()
