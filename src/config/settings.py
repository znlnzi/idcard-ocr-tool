# -*- coding: utf-8 -*-
"""
配置文件
"""

import os

# 应用配置
APP_NAME = "身份证信息提取工具"
APP_VERSION = "1.0.0"

# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

# OCR配置
# 去除字符白名单限制，让Tesseract自由识别中文
TESSERACT_CONFIG = '--oem 3 --psm 6'

# 替代OCR配置方案
TESSERACT_CONFIGS = {
    'default': '--oem 3 --psm 6',
    'single_line': '--oem 3 --psm 8',  # 单行文字
    'single_word': '--oem 3 --psm 10',  # 单个字符
    'sparse': '--oem 3 --psm 11'  # 稀疏文字
}

# 身份证信息位置配置（相对坐标，百分比）
# 注：根据中国第二代身份证标准布局调整
ID_CARD_REGIONS = {
    'name': {
        'x': 0.13,      # 姓名区域x坐标（相对于卡片宽度）
        'y': 0.12,      # 姓名区域y坐标（相对于卡片高度）
        'width': 0.28,  # 姓名区域宽度（扩大以包含较长姓名）
        'height': 0.10  # 姓名区域高度（适当增加）
    },
    'ethnicity': {
        'x': 0.13,      # 民族区域x坐标（与姓名对齐）
        'y': 0.28,      # 民族区域y坐标（在姓名下方）
        'width': 0.20,  # 民族区域宽度（适当增加）
        'height': 0.10  # 民族区域高度（与姓名保持一致）
    }
}

# 备用区域配置（用于不同版本身份证）
ALTERNATIVE_REGIONS = {
    'variant1': {
        'name': {'x': 0.10, 'y': 0.10, 'width': 0.30, 'height': 0.12},
        'ethnicity': {'x': 0.10, 'y': 0.25, 'width': 0.25, 'height': 0.12}
    },
    'variant2': {
        'name': {'x': 0.15, 'y': 0.15, 'width': 0.25, 'height': 0.08},
        'ethnicity': {'x': 0.15, 'y': 0.32, 'width': 0.18, 'height': 0.08}
    }
}

# Excel输出配置
EXCEL_COLUMNS = ['文件名', '姓名', '民族', '识别状态', '备注']

# 界面配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400