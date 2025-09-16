# -*- coding: utf-8 -*-
"""
OCR识别模块
"""

import cv2
import pytesseract
import re
import os
import sys

# 修复PyInstaller打包后的导入问题
try:
    from .preprocessor import ImagePreprocessor
    from ..config.settings import TESSERACT_CONFIG, ID_CARD_REGIONS
except ImportError:
    try:
        from src.ocr.preprocessor import ImagePreprocessor
        from src.config.settings import TESSERACT_CONFIG, ID_CARD_REGIONS
    except ImportError:
        # 动态路径处理
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        
        from ocr.preprocessor import ImagePreprocessor
        from config.settings import TESSERACT_CONFIG, ID_CARD_REGIONS


class IDCardRecognizer:
    
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.setup_tesseract()
        
    def setup_tesseract(self):
        """设置Tesseract OCR"""
        # 根据操作系统设置Tesseract路径
        import platform
        system = platform.system()
        
        if system == "Windows":
            # Windows常见安装路径（包括chocolatey安装路径）
            possible_paths = [
                r"C:\ProgramData\chocolatey\lib\tesseract\tools\tesseract.exe",
                r"C:\Program Files\Tesseract-OCR\tesseract.exe", 
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe"
            ]
            
            for path in possible_paths:
                expanded_path = os.path.expandvars(path)
                if os.path.exists(expanded_path):
                    pytesseract.pytesseract.tesseract_cmd = expanded_path
                    print(f"找到Tesseract: {expanded_path}")
                    break
            else:
                # 如果都找不到，尝试从PATH中查找
                import shutil
                tesseract_path = shutil.which("tesseract")
                if tesseract_path:
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    print(f"从PATH找到Tesseract: {tesseract_path}")
                else:
                    print("警告：未找到Tesseract OCR，OCR功能可能无法工作")
        
        # 测试Tesseract是否可用
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            print(f"警告：Tesseract OCR未正确安装或配置: {e}")
            print("请确保已安装Tesseract OCR并正确配置路径")
            
    def recognize(self, image_path):
        """识别身份证信息"""
        try:
            # 预处理图像
            processed_image = self.preprocessor.preprocess_for_ocr(image_path)
            
            # 提取文字区域
            regions = self.preprocessor.extract_text_regions(processed_image, ID_CARD_REGIONS)
            
            # 识别姓名
            name = ""
            if 'name' in regions:
                name = self.recognize_name(regions['name'])
                
            # 识别民族
            ethnicity = ""
            if 'ethnicity' in regions:
                ethnicity = self.recognize_ethnicity(regions['ethnicity'])
                
            return {
                'success': True,
                'name': name,
                'ethnicity': ethnicity
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def recognize_name(self, name_region):
        """识别姓名"""
        try:
            # 使用中文语言包进行OCR
            config = TESSERACT_CONFIG + " -l chi_sim"
            text = pytesseract.image_to_string(name_region, config=config)
            
            # 清理文本
            name = self.clean_name_text(text)
            
            return name
            
        except Exception as e:
            print(f"姓名识别失败: {e}")
            return ""
            
    def recognize_ethnicity(self, ethnicity_region):
        """识别民族"""
        try:
            # 使用中文语言包进行OCR
            config = TESSERACT_CONFIG + " -l chi_sim"
            text = pytesseract.image_to_string(ethnicity_region, config=config)
            
            # 清理文本
            ethnicity = self.clean_ethnicity_text(text)
            
            return ethnicity
            
        except Exception as e:
            print(f"民族识别失败: {e}")
            return ""
            
    def clean_name_text(self, text):
        """清理姓名文本"""
        if not text:
            return ""
            
        # 移除空白字符
        text = text.strip()
        
        # 移除非中文字符（保留常见姓名字符）
        text = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', '', text)
        
        # 移除常见的OCR误识别字符
        text = text.replace('姓名', '').replace('名', '').replace('姓', '')
        
        # 限制长度（中文姓名一般不超过4个字）
        if len(text) > 6:
            text = text[:6]
            
        return text.strip()
        
    def clean_ethnicity_text(self, text):
        """清理民族文本"""
        if not text:
            return ""
            
        # 移除空白字符
        text = text.strip()
        
        # 移除非中文字符
        text = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', '', text)
        
        # 移除常见的OCR误识别字符
        text = text.replace('民族', '').replace('族', '').replace('民', '')
        
        # 常见民族名称映射（处理OCR识别错误）
        ethnicity_map = {
            '汉': '汉族',
            '蒙': '蒙古族',
            '蒙古': '蒙古族',
            '回': '回族',
            '藏': '藏族',
            '维': '维吾尔族',
            '维吾尔': '维吾尔族',
            '苗': '苗族',
            '彝': '彝族',
            '壮': '壮族',
            '布依': '布依族',
            '朝鲜': '朝鲜族',
            '满': '满族',
            '侗': '侗族',
            '瑶': '瑶族',
            '白': '白族',
            '土家': '土家族',
            '哈尼': '哈尼族',
            '哈萨克': '哈萨克族',
            '傣': '傣族',
            '黎': '黎族',
            '傈僳': '傈僳族',
            '佤': '佤族',
            '畲': '畲族',
            '高山': '高山族',
            '拉祜': '拉祜族',
            '水': '水族',
            '东乡': '东乡族',
            '纳西': '纳西族',
            '景颇': '景颇族',
            '柯尔克孜': '柯尔克孜族',
            '土': '土族',
            '达斡尔': '达斡尔族',
            '仫佬': '仫佬族',
            '羌': '羌族',
            '布朗': '布朗族',
            '撒拉': '撒拉族',
            '毛南': '毛南族',
            '仡佬': '仡佬族',
            '锡伯': '锡伯族',
            '阿昌': '阿昌族',
            '普米': '普米族',
            '塔吉克': '塔吉克族',
            '怒': '怒族',
            '乌孜别克': '乌孜别克族',
            '俄罗斯': '俄罗斯族',
            '鄂温克': '鄂温克族',
            '德昂': '德昂族',
            '保安': '保安族',
            '裕固': '裕固族',
            '京': '京族',
            '塔塔尔': '塔塔尔族',
            '独龙': '独龙族',
            '鄂伦春': '鄂伦春族',
            '赫哲': '赫哲族',
            '门巴': '门巴族',
            '珞巴': '珞巴族',
            '基诺': '基诺族'
        }
        
        # 尝试匹配民族名称
        for key, value in ethnicity_map.items():
            if key in text:
                return value
                
        # 如果没有匹配到，检查是否已经是完整的民族名称
        if text.endswith('族'):
            return text
        elif text and len(text) <= 4:
            # 对于短文本，可能是民族名称的一部分，直接加上"族"
            return text + '族'
            
        return text.strip()
        
    def recognize_with_multiple_methods(self, image_path):
        """使用多种方法进行识别以提高准确率"""
        results = []
        
        try:
            # 方法1：标准预处理
            result1 = self.recognize(image_path)
            results.append(result1)
            
            # 方法2：不同的预处理参数
            # 可以添加其他预处理方法
            
            # 选择最佳结果
            best_result = self.select_best_result(results)
            return best_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def select_best_result(self, results):
        """从多个识别结果中选择最佳结果"""
        if not results:
            return {'success': False, 'error': '无识别结果'}
            
        # 优先选择成功的结果
        successful_results = [r for r in results if r.get('success', False)]
        
        if not successful_results:
            return results[0]  # 如果都失败，返回第一个结果
            
        # 选择姓名和民族都不为空的结果
        complete_results = [r for r in successful_results 
                          if r.get('name', '') and r.get('ethnicity', '')]
        
        if complete_results:
            return complete_results[0]
            
        # 选择至少有一个字段不为空的结果
        partial_results = [r for r in successful_results 
                         if r.get('name', '') or r.get('ethnicity', '')]
        
        if partial_results:
            return partial_results[0]
            
        return successful_results[0]