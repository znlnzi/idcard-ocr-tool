# -*- coding: utf-8 -*-
"""
文件处理工具
"""

import os
from ..config.settings import SUPPORTED_IMAGE_FORMATS


class FileHandler:
    
    def __init__(self):
        pass
        
    def get_image_files(self, folder_path):
        """获取文件夹中的所有图片文件"""
        image_files = []
        
        if not os.path.exists(folder_path):
            raise ValueError(f"文件夹不存在: {folder_path}")
            
        if not os.path.isdir(folder_path):
            raise ValueError(f"路径不是文件夹: {folder_path}")
            
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # 检查是否是文件
                if os.path.isfile(file_path):
                    # 检查文件扩展名
                    _, ext = os.path.splitext(filename.lower())
                    if ext in SUPPORTED_IMAGE_FORMATS:
                        image_files.append(file_path)
                        
        except Exception as e:
            raise ValueError(f"读取文件夹失败: {str(e)}")
            
        # 按文件名排序
        image_files.sort()
        
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