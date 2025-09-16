# -*- coding: utf-8 -*-
"""
打包脚本 - 使用PyInstaller将Python程序打包为Windows可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
            
    # 清理spec文件
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        print(f"删除spec文件: {spec_file}")
        os.remove(spec_file)


def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False
    return True


def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 检测操作系统
    import platform
    is_windows = platform.system() == "Windows"
    is_macos = platform.system() == "Darwin"
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个文件
        '--name=身份证信息提取工具',        # 可执行文件名称
        '--hidden-import=PIL._tkinter_finder',  # 隐式导入
        '--hidden-import=pytesseract',
        '--hidden-import=cv2',
        '--hidden-import=openpyxl',
        '--distpath=dist',              # 输出目录
        '--workpath=build',             # 工作目录
        '--specpath=.',                 # spec文件位置
        'src/main.py'                   # 主程序文件
    ]
    
    # 根据操作系统添加特定参数
    if is_windows:
        cmd.append('--windowed')        # Windows下不显示控制台窗口
        cmd.append('--add-data=src;src')  # Windows路径分隔符
        # 检查图标文件
        if os.path.exists('assets/icon.ico'):
            cmd.append('--icon=assets/icon.ico')
    elif is_macos:
        cmd.append('--windowed')        # macOS下不显示控制台窗口
        cmd.append('--add-data=src:src')  # macOS/Linux路径分隔符
        # 检查图标文件
        if os.path.exists('assets/icon.icns'):
            cmd.append('--icon=assets/icon.icns')
    else:
        # Linux
        cmd.append('--add-data=src:src')  # Linux路径分隔符
    
    print(f"构建目标平台: {platform.system()}")
    if not any('--icon' in arg for arg in cmd):
        print("警告: 未找到图标文件，将使用默认图标")
    
    try:
        subprocess.check_call(cmd)
        print("构建完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False


def create_dist_package():
    """创建发布包"""
    print("创建发布包...")
    
    # 创建发布目录
    release_dir = 'release'
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制可执行文件（根据操作系统确定文件名）
    import platform
    if platform.system() == "Windows":
        exe_file = 'dist/身份证信息提取工具.exe'
    else:
        exe_file = 'dist/身份证信息提取工具'
        
    if os.path.exists(exe_file):
        shutil.copy2(exe_file, release_dir)
        print(f"已复制可执行文件到: {release_dir}")
    else:
        print("错误: 未找到可执行文件")
        return False
    
    # 创建使用说明
    readme_content = """
身份证信息提取工具 使用说明
==============================

功能介绍：
本工具可以批量处理身份证图片，自动识别姓名和民族信息，并导出为Excel文件。

使用步骤：
1. 双击运行"身份证信息提取工具.exe"
2. 点击"浏览"按钮选择包含身份证图片的文件夹
3. 选择Excel输出文件的保存位置
4. 点击"开始处理"按钮开始批量识别
5. 处理完成后会自动生成Excel文件

支持格式：
- 图片格式：JPG、JPEG、PNG、BMP、TIFF、TIF
- 输出格式：Excel (.xlsx)

注意事项：
1. 请确保身份证图片清晰，避免模糊、倾斜
2. 建议图片大小适中，过大或过小可能影响识别准确率
3. 处理过程中请勿关闭程序
4. 如遇到识别错误，可手动修正Excel文件中的结果

技术支持：
如有问题，请联系技术支持团队

版本信息：
版本号：1.0.0
构建日期：2024年
"""
    
    readme_file = os.path.join(release_dir, '使用说明.txt')
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"已创建使用说明: {readme_file}")
    
    # 创建示例文件夹
    examples_dir = os.path.join(release_dir, '示例图片')
    os.makedirs(examples_dir, exist_ok=True)
    
    example_readme = """
请将要处理的身份证图片放在此文件夹中，
然后在程序中选择此文件夹进行批量处理。

支持的图片格式：
- .jpg / .jpeg
- .png
- .bmp
- .tiff / .tif
"""
    
    with open(os.path.join(examples_dir, '请将身份证图片放在这里.txt'), 'w', encoding='utf-8') as f:
        f.write(example_readme)
    
    print("发布包创建完成！")
    return True


def main():
    """主函数"""
    print("身份证信息提取工具 - 构建脚本")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('src/main.py'):
        print("错误: 请在项目根目录下运行此脚本")
        return
    
    # 清理构建目录
    clean_build_dirs()
    
    # 安装依赖
    if not install_dependencies():
        print("构建中止: 依赖安装失败")
        return
    
    # 构建可执行文件
    if not build_executable():
        print("构建中止: 可执行文件生成失败")
        return
    
    # 创建发布包
    if not create_dist_package():
        print("构建中止: 发布包创建失败")
        return
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print(f"可执行文件位置: dist/身份证信息提取工具.exe")
    print(f"发布包位置: release/")
    print("=" * 50)


if __name__ == "__main__":
    main()