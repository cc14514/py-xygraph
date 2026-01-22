# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from core import XYGraph

def interactive_mode():
    """交互式图形界面模式"""
    print("=" * 50)
    print("🎨 py-xygraph - GUI 交互模式")
    print("=" * 50)
    print("窗口已打开，请在底部的文本框中输入方程式 (例如: x^2, sin(x))")
    print("按回车键绘制")

    graph = XYGraph()
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(bottom=0.2) # 为文本框留出空间
    
    # 设置初始 x 值
    x_values = np.linspace(graph.x_min, graph.x_max, graph.points)
    
    # 初始化图形元素
    line, = ax.plot([], [], 'b-', linewidth=2, label='Function')
    points_plot, = ax.plot([], [], 'ro', markersize=6, alpha=0.6)
    
    # 设置坐标轴初始状态
    ax.set_xlabel('x', fontsize=12, fontweight='bold')
    ax.set_ylabel('y', fontsize=12, fontweight='bold')
    ax.set_title('请输入方程式', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='k', linewidth=0.5, linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linewidth=0.5, linestyle='-', alpha=0.3)
    ax.set_xlim(graph.x_min, graph.x_max)
    ax.set_ylim(-10, 10)

    # 图形状态存储
    state = {
        'equation': '',
        'xmin': graph.x_min,
        'xmax': graph.x_max
    }

    def update_plot(val=None):
        """更新图形"""
        if not state['equation']:
            return

        try:
            # 重新生成 x 值（范围可能改变）
            x_values = np.linspace(state['xmin'], state['xmax'], graph.points)
            
            # 复用 parse_equation 和 evaluate_expression
            expression = graph.parse_equation(state['equation'])
            y_values = graph.evaluate_expression(expression, x_values)
            
            # 更新数据
            line.set_data(x_values, y_values)
            points_plot.set_data(x_values, y_values)
            
            # 更新标题
            ax.set_title(f"函数图像: {state['equation']}", fontsize=14, fontweight='bold')
            
            # 更新 x 轴范围
            ax.set_xlim(state['xmin'], state['xmax'])

            # 自动调整 y 轴范围
            if np.all(np.isfinite(y_values)):
                y_min, y_max = np.min(y_values), np.max(y_values)
                if y_min == y_max:
                    y_margin = 1.0
                else:
                    y_margin = (y_max - y_min) * 0.1
                ax.set_ylim(y_min - y_margin, y_max + y_margin)
            
            plt.draw()
            print(f"✅ 成功绘制: {state['equation']}, 范围 [{state['xmin']}, {state['xmax']}]")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 错误: {error_msg}")
            ax.set_title(f'错误: {error_msg}', fontsize=12, color='red')
            plt.draw()

    def submit_eq(text):
        state['equation'] = text.strip()
        update_plot()

    def submit_xmin(text):
        try:
            val = float(text)
            if val < state['xmax']:
                state['xmin'] = val
                update_plot()
            else:
                print("❌ xmin 必须小于 xmax")
        except ValueError:
            print("❌ xmin 输入格式错误")

    def submit_xmax(text):
        try:
            val = float(text)
            if val > state['xmin']:
                state['xmax'] = val
                update_plot()
            else:
                print("❌ xmax 必须大于 xmin")
        except ValueError:
             print("❌ xmax 输入格式错误")

    # 添加方程式文本框
    axbox_eq = plt.axes([0.15, 0.05, 0.40, 0.075])
    text_box_eq = TextBox(axbox_eq, 'y= ', initial='', hovercolor='0.95')
    text_box_eq.on_submit(submit_eq)
    
    # 添加 X 轴范围输入框
    axbox_min = plt.axes([0.65, 0.05, 0.10, 0.075]) 
    text_box_min = TextBox(axbox_min, 'x∈[', initial=str(graph.x_min), hovercolor='0.95', label_pad=0.01)
    text_box_min.on_submit(submit_xmin)

    axbox_max = plt.axes([0.80, 0.05, 0.10, 0.075])
    text_box_max = TextBox(axbox_max, ',', initial=str(graph.x_max), hovercolor='0.95', label_pad=0.01)
    # 添加右括弧装饰（可选，这里用 text 简单表示）
    plt.text(1.02, 0.3, ']', transform=axbox_max.transAxes, fontsize=12)
    text_box_max.on_submit(submit_xmax)
    
    plt.show()
