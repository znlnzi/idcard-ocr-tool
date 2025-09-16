#!/bin/bash
# Docker构建Windows EXE脚本

echo "=== Docker 构建 Windows EXE 文件 ==="
echo

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker Desktop"
    echo "   下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 未运行，请启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
docker build -f Dockerfile.windows -t idcard-builder:windows .

if [ $? -ne 0 ]; then
    echo "❌ Docker镜像构建失败"
    exit 1
fi

echo "✅ Docker镜像构建完成"
echo

# 运行容器并构建exe文件
echo "🚀 运行容器构建exe文件..."
docker run --rm \
    -v "$(pwd)/dist-windows:/app/dist" \
    -v "$(pwd)/release-windows:/app/release" \
    idcard-builder:windows

if [ $? -eq 0 ]; then
    echo "✅ Windows EXE 构建完成!"
    echo "📁 输出目录:"
    echo "   - 可执行文件: ./dist-windows/"
    echo "   - 发布包: ./release-windows/"
    echo
    ls -la dist-windows/ 2>/dev/null || echo "   dist-windows/ 目录为空或不存在"
    ls -la release-windows/ 2>/dev/null || echo "   release-windows/ 目录为空或不存在"
else
    echo "❌ 构建失败"
    exit 1
fi