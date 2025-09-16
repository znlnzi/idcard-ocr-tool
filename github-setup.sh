#!/bin/bash
# GitHub一键构建设置脚本

echo "🚀 GitHub Actions Windows EXE 一键构建设置"
echo "============================================"
echo

# 检查是否已经是git仓库
if [ ! -d ".git" ]; then
    echo "📝 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ 已是Git仓库"
fi

# 创建.gitignore
echo "📝 创建.gitignore文件..."
cat > .gitignore << 'EOF'
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
dist-wine/
build-wine/
release-wine/

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
EOF

echo "✅ .gitignore创建完成"

# 添加所有文件到Git
echo "📦 添加文件到Git..."
git add .
echo "✅ 文件添加完成"

# 提交代码
echo "💾 提交代码..."
if git diff --cached --quiet; then
    echo "⚠️ 没有新的更改需要提交"
else
    git commit -m "🎉 身份证信息提取工具 - 支持Windows EXE自动构建

功能特点:
- 🖼️ 批量身份证图片识别
- 📊 Excel结果导出
- 🤖 自动GitHub Actions构建
- 🍷 多种构建方案支持

技术栈: Python + OpenCV + Tesseract OCR + PyInstaller"
    echo "✅ 代码提交完成"
fi

echo
echo "🎯 接下来的步骤:"
echo "1. 在GitHub上创建新仓库: https://github.com/new"
echo "2. 仓库名称建议: idcard-ocr-tool"
echo "3. 创建后，复制仓库地址，如: https://github.com/用户名/idcard-ocr-tool.git"
echo
echo "然后运行以下命令:"
echo "git remote add origin https://github.com/用户名/idcard-ocr-tool.git"
echo "git branch -M main"
echo "git push -u origin main"
echo
echo "推送完成后:"
echo "🔄 访问GitHub仓库 -> Actions标签页"
echo "⏱️ 等待 'Build Windows EXE' 工作流完成 (约5-10分钟)"
echo "📥 在Artifacts中下载 'windows-executable.zip'"
echo
echo "🎉 Windows EXE文件就生成好了!"