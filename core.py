# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re

# 设置中文字体支持
rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'Heiti TC', 'SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

class XYGraph:
    """直角坐标系图像绘制类"""
    
    def __init__(self, points=500, x_min=-10, x_max=10):
        """
        初始化图形对象
        
        Args: 
            points:  绘制的点数，默认 500
            x_min:  x 轴最小值，默认 -10
            x_max: x 轴最大值，默认 +10
        """
        self.points = points
        self.x_min = x_min
        self.x_max = x_max
        
    def parse_equation(self, equation):
        """
        解析方程式，将数学表达式转换为 Python 可执行的表达式
        
        Args:
            equation: 输入的方程式字符串，如 "y=x^2"
            
        Returns: 
            解析后的表达式字符串
        """
        # 移除空格
        equation = equation.replace(' ', '')
        
        # 提取等号右边的表达式
        if '=' in equation:
            parts = equation.split('=')
            if len(parts) != 2:
                raise ValueError("方程式格式错误，应为 y=f(x) 的形式")
            expression = parts[1]
        else:
            expression = equation
        
        # 将 ^ 替换为 **（Python 的幂运算符）
        expression = expression.replace('^', '**')
        
        # 处理隐式乘法，如 2x -> 2*x
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        
        # 处理函数前的系数，如 2sin(x) -> 2*sin(x)
        expression = re.sub(r'(\d)(sin|cos|tan|sqrt|exp|log|abs)', r'\1*\2', expression)
        
        return expression
    
    def evaluate_expression(self, expression, x_values):
        """
        计算表达式在给定 x 值上的结果
        
        Args: 
            expression: 解析后的表达式
            x_values: x 值数组
            
        Returns: 
            y 值数组
        """
        # 创建安全的数学函数环境
        safe_dict = {
            'x': x_values,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'sqrt': np.sqrt,
            'exp': np.exp,
            'log': np.log,
            'abs':  np.abs,
            'pi': np.pi,
            'e': np.e,
        }
        
        try:
            # 允许使用内置函数以解决 Python 3.14/Numpy 2.x 中的兼容性问题
            y_values = eval(expression, {}, safe_dict)
            return y_values
        except Exception as e:
            raise ValueError(f"计算表达式时出错: {str(e)}")
    
    def plot(self, equation, title=None, show=True, save_path=None):
        """
        绘制方程式图像 (Static CLI Plot)
        
        Args:
            equation: 方程式字符串
            title: 图表标题
            show: 是否显示图形
            save_path: 保存路径（可选）
        """
        try:
            # 解析方程式
            expression = self.parse_equation(equation)
            print(f"📐 解析方程式: {equation}")
            print(f"🔢 转换为表达式: {expression}")
            
            # 生成 x 值
            x_values = np.linspace(self.x_min, self.x_max, self.points)
            
            # 计算 y 值
            y_values = self.evaluate_expression(expression, x_values)
            
            # 创建图形
            plt.figure(figsize=(10, 6))
            
            # 绘制坐标轴
            plt.axhline(y=0, color='k', linewidth=0.5, linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linewidth=0.5, linestyle='-', alpha=0.3)
            
            # 绘制函数曲线
            plt.plot(x_values, y_values, 'b-', linewidth=2, label=equation)
            plt.plot(x_values, y_values, 'ro', markersize=6, alpha=0.6)
            
            # 设置网格
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # 设置标签
            plt.xlabel('x', fontsize=12, fontweight='bold')
            plt.ylabel('y', fontsize=12, fontweight='bold')
            plt.title(title or f'函数图像:  {equation}', fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            
            # 自动调整 y 轴范围
            valid_y = y_values[np.isfinite(y_values)]
            if len(valid_y) > 0:
                y_min, y_max = np.min(valid_y), np.max(valid_y)
                margin = 1.0 if y_min == y_max else (y_max - y_min) * 0.1
                plt.ylim([y_min - margin, y_max + margin])
                
                print(f"✅ 成功绘制 {self.points} 个点")
                print(f"📊 x 范围: [{self.x_min}, {self.x_max}]")
                print(f"📊 y 范围: [{y_min:.2f}, {y_max:.2f}] (有效点: {len(valid_y)}/{len(y_values)})")
            else:
                print(f"⚠️ 警告: 没有有效的 y 值可供绘制 (可能是定义域问题)")
                plt.ylim([-10, 10]) # 默认范围
            
            # 保存图形
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"💾 图形已保存到: {save_path}")
            
            # 显示图形
            if show:
                plt.show()
            
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            raise
