# -*- coding: utf-8 -*-
"""
Wine构建脚本 - 在macOS上使用Wine构建Windows EXE
"""

import os
import sys
import subprocess
import time
from pathlib import Path


class WineBuilder:
    
    def __init__(self):
        self.wine_prefix = os.path.expanduser("~/.wine")
        self.python_version = "3.9.16"
        
    def run_wine_command(self, cmd, check=True):
        """运行Wine命令"""
        print(f"执行Wine命令: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            if e.stderr:
                print(f"错误信息: {e.stderr}")
            if check:
                raise
            return e
            
    def check_wine_environment(self):
        """检查Wine环境"""
        print("🍷 检查Wine环境...")
        
        # 检查Wine版本
        result = subprocess.run(["wine", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Wine未正确安装")
            return False
            
        print(f"✅ Wine版本: {result.stdout.strip()}")
        
        # 初始化Wine前缀（如果需要）
        if not os.path.exists(self.wine_prefix):
            print("🔧 初始化Wine环境...")
            os.environ['WINEARCH'] = 'win64'
            self.run_wine_command(["wineboot", "--init"])
            time.sleep(5)
            
        return True
        
    def install_python_with_wine(self):
        """在Wine中安装Python"""
        print("🐍 在Wine中安装Python...")
        
        # 检查Python是否已安装
        result = self.run_wine_command(["wine", "python", "--version"], check=False)
        if result.returncode == 0:
            print("✅ Python已安装在Wine中")
            return True
            
        print("📥 下载Python安装包...")
        python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-amd64.exe"
        python_installer = f"python-{self.python_version}-amd64.exe"
        
        # 下载Python
        download_cmd = ["curl", "-L", "-o", python_installer, python_url]
        try:
            subprocess.run(download_cmd, check=True)
        except subprocess.CalledProcessError:
            # 如果下载失败，尝试备用版本
            print("⚠️ 下载失败，尝试备用版本...")
            self.python_version = "3.9.13"
            python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-amd64.exe"
            python_installer = f"python-{self.python_version}-amd64.exe"
            download_cmd = ["curl", "-L", "-o", python_installer, python_url]
            subprocess.run(download_cmd, check=True)
            
        print("🔧 安装Python到Wine...")
        # 静默安装Python
        install_cmd = ["wine", python_installer, "/quiet", "InstallAllUsers=1", "PrependPath=1"]
        self.run_wine_command(install_cmd)
        
        # 等待安装完成
        time.sleep(10)
        
        # 验证安装
        result = self.run_wine_command(["wine", "python", "--version"], check=False)
        if result.returncode == 0:
            print("✅ Python安装成功")
            # 清理安装包
            if os.path.exists(python_installer):
                os.remove(python_installer)
            return True
        else:
            print("❌ Python安装失败")
            return False
            
    def install_dependencies(self):
        """在Wine中安装Python依赖"""
        print("📦 安装Python依赖包...")
        
        # 升级pip
        print("⬆️ 升级pip...")
        self.run_wine_command(["wine", "python", "-m", "pip", "install", "--upgrade", "pip"])
        
        # 安装依赖包
        print("📥 安装项目依赖...")
        deps = [
            "pillow>=10.0.0",
            "opencv-python>=4.8.0", 
            "pytesseract>=0.3.10",
            "openpyxl>=3.1.0",
            "pyinstaller>=6.0.0",
            "numpy>=1.24.0"
        ]
        
        for dep in deps:
            print(f"安装 {dep}...")
            result = self.run_wine_command(["wine", "python", "-m", "pip", "install", dep], check=False)
            if result.returncode != 0:
                print(f"⚠️ {dep} 安装失败，继续安装其他依赖...")
                
        print("✅ 依赖安装完成")
        
    def install_tesseract(self):
        """在Wine中安装Tesseract OCR"""
        print("👁️ 安装Tesseract OCR...")
        
        # 下载Tesseract安装包
        tesseract_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
        tesseract_installer = "tesseract-installer.exe"
        
        print("📥 下载Tesseract安装包...")
        try:
            download_cmd = ["curl", "-L", "-o", tesseract_installer, tesseract_url]
            subprocess.run(download_cmd, check=True)
        except subprocess.CalledProcessError:
            print("❌ Tesseract下载失败，构建将继续，但OCR功能可能不工作")
            return False
            
        print("🔧 安装Tesseract...")
        # 静默安装Tesseract
        install_cmd = ["wine", tesseract_installer, "/S"]
        self.run_wine_command(install_cmd, check=False)
        
        time.sleep(5)
        
        # 下载中文语言包
        print("📥 下载中文语言包...")
        lang_url = "https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata"
        try:
            download_cmd = ["curl", "-L", "-o", "chi_sim.traineddata", lang_url]
            subprocess.run(download_cmd, check=True)
            
            # 复制语言包到tessdata目录
            tessdata_dir = f"{self.wine_prefix}/drive_c/Program Files/Tesseract-OCR/tessdata"
            os.makedirs(tessdata_dir, exist_ok=True)
            subprocess.run(["cp", "chi_sim.traineddata", tessdata_dir], check=False)
            os.remove("chi_sim.traineddata")
            
        except subprocess.CalledProcessError:
            print("⚠️ 中文语言包下载失败")
            
        # 清理安装包
        if os.path.exists(tesseract_installer):
            os.remove(tesseract_installer)
            
        print("✅ Tesseract安装完成")
        return True
        
    def build_exe(self):
        """使用Wine中的PyInstaller构建EXE"""
        print("🔨 使用PyInstaller构建Windows EXE...")
        
        # 清理之前的构建
        if os.path.exists("dist"):
            subprocess.run(["rm", "-rf", "dist"], check=False)
        if os.path.exists("build"):
            subprocess.run(["rm", "-rf", "build"], check=False)
            
        # PyInstaller命令
        pyinstaller_cmd = [
            "wine", "python", "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=身份证信息提取工具",
            "--add-data=src;src",
            "--hidden-import=PIL._tkinter_finder",
            "--hidden-import=pytesseract",
            "--hidden-import=cv2",
            "--hidden-import=openpyxl",
            "--distpath=dist-wine",
            "--workpath=build-wine",
            "src/main.py"
        ]
        
        print("🚀 开始构建...")
        result = self.run_wine_command(pyinstaller_cmd, check=False)
        
        if result.returncode == 0:
            print("✅ EXE构建成功！")
            
            # 检查生成的文件
            exe_path = "dist-wine/身份证信息提取工具.exe"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path)
                print(f"📁 生成的EXE文件: {exe_path} ({size/1024/1024:.1f}MB)")
                
                # 创建发布包
                self.create_release_package()
                return True
            else:
                print("❌ 未找到生成的EXE文件")
                return False
        else:
            print("❌ EXE构建失败")
            return False
            
    def create_release_package(self):
        """创建发布包"""
        print("📦 创建发布包...")
        
        release_dir = "release-wine"
        os.makedirs(release_dir, exist_ok=True)
        
        # 复制EXE文件
        exe_src = "dist-wine/身份证信息提取工具.exe"
        exe_dst = f"{release_dir}/身份证信息提取工具.exe"
        if os.path.exists(exe_src):
            subprocess.run(["cp", exe_src, exe_dst], check=True)
            
        # 创建使用说明
        readme_content = """
身份证信息提取工具 (Wine构建版本)
================================

本工具使用Wine在macOS上构建的Windows可执行文件。

使用方法：
1. 双击运行"身份证信息提取工具.exe"
2. 选择包含身份证图片的文件夹
3. 设置输出Excel文件路径
4. 点击"开始处理"进行批量识别

支持格式：
- 图片：JPG、JPEG、PNG、BMP、TIFF等
- 输出：Excel (.xlsx)

注意事项：
- 确保身份证图片清晰完整
- 建议图片大小适中，避免过大或过小
- 如遇到问题，请检查是否安装了必要的运行库

构建信息：
- 构建方式：Wine + PyInstaller
- 构建时间：%s
- Python版本：%s
""" % (time.strftime("%Y-%m-%d %H:%M:%S"), self.python_version)

        with open(f"{release_dir}/使用说明.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
            
        print(f"✅ 发布包已创建: {release_dir}/")
        
    def run(self):
        """运行完整的构建流程"""
        print("🍷 Wine构建器 - 在macOS上构建Windows EXE")
        print("=" * 60)
        
        try:
            # 检查环境
            if not self.check_wine_environment():
                return False
                
            # 安装Python
            if not self.install_python_with_wine():
                return False
                
            # 安装依赖
            self.install_dependencies()
            
            # 安装Tesseract
            self.install_tesseract()
            
            # 构建EXE
            if self.build_exe():
                print("\n🎉 构建完成！")
                print("📁 Windows EXE文件位置:")
                print("   - dist-wine/身份证信息提取工具.exe")
                print("   - release-wine/身份证信息提取工具.exe (发布版)")
                return True
            else:
                return False
                
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断构建")
            return False
        except Exception as e:
            print(f"\n❌ 构建过程出现错误: {e}")
            return False


if __name__ == "__main__":
    builder = WineBuilder()
    success = builder.run()
    sys.exit(0 if success else 1)