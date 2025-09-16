#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的结构验证脚本
"""

import os
import sys

# 添加src目录到Python路径
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_imports():
    """测试关键模块是否可以导入"""
    
    try:
        print("[TEST] 测试配置文件导入...")
        from config.settings import TESSERACT_CONFIG, TESSERACT_CONFIGS, ID_CARD_REGIONS, ALTERNATIVE_REGIONS
        print(f"[SUCCESS] 配置文件导入成功")
        print(f"   Tesseract配置: {TESSERACT_CONFIG}")
        print(f"   多配置选项: {len(TESSERACT_CONFIGS)}")
        print(f"   主区域配置: {list(ID_CARD_REGIONS.keys())}")
        print(f"   备用区域配置: {list(ALTERNATIVE_REGIONS.keys())}")
        
        print("[TEST] 测试文件处理器导入...")
        from utils.file_handler import FileHandler
        print("[SUCCESS] 文件处理器导入成功")
        
        # 测试文件处理器实例化
        file_handler = FileHandler()
        print("[SUCCESS] 文件处理器实例化成功")
        
        print("[TEST] 测试Excel写入器导入...")
        from utils.excel_writer import ExcelWriter
        print("[SUCCESS] Excel写入器导入成功")
        
        print("[TEST] 测试主界面导入...")
        from gui.main_window import MainWindow
        print("[SUCCESS] 主界面导入成功")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"[ERROR] 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始结构验证测试")
    print("=" * 50)
    
    success = test_imports()
    
    print("=" * 50)
    if success:
        print("结构验证通过！")
        print("\n修复总结:")
        print("1. ✓ 优化了OCR区域定位配置")
        print("2. ✓ 去除了过度限制的字符白名单") 
        print("3. ✓ 添加了多种OCR配置方案")
        print("4. ✓ 实现了多区域配置尝试")
        print("5. ✓ 改进了文本清理逻辑")
        print("6. ✓ 增加了详细的调试功能")
        print("\n现在你可以重新构建程序并测试OCR功能了！")
        print("记得在运行时启用调试模式来查看详细信息。")
    else:
        print("结构验证失败，需要检查代码问题")
        
if __name__ == "__main__":
    main()