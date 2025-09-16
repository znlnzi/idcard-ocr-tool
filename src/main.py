# -*- coding: utf-8 -*-
"""
身份证信息提取工具主程序
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from gui.main_window import MainWindow


def main():
    """主函数"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按Enter键退出...")


if __name__ == "__main__":
    main()