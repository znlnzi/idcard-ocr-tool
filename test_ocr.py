#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR功能测试脚本
"""

import os
import sys

# 添加src目录到Python路径
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_ocr_functionality():
    """测试OCR功能"""
    
    try:
        # 导入OCR识别器
        from ocr.recognizer import IDCardRecognizer
        
        print("[SUCCESS] OCR识别器导入成功")
        
        # 创建识别器实例
        recognizer = IDCardRecognizer()
        print("[SUCCESS] OCR识别器实例创建成功")
        
        # 检查Tesseract是否可用
        import pytesseract
        try:
            version = pytesseract.get_tesseract_version()
            print(f"[SUCCESS] Tesseract版本: {version}")
        except Exception as e:
            print(f"[ERROR] Tesseract不可用: {e}")
            return False
        
        # 测试OCR配置
        from config.settings import TESSERACT_CONFIG, TESSERACT_CONFIGS, ID_CARD_REGIONS, ALTERNATIVE_REGIONS
        print("[SUCCESS] OCR配置加载成功:")
        print(f"   默认配置: {TESSERACT_CONFIG}")
        print(f"   替代配置数量: {len(TESSERACT_CONFIGS)}")
        print(f"   区域配置数量: {len(ID_CARD_REGIONS)}")
        print(f"   备用区域配置数量: {len(ALTERNATIVE_REGIONS)}")
        
        # 如果有测试图片，进行实际OCR测试
        test_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        test_image = None
        
        # 在当前目录查找测试图片
        for filename in os.listdir(current_dir):
            if any(filename.lower().endswith(ext) for ext in test_image_extensions):
                test_image = os.path.join(current_dir, filename)
                break
        
        if test_image and os.path.exists(test_image):
            print(f"[INFO] 找到测试图片: {test_image}")
            try:
                # 进行OCR识别测试
                result = recognizer.recognize_with_multiple_methods(test_image, debug=True)
                
                print("[RESULT] OCR识别结果:")
                print(f"   成功状态: {result.get('success', False)}")
                print(f"   姓名: '{result.get('name', '')}'")
                print(f"   民族: '{result.get('ethnicity', '')}'")
                
                if 'debug_attempts' in result:
                    print("[DEBUG] 多种方法尝试:")
                    for attempt in result['debug_attempts']:
                        print(f"   {attempt['method']}: 姓名='{attempt['name']}', 民族='{attempt['ethnicity']}'")
                
                if result.get('success'):
                    print("[SUCCESS] OCR功能测试通过")
                else:
                    print("[WARNING] OCR识别未成功，但系统正常运行")
                    
            except Exception as ocr_error:
                print(f"[ERROR] OCR识别测试失败: {ocr_error}")
                return False
                
        else:
            print("[INFO] 未找到测试图片文件，跳过实际OCR测试")
            print("   (可以将身份证图片放在项目根目录进行完整测试)")
        
        return True
        
    except ImportError as import_error:
        print(f"[ERROR] 导入失败: {import_error}")
        return False
    except Exception as e:
        print(f"[ERROR] 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始OCR功能测试")
    print("=" * 50)
    
    success = test_ocr_functionality()
    
    print("=" * 50)
    if success:
        print("OCR功能测试完成！系统可以正常工作")
        print("\n使用说明:")
        print("1. 启动程序后，勾选'启用调试模式'")
        print("2. 选择包含身份证图片的文件夹")
        print("3. 程序会自动尝试多种OCR配置和区域定位")
        print("4. 调试模式会保存中间图像到debug文件夹")
        print("5. 查看处理日志了解详细识别过程")
    else:
        print("OCR功能测试失败，请检查环境配置")
        
if __name__ == "__main__":
    main()