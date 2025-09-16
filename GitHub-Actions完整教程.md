# 🚀 GitHub Actions 完整操作教程

## 📋 前置准备

### 需要的账号
- GitHub账号（免费）：https://github.com/join

### 本地环境
- ✅ 项目代码已准备完毕
- ✅ Git已配置好
- ✅ GitHub Actions工作流已创建

## 🎯 详细操作步骤

### 步骤1：创建GitHub仓库

1. **访问GitHub创建页面**
   ```
   https://github.com/new
   ```

2. **填写仓库信息**
   - Repository name: `idcard-ocr-tool` （推荐名称）
   - Description: `身份证信息提取工具 - 批量OCR识别和Excel导出`
   - ✅ Public（公开仓库，免费使用Actions）
   - ❌ 不要勾选 "Add a README file"
   - ❌ 不要勾选 "Add .gitignore"
   - ❌ 不要勾选 "Choose a license"

3. **点击"Create repository"**

### 步骤2：推送代码到GitHub

在终端中运行以下命令（替换你的用户名）：

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/idcard-ocr-tool.git

# 设置主分支名称
git branch -M main

# 推送代码
git push -u origin main
```

**示例**：
如果你的GitHub用户名是 `zhangsan`，那么命令是：
```bash
git remote add origin https://github.com/zhangsan/idcard-ocr-tool.git
git branch -M main
git push -u origin main
```

### 步骤3：触发自动构建

1. **推送完成后，访问你的仓库**
   ```
   https://github.com/YOUR_USERNAME/idcard-ocr-tool
   ```

2. **点击 "Actions" 标签页**
   - 你会看到 "Build Windows EXE" 工作流
   - 如果是第一次推送，工作流会自动开始运行

3. **监控构建过程**
   - 点击正在运行的工作流
   - 你可以看到实时的构建日志
   - 整个过程大约需要 5-10 分钟

### 步骤4：下载Windows EXE文件

1. **等待构建完成**
   - 状态显示绿色✅表示构建成功
   - 状态显示红色❌表示构建失败（需要检查日志）

2. **下载构建产物**
   - 在完成的工作流页面向下滚动
   - 找到 "Artifacts" 部分
   - 点击下载 `windows-executable` 文件
   - 这是一个ZIP压缩包，包含了Windows EXE文件

3. **解压获得EXE文件**
   ```
   windows-executable.zip
   ├── 身份证信息提取工具.exe    # Windows可执行文件
   └── release/
       ├── 身份证信息提取工具.exe
       ├── 使用说明.txt
       └── 示例图片/
   ```

## 🔄 后续使用

### 修改代码后重新构建
每次修改代码后，只需要：
```bash
git add .
git commit -m "更新功能"
git push
```

GitHub会自动触发新的构建，生成新版本的EXE文件。

### 手动触发构建
如果需要手动触发构建：
1. 进入仓库的Actions页面
2. 选择 "Build Windows EXE" 工作流
3. 点击 "Run workflow" 按钮
4. 点击 "Run workflow" 确认

## 🛠️ 故障排除

### 常见问题1：推送失败
**错误信息**: `Permission denied (publickey)`

**解决方案**:
1. 使用HTTPS方式（推荐）：
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/idcard-ocr-tool.git
   ```

2. 或者配置SSH密钥：
   ```bash
   ssh-keygen -t rsa -C "your_email@example.com"
   # 将 ~/.ssh/id_rsa.pub 内容添加到GitHub账号的SSH Keys中
   ```

### 常见问题2：构建失败
**可能原因**:
- 依赖包版本不兼容
- Python版本问题
- Tesseract安装失败

**解决方案**:
1. 查看构建日志找到具体错误
2. 修改 `.github/workflows/build-windows.yml` 文件
3. 重新提交代码触发构建

### 常见问题3：无法下载Artifacts
**原因**: GitHub要求登录才能下载

**解决方案**:
1. 确保已登录GitHub账号
2. 如果是私有仓库，确保有访问权限
3. Artifacts有保留期限（默认90天）

## 🎯 优化建议

### 加快构建速度
在 `.github/workflows/build-windows.yml` 中添加缓存：
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 添加版本号
可以使用Git标签触发版本发布：
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 多平台构建
修改工作流支持同时构建Windows、macOS、Linux版本：
```yaml
strategy:
  matrix:
    os: [windows-latest, macos-latest, ubuntu-latest]
runs-on: ${{ matrix.os }}
```

## 📊 构建结果说明

### 成功构建后你会得到：
- ✅ `身份证信息提取工具.exe` (约50MB)
- ✅ 完整的使用说明文档
- ✅ 示例图片文件夹
- ✅ 所有必要的运行库已打包

### EXE文件特点：
- 🖥️ 支持Windows 10/11 (64位)
- 📦 单文件部署，无需安装Python
- 🔒 已包含Tesseract OCR引擎
- 🌏 支持中文OCR识别
- 💾 大小约50MB，启动速度快

## 🎉 大功告成！

按照以上步骤，你就可以在macOS上成功生成Windows EXE文件了！

整个过程：
1. ⏰ 创建仓库：2分钟
2. ⏰ 推送代码：1分钟  
3. ⏰ 等待构建：8分钟
4. ⏰ 下载文件：1分钟

**总计12分钟**，你就有了一个专业的Windows可执行文件！