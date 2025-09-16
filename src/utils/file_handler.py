# -*- coding: utf-8 -*-
"""
文件处理工具
"""

import os
import sys

# 修复PyInstaller和直接运行的导入问题
try:
    from ..config.settings import SUPPORTED_IMAGE_FORMATS
except ImportError:
    try:
        from src.config.settings import SUPPORTED_IMAGE_FORMATS
    except ImportError:
        # 动态路径处理
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        
        from config.settings import SUPPORTED_IMAGE_FORMATS


class FileHandler:
    
    def __init__(self):
        pass
        
    def get_image_files(self, folder_path):
        """获取文件夹中的所有图片文件"""
        image_files = []
        
        # 标准化路径
        normalized_folder = os.path.normpath(folder_path)
        
        if not os.path.exists(normalized_folder):
            raise ValueError(f"Folder not found: {normalized_folder}")
            
        if not os.path.isdir(normalized_folder):
            raise ValueError(f"Path is not a directory: {normalized_folder}")
        
        print(f"Scanning folder: {normalized_folder}")
        
        try:
            # 获取文件列表
            files = os.listdir(normalized_folder)
            print(f"Found {len(files)} files in directory")
            
            for filename in files:
                try:
                    file_path = os.path.join(normalized_folder, filename)
                    
                    # 标准化文件路径
                    normalized_file_path = os.path.normpath(file_path)
                    
                    # 检查是否是文件
                    if os.path.isfile(normalized_file_path):
                        # 检查文件扩展名
                        _, ext = os.path.splitext(filename.lower())
                        if ext in SUPPORTED_IMAGE_FORMATS:
                            # 验证文件可读性
                            if self.validate_image_file(normalized_file_path)[0]:
                                image_files.append(normalized_file_path)
                                print(f"Added image file: {filename}")
                            else:
                                print(f"Skipped invalid image: {filename}")
                        else:
                            print(f"Skipped non-image file: {filename} (ext: {ext})")
                    else:
                        print(f"Skipped non-file: {filename}")
                        
                except Exception as file_error:
                    print(f"Error processing file {filename}: {file_error}")
                    continue
                        
        except Exception as e:
            raise ValueError(f"Failed to read folder: {str(e)}")
        
        # 按文件名排序
        image_files.sort()
        
        print(f"Total valid image files found: {len(image_files)}")
        return image_files
        
    def validate_image_file(self, file_path):
        """验证图片文件"""
        if not os.path.exists(file_path):
            return False, "文件不存在"
            
        if not os.path.isfile(file_path):
            return False, "路径不是文件"
            
        # 检查文件扩展名
        _, ext = os.path.splitext(file_path.lower())
        if ext not in SUPPORTED_IMAGE_FORMATS:
            return False, f"不支持的文件格式: {ext}"
            
        # 检查文件大小
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False, "文件为空"
            elif file_size > 50 * 1024 * 1024:  # 50MB限制
                return False, "文件过大"
        except Exception as e:
            return False, f"无法读取文件信息: {str(e)}"
            
        return True, "文件有效"
        
    def ensure_directory_exists(self, file_path):
        """确保目录存在"""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                raise ValueError(f"创建目录失败: {str(e)}")
                
    def get_safe_filename(self, filename):
        """获取安全的文件名"""
        # 移除或替换不安全的字符
        unsafe_chars = '<>:"/\\|?*'
        safe_filename = filename
        
        for char in unsafe_chars:
            safe_filename = safe_filename.replace(char, '_')
            
        # 限制文件名长度
        if len(safe_filename) > 200:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:200-len(ext)] + ext
            
        return safe_filename