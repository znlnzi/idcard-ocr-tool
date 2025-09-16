# -*- coding: utf-8 -*-
"""
图像预处理模块
"""

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:
    
    def __init__(self):
        pass
        
    def load_image(self, image_path):
        """加载图像"""
        try:
            # 使用OpenCV加载图像
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"无法加载图像: {image_path}")
            return image
        except Exception as e:
            raise ValueError(f"加载图像失败: {str(e)}")
            
    def resize_image(self, image, max_width=1200, max_height=800):
        """调整图像大小以提高处理速度"""
        h, w = image.shape[:2]
        
        # 计算缩放比例
        scale_w = max_width / w
        scale_h = max_height / h
        scale = min(scale_w, scale_h, 1.0)  # 不放大，只缩小
        
        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
        return image
        
    def enhance_contrast(self, image):
        """增强对比度"""
        # 转换为LAB颜色空间
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab)
        
        # 对L通道应用CLAHE（限制对比度自适应直方图均衡化）
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        
        # 合并通道并转换回BGR
        lab = cv2.merge((l_channel, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
        
    def denoise_image(self, image):
        """图像去噪"""
        # 使用双边滤波去噪，保持边缘
        denoised = cv2.bilateralFilter(image, 9, 75, 75)
        return denoised
        
    def convert_to_grayscale(self, image):
        """转换为灰度图"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        return gray
        
    def threshold_image(self, gray_image):
        """二值化处理"""
        # 使用自适应阈值
        binary = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        return binary
        
    def detect_id_card(self, image):
        """检测身份证区域"""
        gray = self.convert_to_grayscale(image)
        
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 寻找最大的矩形轮廓
        max_area = 0
        best_contour = None
        
        for contour in contours:
            # 近似轮廓
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # 如果是四边形且面积足够大
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if area > max_area and area > 10000:  # 最小面积阈值
                    max_area = area
                    best_contour = approx
                    
        if best_contour is not None:
            # 透视变换矫正
            return self.perspective_transform(image, best_contour)
        else:
            # 如果没有检测到身份证轮廓，返回原图
            return image
            
    def perspective_transform(self, image, contour):
        """透视变换矫正身份证"""
        # 获取四个角点
        points = contour.reshape(4, 2).astype(np.float32)
        
        # 排序角点：左上、右上、右下、左下
        points = self.order_points(points)
        
        # 计算目标尺寸（身份证标准比例约为1.6:1）
        width = 640
        height = 400
        
        # 目标角点
        dst_points = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype=np.float32)
        
        # 计算透视变换矩阵
        matrix = cv2.getPerspectiveTransform(points, dst_points)
        
        # 应用透视变换
        transformed = cv2.warpPerspective(image, matrix, (width, height))
        
        return transformed
        
    def order_points(self, points):
        """排序四个角点"""
        # 初始化排序后的坐标
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # 计算点的和与差
        s = points.sum(axis=1)
        diff = np.diff(points, axis=1)
        
        # 左上角点的和最小，右下角点的和最大
        rect[0] = points[np.argmin(s)]  # 左上
        rect[2] = points[np.argmax(s)]  # 右下
        
        # 右上角点的差最小，左下角点的差最大
        rect[1] = points[np.argmin(diff)]  # 右上
        rect[3] = points[np.argmax(diff)]  # 左下
        
        return rect
        
    def extract_text_regions(self, image, region_configs):
        """提取文字区域"""
        regions = {}
        h, w = image.shape[:2]
        
        for region_name, config in region_configs.items():
            # 计算实际坐标
            x = int(config['x'] * w)
            y = int(config['y'] * h)
            width = int(config['width'] * w)
            height = int(config['height'] * h)
            
            # 确保坐标在图像范围内
            x = max(0, min(x, w - 1))
            y = max(0, min(y, h - 1))
            width = min(width, w - x)
            height = min(height, h - y)
            
            # 提取区域
            region = image[y:y+height, x:x+width]
            
            # 对文字区域进行专门的预处理
            processed_region = self.preprocess_text_region(region)
            regions[region_name] = processed_region
            
        return regions
        
    def preprocess_text_region(self, region):
        """对文字区域进行专门的预处理"""
        if region.size == 0:
            return region
            
        # 放大区域以提高OCR精度
        scale_factor = 3
        h, w = region.shape[:2]
        new_w = w * scale_factor
        new_h = h * scale_factor
        enlarged = cv2.resize(region, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # 转换为灰度
        if len(enlarged.shape) == 3:
            gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
        else:
            gray = enlarged
            
        # 去噪
        denoised = cv2.medianBlur(gray, 3)
        
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
        enhanced = clahe.apply(denoised)
        
        # 二值化
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 形态学操作去除噪点
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return binary
        
    def preprocess_for_ocr(self, image_path):
        """完整的OCR预处理流程"""
        try:
            # 加载图像
            image = self.load_image(image_path)
            
            # 调整大小
            image = self.resize_image(image)
            
            # 去噪
            image = self.denoise_image(image)
            
            # 增强对比度
            image = self.enhance_contrast(image)
            
            # 检测并矫正身份证
            corrected = self.detect_id_card(image)
            
            return corrected
            
        except Exception as e:
            raise ValueError(f"图像预处理失败: {str(e)}")