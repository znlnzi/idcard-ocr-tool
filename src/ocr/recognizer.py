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
    from ..config.settings import TESSERACT_CONFIG, TESSERACT_CONFIGS, ID_CARD_REGIONS, ALTERNATIVE_REGIONS
except ImportError:
    try:
        from src.ocr.preprocessor import ImagePreprocessor
        from src.config.settings import TESSERACT_CONFIG, TESSERACT_CONFIGS, ID_CARD_REGIONS, ALTERNATIVE_REGIONS
    except ImportError:
        # 动态路径处理
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        
        from ocr.preprocessor import ImagePreprocessor
        from config.settings import TESSERACT_CONFIG, TESSERACT_CONFIGS, ID_CARD_REGIONS, ALTERNATIVE_REGIONS


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
            
    def recognize(self, image_path, debug=False):
        """识别身份证信息"""
        try:
            print(f"[DEBUG] 开始识别图像: {image_path}")
            
            # 预处理图像
            processed_image = self.preprocessor.preprocess_for_ocr(image_path)
            print(f"[DEBUG] 预处理完成，图像尺寸: {processed_image.shape}")
            
            # 保存调试图像
            if debug:
                import os
                debug_dir = os.path.join(os.path.dirname(image_path), 'debug')
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                    
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                processed_path = os.path.join(debug_dir, f"{base_name}_processed.jpg")
                cv2.imwrite(processed_path, processed_image)
                print(f"[DEBUG] 预处理图像保存至: {processed_path}")
            
            # 提取文字区域
            regions = self.preprocessor.extract_text_regions(processed_image, ID_CARD_REGIONS)
            print(f"[DEBUG] 提取到 {len(regions)} 个文字区域")
            
            # 保存区域调试图像
            if debug:
                for region_name, region_image in regions.items():
                    region_path = os.path.join(debug_dir, f"{base_name}_{region_name}_region.jpg")
                    cv2.imwrite(region_path, region_image)
                    print(f"[DEBUG] {region_name}区域保存至: {region_path}")
            
            # 识别姓名
            name = ""
            name_raw_text = ""
            if 'name' in regions:
                name_raw_text = self.get_raw_ocr_text(regions['name'])
                print(f"[DEBUG] 姓名区域OCR原始文本: '{name_raw_text}'")
                name = self.recognize_name(regions['name'])
                print(f"[DEBUG] 姓名清理后结果: '{name}'")
                
            # 识别民族
            ethnicity = ""
            ethnicity_raw_text = ""
            if 'ethnicity' in regions:
                ethnicity_raw_text = self.get_raw_ocr_text(regions['ethnicity'])
                print(f"[DEBUG] 民族区域OCR原始文本: '{ethnicity_raw_text}'")
                ethnicity = self.recognize_ethnicity(regions['ethnicity'])
                print(f"[DEBUG] 民族清理后结果: '{ethnicity}'")
            
            result = {
                'success': True,
                'name': name,
                'ethnicity': ethnicity
            }
            
            # 添加调试信息
            if debug:
                result['debug'] = {
                    'name_raw_text': name_raw_text,
                    'ethnicity_raw_text': ethnicity_raw_text,
                    'image_shape': processed_image.shape,
                    'regions_extracted': list(regions.keys())
                }
            
            print(f"[DEBUG] 最终识别结果: 姓名='{name}', 民族='{ethnicity}'")
            return result
            
        except Exception as e:
            print(f"[DEBUG] 识别过程出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
            
    def get_raw_ocr_text(self, region_image, config_name='default'):
        """获取原始OCR文本，用于调试"""
        try:
            # 使用指定的OCR配置
            if config_name in TESSERACT_CONFIGS:
                config = TESSERACT_CONFIGS[config_name] + " -l chi_sim"
            else:
                config = TESSERACT_CONFIG + " -l chi_sim"
                
            text = pytesseract.image_to_string(region_image, config=config)
            return text.strip()
        except Exception as e:
            print(f"OCR识别失败: {e}")
            return ""
    
    def get_multiple_ocr_attempts(self, region_image):
        """使用多种OCR配置尝试识别"""
        results = {}
        
        for config_name in TESSERACT_CONFIGS:
            try:
                config = TESSERACT_CONFIGS[config_name] + " -l chi_sim"
                text = pytesseract.image_to_string(region_image, config=config)
                results[config_name] = text.strip()
            except Exception as e:
                results[config_name] = f"Error: {str(e)}"
                
        return results
    
    def recognize_name(self, name_region):
        """识别姓名 - 使用多种OCR配置尝试"""
        try:
            # 尝试多种OCR配置
            ocr_results = self.get_multiple_ocr_attempts(name_region)
            print(f"[DEBUG] 姓名多种OCR结果: {ocr_results}")
            
            # 选择最佳OCR结果
            best_text = ""
            for config_name, text in ocr_results.items():
                if text and not text.startswith("Error:"):
                    cleaned = self.clean_name_text(text)
                    if cleaned and len(cleaned) >= len(best_text):
                        best_text = cleaned
                        print(f"[DEBUG] 选择{config_name}配置的结果: '{cleaned}'")
            
            print(f"[DEBUG] 姓名最终结果: '{best_text}'")
            return best_text
            
        except Exception as e:
            print(f"姓名识别失败: {e}")
            return ""
            
    def recognize_ethnicity(self, ethnicity_region):
        """识别民族 - 使用多种OCR配置尝试"""
        try:
            # 尝试多种OCR配置
            ocr_results = self.get_multiple_ocr_attempts(ethnicity_region)
            print(f"[DEBUG] 民族多种OCR结果: {ocr_results}")
            
            # 选择最佳OCR结果
            best_text = ""
            for config_name, text in ocr_results.items():
                if text and not text.startswith("Error:"):
                    cleaned = self.clean_ethnicity_text(text)
                    if cleaned and (not best_text or len(cleaned) >= len(best_text)):
                        best_text = cleaned
                        print(f"[DEBUG] 选择{config_name}配置的结果: '{cleaned}'")
            
            print(f"[DEBUG] 民族最终结果: '{best_text}'")
            return best_text
            
        except Exception as e:
            print(f"民族识别失败: {e}")
            return ""
            
    def clean_name_text(self, text):
        """清理姓名文本"""
        if not text:
            return ""
            
        print(f"[DEBUG] 姓名清理前: '{text}'")
        
        # 移除空白字符
        text = text.strip()
        print(f"[DEBUG] 去除空白后: '{text}'")
        
        # 保存原始文本用于备选方案
        original_text = text
        
        # 移除非中文字符，但保留英文字母（少数民族姓名可能包含）
        text = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u0041-\u005a\u0061-\u007a]', '', text)
        print(f"[DEBUG] 保留中英文后: '{text}'")
        
        # 移除常见的OCR误识别标签，但更保守
        if '姓名' in text:
            text = text.replace('姓名', '')
        if text.startswith('名') and len(text) > 1:
            text = text[1:]
        if text.startswith('姓') and len(text) > 1:
            text = text[1:]
        
        print(f"[DEBUG] 移除标签后: '{text}'")
        
        # 如果清理后为空，尝试从原始文本中提取
        if not text.strip():
            # 尝试提取连续的中文字符
            chinese_matches = re.findall(r'[\u4e00-\u9fff]+', original_text)
            if chinese_matches:
                # 选择最长的中文字符串
                text = max(chinese_matches, key=len)
                print(f"[DEBUG] 从原始文本提取: '{text}'")
        
        # 限制长度（中文姓名一般不超过6个字）
        if len(text) > 8:
            text = text[:8]
            
        result = text.strip()
        print(f"[DEBUG] 姓名最终结果: '{result}'")
        return result
        
    def clean_ethnicity_text(self, text):
        """清理民族文本"""
        if not text:
            return ""
            
        print(f"[DEBUG] 民族清理前: '{text}'")
        
        # 移除空白字符
        text = text.strip()
        print(f"[DEBUG] 去除空白后: '{text}'")
        
        # 保存原始文本
        original_text = text
        
        # 移除非中文字符
        text = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', '', text)
        print(f"[DEBUG] 保留中文后: '{text}'")
        
        # 更保守地移除标签
        if '民族' in text:
            text = text.replace('民族', '')
        # 不要随便删除"族"字，因为很多民族名都以"族"结尾
        if text.startswith('民') and len(text) > 1 and not text.endswith('族'):
            text = text[1:]
        
        print(f"[DEBUG] 移除标签后: '{text}'")
        
        # 如果清理后为空，尝试从原始文本中提取
        if not text.strip():
            chinese_matches = re.findall(r'[\u4e00-\u9fff]+', original_text)
            if chinese_matches:
                text = max(chinese_matches, key=len)
                print(f"[DEBUG] 从原始文本提取: '{text}'")
        
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
        
    def recognize_with_multiple_methods(self, image_path, debug=False):
        """使用多种方法进行识别以提高准确率"""
        results = []
        
        try:
            print(f"[DEBUG] 开始多种方法识别: {image_path}")
            
            # 方法1：使用默认区域配置
            result1 = self.recognize_with_regions(image_path, ID_CARD_REGIONS, debug)
            results.append(('default', result1))
            print(f"[DEBUG] 默认区域结果: 姓名='{result1.get('name', '')}', 民族='{result1.get('ethnicity', '')}")
            
            # 如果默认结果不好，尝试其他区域配置
            if not result1.get('success') or (not result1.get('name') and not result1.get('ethnicity')):
                # 方法2：使用备用区域配置1
                result2 = self.recognize_with_regions(image_path, ALTERNATIVE_REGIONS['variant1'], debug)
                results.append(('variant1', result2))
                print(f"[DEBUG] 备用区域1结果: 姓名='{result2.get('name', '')}', 民族='{result2.get('ethnicity', '')}")
                
                # 方法3：使用备用区域配置2
                result3 = self.recognize_with_regions(image_path, ALTERNATIVE_REGIONS['variant2'], debug)
                results.append(('variant2', result3))
                print(f"[DEBUG] 备用区域2结果: 姓名='{result3.get('name', '')}', 民族='{result3.get('ethnicity', '')}")
            
            # 选择最佳结果
            best_result = self.select_best_result([r[1] for r in results])
            
            # 添加调试信息
            if debug:
                best_result['debug_attempts'] = [{'method': method, 'name': r.get('name', ''), 'ethnicity': r.get('ethnicity', '')} for method, r in results]
            
            return best_result
            
        except Exception as e:
            print(f"[DEBUG] 多种方法识别失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def recognize_with_regions(self, image_path, regions_config, debug=False):
        """使用指定的区域配置进行识别"""
        try:
            # 预处理图像
            processed_image = self.preprocessor.preprocess_for_ocr(image_path)
            
            # 提取文字区域
            regions = self.preprocessor.extract_text_regions(processed_image, regions_config)
            
            # 识别姓名和民族
            name = ""
            ethnicity = ""
            
            if 'name' in regions:
                name = self.recognize_name(regions['name'])
                
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