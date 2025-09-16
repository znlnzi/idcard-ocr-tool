# -*- coding: utf-8 -*-
"""
跨平台构建脚本
支持在macOS上构建Windows EXE文件的多种方案
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path


class CrossPlatformBuilder:
    
    def __init__(self):
        self.current_platform = platform.system()
        self.project_root = Path(__file__).parent
        
    def show_menu(self):
        """显示构建选项菜单"""
        print("🔨 身份证信息提取工具 - 跨平台构建器")
        print("=" * 60)
        print()
        print("请选择构建方案:")
        print()
        print("1. 🖥️  当前平台构建 (macOS)")
        print("2. 🌐 GitHub Actions 构建 (推荐)")
        print("3. 🐳 Docker 构建 (需要Docker)")
        print("4. ☁️  在线构建服务")
        print("5. 📋 显示Windows手动构建说明")
        print("0. ❌ 退出")
        print()
        
        choice = input("请输入选项 (0-5): ").strip()
        return choice
        
    def build_current_platform(self):
        """当前平台构建"""
        print(f"🔨 正在{self.current_platform}平台上构建...")
        
        try:
            # 运行原有的构建脚本
            result = subprocess.run([sys.executable, "build.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 构建成功!")
                self.show_build_results()
            else:
                print("❌ 构建失败:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ 构建过程中出现错误: {e}")
            
    def github_actions_build(self):
        """GitHub Actions构建说明"""
        print("🌐 GitHub Actions 自动构建方案")
        print("-" * 40)
        print()
        print("这是最推荐的方案，可以自动构建Windows EXE文件。")
        print()
        print("步骤:")
        print("1. 将代码推送到GitHub仓库")
        print("2. GitHub会自动运行构建流程")
        print("3. 在Actions页面下载构建好的Windows EXE文件")
        print()
        print("详细操作:")
        print()
        
        # 检查是否已经初始化git
        if not os.path.exists('.git'):
            print("📝 初始化Git仓库:")
            print("   git init")
            print("   git add .")
            print("   git commit -m 'Initial commit'")
            print()
            
        print("📤 推送到GitHub:")
        print("   # 在GitHub上创建新仓库，然后:")
        print("   git remote add origin https://github.com/你的用户名/idcard.git")
        print("   git branch -M main") 
        print("   git push -u origin main")
        print()
        print("🔄 触发构建:")
        print("   代码推送后，访问 GitHub仓库 -> Actions 标签页")
        print("   查看 'Build Windows EXE' 工作流程")
        print("   构建完成后在 Artifacts 中下载 windows-executable.zip")
        print()
        
        if input("是否要自动初始化Git仓库? (y/N): ").lower() == 'y':
            self.init_git_repo()
            
    def docker_build(self):
        """Docker构建"""
        print("🐳 Docker 构建方案")
        print("-" * 40)
        print()
        
        # 检查Docker是否安装
        try:
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Docker未安装")
                
            print("✅ Docker已安装")
            print(f"   版本: {result.stdout.strip()}")
            print()
            
        except Exception:
            print("❌ Docker未安装或未运行")
            print("   请先安装Docker Desktop: https://www.docker.com/products/docker-desktop")
            return
            
        print("注意: Docker Windows容器在macOS上可能有兼容性问题")
        print("建议使用GitHub Actions方案")
        print()
        
        if input("确定要继续Docker构建吗? (y/N): ").lower() == 'y':
            try:
                print("🔨 运行Docker构建...")
                result = subprocess.run(["./build-docker.sh"], shell=True)
                
                if result.returncode == 0:
                    print("✅ Docker构建完成!")
                else:
                    print("❌ Docker构建失败")
                    
            except Exception as e:
                print(f"❌ Docker构建出错: {e}")
                
    def online_build_services(self):
        """在线构建服务说明"""
        print("☁️ 在线构建服务")
        print("-" * 40)
        print()
        print("如果GitHub Actions不方便使用，可以考虑以下在线服务:")
        print()
        print("1. 🔗 GitLab CI/CD")
        print("   - 创建GitLab仓库")
        print("   - 使用类似的CI/CD配置")
        print("   - 支持Windows Runner")
        print()
        print("2. 🔗 Azure DevOps")
        print("   - Microsoft的CI/CD服务")
        print("   - 天然支持Windows构建")
        print()
        print("3. 🔗 CircleCI")
        print("   - 支持Windows执行器")
        print("   - 有免费额度")
        print()
        print("4. 🔗 AppVeyor")
        print("   - 专门针对Windows应用的CI服务")
        print("   - 对开源项目免费")
        print()
        
    def show_windows_manual_build(self):
        """显示Windows手动构建说明"""
        print("📋 Windows 手动构建说明")
        print("-" * 40)
        print()
        print("如果有Windows电脑或虚拟机，可以按以下步骤手动构建:")
        print()
        print("前置要求:")
        print("✅ Windows 10/11 系统")
        print("✅ Python 3.8+ (推荐3.9)")
        print("✅ Git (可选)")
        print()
        print("构建步骤:")
        print("1. 📥 下载项目代码到Windows系统")
        print("2. 🔧 安装Tesseract OCR:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("3. 🐍 安装Python依赖:")
        print("   pip install -r requirements.txt")
        print("4. 🔨 运行构建脚本:")
        print("   python build.py")
        print("5. 📦 获取生成的EXE文件:")
        print("   dist/身份证信息提取工具.exe")
        print()
        print("💡 提示: 可以用虚拟机或远程Windows电脑进行构建")
        print()
        
    def init_git_repo(self):
        """初始化Git仓库"""
        try:
            if not os.path.exists('.git'):
                subprocess.run(["git", "init"], check=True)
                print("✅ Git仓库初始化完成")
                
            # 创建.gitignore
            gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# PyInstaller
*.manifest
*.spec
build/
dist/
release/

# macOS
.DS_Store

# Windows
Thumbs.db
*.exe

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.log
"""
            
            with open('.gitignore', 'w') as f:
                f.write(gitignore_content.strip())
                
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit with ID card OCR tool"], check=True)
            
            print("✅ 代码已提交到本地Git仓库")
            print("💡 接下来请在GitHub上创建仓库并推送代码")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git操作失败: {e}")
        except Exception as e:
            print(f"❌ 初始化Git仓库时出错: {e}")
            
    def show_build_results(self):
        """显示构建结果"""
        print()
        print("📊 构建结果:")
        print("-" * 20)
        
        dist_path = self.project_root / "dist"
        release_path = self.project_root / "release"
        
        if dist_path.exists():
            files = list(dist_path.iterdir())
            print(f"📁 dist/ 目录: {len(files)} 个文件")
            for file in files[:3]:  # 只显示前3个文件
                size = file.stat().st_size if file.is_file() else 0
                print(f"   {file.name} ({size/1024/1024:.1f}MB)")
                
        if release_path.exists():
            files = list(release_path.iterdir()) 
            print(f"📦 release/ 目录: {len(files)} 个文件")
            
        print()
        
    def run(self):
        """运行构建器"""
        while True:
            choice = self.show_menu()
            
            if choice == '0':
                print("👋 退出构建器")
                break
            elif choice == '1':
                self.build_current_platform()
            elif choice == '2':
                self.github_actions_build()
            elif choice == '3':
                self.docker_build()
            elif choice == '4':
                self.online_build_services()
            elif choice == '5':
                self.show_windows_manual_build()
            else:
                print("❌ 无效选项，请重新选择")
                
            print()
            input("按Enter键继续...")
            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    builder = CrossPlatformBuilder()
    builder.run()