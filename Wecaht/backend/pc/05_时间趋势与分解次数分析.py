"""
时间趋势与分解次数分析可视化（交互式）
1. 随着时间（年 / 月 / 日）的增加，使用次数的变化
2. 根据分解程度的不同，分解次数（因子数量）的分布
使用 Plotly 生成交互式图表
"""
import sys
import os
from collections import defaultdict, Counter
from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, History

app = create_app()


def generate_time_and_factor_count_charts():
    """生成时间趋势与分解次数分析图（交互式）"""
    # 确保导入所有必要的模块
    import plotly.graph_objects as go
    import plotly.colors as pc
    from plotly.subplots import make_subplots
    from collections import defaultdict
    from app import create_app
    from models import db, History

    app = create_app()

    with app.app_context():
        histories = History.query.all()

        if not histories:
            print("没有历史记录数据，请先运行数据生成脚本")
            return

        # -----------------------------
        # 1. 时间趋势：年 / 月 / 日 的使用次数
        # -----------------------------
        daily_stats = defaultdict(int)
        monthly_stats = defaultdict(int)
        yearly_stats = defaultdict(int)

        for h in histories:
            if not h.create_time:
                continue
            dt = h.create_time
            day_key = dt.date()
            month_key = dt.strftime("%Y-%m")
            year_key = dt.year
            daily_stats[day_key] += 1
            monthly_stats[month_key] += 1
            yearly_stats[year_key] += 1

        # 排序
        daily_dates = sorted(daily_stats.keys())
        daily_counts = [daily_stats[d] for d in daily_dates]

        monthly_keys = sorted(monthly_stats.keys())
        monthly_counts = [monthly_stats[m] for m in monthly_keys]

        yearly_keys = sorted(yearly_stats.keys())
        yearly_counts = [yearly_stats[y] for y in yearly_keys]

        # -----------------------------
        # 2. 分解程度 vs 分解次数（因子数量）
        # -----------------------------
        level_factor_counts = defaultdict(list)

        for h in histories:
            if h.factorization_level_name and h.factor_count is not None:
                level_factor_counts[h.factorization_level_name].append(h.factor_count)

        level_labels = sorted(level_factor_counts.keys())
        avg_factor_counts = [
            (sum(values) / len(values) if values else 0)
            for values in (level_factor_counts[label] for label in level_labels)
        ]
        total_histories_per_level = [
            len(level_factor_counts[label]) for label in level_labels
        ]

        # 为箱线图准备数据
        box_data = [level_factor_counts[label] for label in level_labels]

        # -----------------------------
        # 创建子图：上面时间趋势，下面分解次数分析
        # -----------------------------
        fig = make_subplots(
            rows=2,
            cols=2,
            specs=[[{"colspan": 2}, None], [{"type": "bar"}, {"type": "box"}]],
            subplot_titles=(
                "分解使用次数时间趋势（年 / 月 / 日切换）",
                "不同分解程度的平均分解次数",
                "不同分解程度的分解次数分布",
            ),
            vertical_spacing=0.15,
        )

        # 时间趋势三条折线（用按钮控制显示）
        # 使用颜色
        colors_time = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

        # 年
        fig.add_trace(
            go.Scatter(
                x=yearly_keys,
                y=yearly_counts,
                mode="lines+markers",
                name="按年",
                marker=dict(color=colors_time[0], size=8),
                line=dict(width=3, color=colors_time[0]),
                hovertemplate="<b>%{x}年</b><br>使用次数: %{y}<extra></extra>",
                visible=True,
            ),
            row=1,
            col=1,
        )

        # 月
        fig.add_trace(
            go.Scatter(
                x=monthly_keys,
                y=monthly_counts,
                mode="lines+markers",
                name="按月",
                marker=dict(color=colors_time[1], size=8),
                line=dict(width=3, color=colors_time[1]),
                hovertemplate="<b>%{x}</b><br>使用次数: %{y}<extra></extra>",
                visible=False,
            ),
            row=1,
            col=1,
        )

        # 日
        fig.add_trace(
            go.Scatter(
                x=daily_dates,
                y=daily_counts,
                mode="lines+markers",
                name="按日",
                marker=dict(color=colors_time[2], size=6),
                line=dict(width=2, color=colors_time[2]),
                hovertemplate="<b>%{x}</b><br>使用次数: %{y}<extra></extra>",
                visible=False,
            ),
            row=1,
            col=1,
        )

        # 添加切换按钮（年 / 月 / 日）
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.5,
                    y=1.25,
                    xanchor="center",
                    buttons=[
                        dict(
                            label="按年",
                            method="update",
                            args=[
                                {"visible": [True, False, False, True, True]},
                                {
                                    "xaxis": {
                                        "title": "年份",
                                    }
                                },
                            ],
                        ),
                        dict(
                            label="按月",
                            method="update",
                            args=[
                                {"visible": [False, True, False, True, True]},
                                {
                                    "xaxis": {
                                        "title": "月份",
                                    }
                                },
                            ],
                        ),
                        dict(
                            label="按日",
                            method="update",
                            args=[
                                {"visible": [False, False, True, True, True]},
                                {
                                    "xaxis": {
                                        "title": "日期",
                                    }
                                },
                            ],
                        ),
                    ],
                )
            ]
        )

        # 不同分解程度的平均分解次数（柱状图）
        colors_bar = pc.sample_colorscale(
            "Viridis",
            [i / max(len(level_labels) - 1, 1) for i in range(len(level_labels))],
        )
        fig.add_trace(
            go.Bar(
                x=level_labels,
                y=avg_factor_counts,
                marker=dict(color=colors_bar, line=dict(color="black", width=1)),
                text=[f"{v:.2f}" for v in avg_factor_counts],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>平均分解次数: %{y:.2f}<br>记录数: %{customdata}<extra></extra>",
                customdata=total_histories_per_level,
                name="平均分解次数",
            ),
            row=2,
            col=1,
        )

        # 不同分解程度的分解次数分布（箱线图）
        fig.add_trace(
            go.Box(
                x=[label for label, values in zip(level_labels, box_data) for _ in values],
                y=[v for values in box_data for v in values],
                name="分解次数分布",
                marker_color="#FF6B6B",
                boxmean="sd",
                hovertemplate="<b>%{x}</b><br>分解次数: %{y}<extra></extra>",
            ),
            row=2,
            col=2,
        )

        # 布局和坐标轴
        fig.update_layout(
            title_text="时间趋势与分解次数分析",
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            height=1000,
            font=dict(family="SimHei, Microsoft YaHei, Arial", size=12),
        )

        fig.update_xaxes(title_text="时间", row=1, col=1)
        fig.update_yaxes(title_text="使用次数", row=1, col=1)

        fig.update_xaxes(title_text="分解程度", row=2, col=1)
        fig.update_yaxes(title_text="平均分解次数", row=2, col=1)

        fig.update_xaxes(title_text="分解程度", row=2, col=2)
        fig.update_yaxes(title_text="分解次数", row=2, col=2)

        # 保存为 HTML 文件
        output_path = os.path.join(
            os.path.dirname(__file__), "05_时间趋势与分解次数分析.html"
        )
        fig.write_html(output_path, config={"displayModeBar": True, "locale": "zh-CN"})

        print(f"✅ 交互式图表已保存到: {output_path}")
        print(f"   总记录数: {len(histories)}")
        print("   提示: 在浏览器中打开HTML文件查看交互式图表")


if __name__ == "__main__":
    try:
        generate_time_and_factor_count_charts()
    except Exception as e:
        print(f"❌ 生成图表失败: {e}")
        import traceback

        traceback.print_exc()


