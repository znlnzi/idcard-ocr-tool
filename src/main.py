# -*- coding: utf-8 -*-
"""
身份证信息提取工具主程序
"""

import sys
import os

# 添加src目录到Python路径 - 支持开发环境和打包后的环境
if getattr(sys, 'frozen', False):
    # 如果是PyInstaller打包后的环境
    application_path = os.path.dirname(sys.executable)
    src_path = os.path.join(application_path, 'src')
else:
    # 如果是开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))
    src_path = application_path

sys.path.insert(0, src_path)
sys.path.insert(0, application_path)

try:
    from gui.main_window import MainWindow
except ImportError:
    # 备选导入方式
    try:
        from src.gui.main_window import MainWindow
    except ImportError:
        # 最后的备选方式 - 直接导入
        import importlib.util
        spec = importlib.util.find_spec("gui.main_window")
        if spec is None:
            # 手动添加路径并重试
            possible_paths = [
                os.path.join(os.path.dirname(__file__), 'gui'),
                os.path.join(os.path.dirname(sys.executable), 'gui'),
                os.path.join(os.getcwd(), 'src', 'gui'),
                os.path.join(os.getcwd(), 'gui')
            ]
            
            for path in possible_paths:
                if os.path.exists(os.path.join(path, 'main_window.py')):
                    sys.path.insert(0, os.path.dirname(path))
                    break
            
            from gui.main_window import MainWindow
        else:
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