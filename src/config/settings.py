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
TESSERACT_CONFIG = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾百千万亿阿安艾爱奥八白百邦保北贝本比毕边宾博布才材参藏查长常超朝车陈成承程池赤春次从达大丹单道德地第典丁冬东杜段对多额尔发繁方非飞费分丰风峰冯佛福甫府富干刚高戈革格根公古固关光广规贵国海汉杭好和合河黑恒红侯后胡华怀欢黄回慧基吉计佳家建江将交金津进京九居君卡开堪康科克拉来兰老雷里理李立利连良林刘龙路吕马玛买满毛美门蒙梦米民明莫木南楠能尼宁牛诺女欧帕潘培佩鹏品平婆其奇齐起千前强桥琴青清庆求人任日荣如萨撒塞三森山善上少绍社深圳神圣声生胜师十什石时世市手书树双水丝四松苏孙所塔台唐特天田通土图吞托万王为韦卫文武五西希习席县香向小新兴星修许雪雅严盐羊阳尧叶一伊衣依义银音印英永用尤于余鱼宇雨语玉园元远月云再载早泽增张章招真正知志中终州朱珠转庄子族'

# 身份证信息位置配置（相对坐标，百分比）
ID_CARD_REGIONS = {
    'name': {
        'x': 0.12,      # 姓名区域x坐标（相对于卡片宽度）
        'y': 0.15,      # 姓名区域y坐标（相对于卡片高度）
        'width': 0.25,  # 姓名区域宽度
        'height': 0.08  # 姓名区域高度
    },
    'ethnicity': {
        'x': 0.12,      # 民族区域x坐标
        'y': 0.35,      # 民族区域y坐标
        'width': 0.15,  # 民族区域宽度
        'height': 0.08  # 民族区域高度
    }
}

# Excel输出配置
EXCEL_COLUMNS = ['文件名', '姓名', '民族', '识别状态', '备注']

# 界面配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400