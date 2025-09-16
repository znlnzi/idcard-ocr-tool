# -*- coding: utf-8 -*-
"""
简化的Wine构建方案 - 使用现有Python + 交叉编译
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description=""):
    """运行命令并显示结果"""
    if description:
        print(f"🔨 {description}...")
    print(f"执行: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False


def create_wine_spec_file():
    """创建专门的PyInstaller spec文件用于Wine"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=[
        'PIL._tkinter_finder',
        'pytesseract',
        'cv2', 
        'openpyxl',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='身份证信息提取工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('wine-build.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 创建Wine构建spec文件")


def build_with_wine():
    """使用Wine构建Windows EXE"""
    print("🍷 使用Wine构建Windows EXE文件")
    print("=" * 50)
    
    # 检查Wine是否可用
    try:
        result = subprocess.run(["wine", "--version"], capture_output=True, text=True)
        print(f"✅ Wine版本: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Wine未安装，请先安装Wine")
        return False
    
    # 清理之前的构建
    print("🧹 清理之前的构建...")
    for dir_name in ['build', 'dist', 'dist-wine', 'build-wine']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 创建spec文件
    create_wine_spec_file()
    
    # 方法1：尝试使用Wine运行PyInstaller
    print("\n📦 方法1: 尝试使用Wine中的Python...")
    
    # 检查Wine中是否有Python
    wine_python_check = subprocess.run(
        ["wine", "python", "--version"], 
        capture_output=True, text=True
    )
    
    if wine_python_check.returncode == 0:
        print(f"✅ Wine中发现Python: {wine_python_check.stdout.strip()}")
        
        # 尝试在Wine中安装PyInstaller
        print("📦 在Wine中安装PyInstaller...")
        wine_pip_result = subprocess.run([
            "wine", "python", "-m", "pip", "install", "pyinstaller"
        ], capture_output=True, text=True)
        
        if wine_pip_result.returncode == 0:
            print("✅ PyInstaller安装成功")
            
            # 使用Wine中的PyInstaller构建
            wine_build_cmd = [
                "wine", "python", "-m", "PyInstaller",
                "--onefile",
                "--windowed", 
                "--name=身份证信息提取工具",
                "--distpath=dist-wine",
                "--workpath=build-wine",
                "wine-build.spec"
            ]
            
            if run_command(wine_build_cmd, "使用Wine PyInstaller构建"):
                return check_build_result("dist-wine")
    
    # 方法2：使用本地PyInstaller + Wine前缀
    print("\n📦 方法2: 使用本地PyInstaller配置Wine目标...")
    
    # 设置Wine环境变量
    env = os.environ.copy()
    env['WINE'] = 'wine'
    env['WINEPREFIX'] = os.path.expanduser('~/.wine')
    
    # 使用本地PyInstaller，但指定Windows目标
    local_build_cmd = [
        sys.executable, "-m", "PyInstaller", 
        "--onefile",
        "--windowed",
        "--name=身份证信息提取工具", 
        "--distpath=dist-wine",
        "--workpath=build-wine",
        "--target-architecture=x86_64",
        "wine-build.spec"
    ]
    
    if run_command(local_build_cmd, "使用本地PyInstaller构建"):
        return check_build_result("dist-wine")
    
    # 方法3：修改现有macOS构建为Wine兼容
    print("\n📦 方法3: 修改现有构建为Wine兼容...")
    
    # 使用现有的虚拟环境
    venv_python = "./venv/bin/python"
    if os.path.exists(venv_python):
        modified_build_cmd = [
            venv_python, "-m", "PyInstaller",
            "--onefile",
            "--name=身份证信息提取工具",
            "--distpath=dist-wine", 
            "--workpath=build-wine",
            "--add-data=src:src",
            "--hidden-import=PIL._tkinter_finder",
            "--hidden-import=pytesseract",
            "--hidden-import=cv2",
            "--hidden-import=openpyxl",
            "src/main.py"
        ]
        
        if run_command(modified_build_cmd, "使用虚拟环境PyInstaller构建"):
            # 尝试使用Wine运行生成的二进制文件
            return check_and_convert_build("dist-wine")
    
    print("❌ 所有构建方法都失败了")
    return False


def check_build_result(dist_dir):
    """检查构建结果"""
    exe_path = f"{dist_dir}/身份证信息提取工具"
    exe_path_with_ext = f"{dist_dir}/身份证信息提取工具.exe"
    
    if os.path.exists(exe_path_with_ext):
        size = os.path.getsize(exe_path_with_ext)
        print(f"✅ 发现Windows EXE: {exe_path_with_ext} ({size/1024/1024:.1f}MB)")
        create_release_package(exe_path_with_ext)
        return True
    elif os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"✅ 发现可执行文件: {exe_path} ({size/1024/1024:.1f}MB)")
        # 重命名为.exe
        shutil.move(exe_path, exe_path_with_ext)
        create_release_package(exe_path_with_ext)
        return True
    else:
        print(f"❌ 未找到构建结果在 {dist_dir}")
        return False


def check_and_convert_build(dist_dir):
    """检查并转换构建结果"""
    exe_path = f"{dist_dir}/身份证信息提取工具"
    
    if os.path.exists(exe_path):
        # 检查文件类型
        file_result = subprocess.run(["file", exe_path], capture_output=True, text=True)
        print(f"📋 文件类型: {file_result.stdout}")
        
        # 如果是macOS可执行文件，尝试用Wine运行看是否兼容
        if "Mach-O" in file_result.stdout:
            print("⚠️ 生成的是macOS二进制文件，不是Windows EXE")
            print("💡 建议使用其他方案（如GitHub Actions）生成真正的Windows EXE")
            return False
        else:
            # 重命名为.exe并创建发布包
            exe_with_ext = f"{exe_path}.exe"
            shutil.move(exe_path, exe_with_ext)
            create_release_package(exe_with_ext)
            return True
    
    return False


def create_release_package(exe_path):
    """创建发布包"""
    print("📦 创建发布包...")
    
    release_dir = "release-wine"
    os.makedirs(release_dir, exist_ok=True)
    
    # 复制EXE文件
    exe_filename = os.path.basename(exe_path)
    shutil.copy2(exe_path, f"{release_dir}/{exe_filename}")
    
    # 创建使用说明
    readme_content = """
身份证信息提取工具 (Wine构建版本)
================================

本工具使用Wine在macOS上构建，目标为Windows系统。

使用方法：
1. 双击运行"身份证信息提取工具.exe"
2. 选择包含身份证图片的文件夹
3. 设置输出Excel文件路径  
4. 点击"开始处理"进行批量识别

支持格式：
- 输入图片：JPG、JPEG、PNG、BMP、TIFF等
- 输出文件：Excel (.xlsx)

注意事项：
- 需要在Windows系统上运行
- 确保身份证图片清晰完整
- 建议安装Microsoft Visual C++ Redistributable

如果遇到问题：
1. 尝试安装最新的Windows运行库
2. 检查杀毒软件是否误报
3. 以管理员身份运行

构建信息：
- 构建方式：Wine + PyInstaller
- 目标平台：Windows x64
"""

    with open(f"{release_dir}/使用说明.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ 发布包已创建: {release_dir}/")
    print(f"📁 主要文件:")
    print(f"   - {release_dir}/{exe_filename}")
    print(f"   - {release_dir}/使用说明.txt")


def main():
    """主函数"""
    try:
        success = build_with_wine()
        
        if success:
            print("\n🎉 Wine构建完成!")
            print("📁 生成的Windows EXE文件:")
            print("   - dist-wine/身份证信息提取工具.exe")
            print("   - release-wine/身份证信息提取工具.exe (发布版)")
            print("\n💡 提示: 请在Windows系统上测试生成的EXE文件")
        else:
            print("\n❌ Wine构建失败")
            print("💡 建议尝试其他方案:")
            print("   - GitHub Actions自动构建")
            print("   - 在Windows电脑上手动构建")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断构建")
    except Exception as e:
        print(f"\n❌ 构建过程出现错误: {e}")


if __name__ == "__main__":
    main()