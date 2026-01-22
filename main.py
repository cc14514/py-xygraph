#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-xygraph - 数学函数图像绘制工具
帮助孩子通过输入方程式来可视化数学函数
"""

import argparse
from core import XYGraph
from gui import interactive_mode

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(
        description='py-xygraph - 数学函数图像绘制工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例: 
  %(prog)s                          # 进入交互模式
  %(prog)s "y=x^2"                  # 绘制抛物线
  %(prog)s "y=sin(x)" --points 50   # 绘制正弦曲线（50个点）
  %(prog)s "y=x^3" --xmin -5 --xmax 5  # 自定义 x 范围
        '''
    )
    
    parser.add_argument('equation', nargs='?', help='要绘制的方程式，如 y=x^2')
    parser.add_argument('--points', type=int, default=500, help='绘制的点数（默认:  500）')
    parser.add_argument('--xmin', type=float, default=-10, help='x 轴最小值（默认: -10）')
    parser.add_argument('--xmax', type=float, default=10, help='x 轴最大值（默认: 10）')
    parser.add_argument('--save', type=str, help='保存图像到文件')
    
    args = parser.parse_args()
    
    if args.equation:
        # 命令行模式
        graph = XYGraph(points=args.points, x_min=args.xmin, x_max=args.xmax)
        graph.plot(args.equation, save_path=args.save)
    else:
        # GUI 交互模式
        interactive_mode()

if __name__ == '__main__':
    main()
