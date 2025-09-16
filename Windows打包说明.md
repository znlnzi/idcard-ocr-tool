# Windows系统打包说明

当前在macOS系统上生成的是macOS可执行文件。如需要生成Windows exe文件，请在Windows系统上执行以下步骤：

## Windows环境要求

1. **Python 3.8+** 
2. **Tesseract OCR** (必须安装)

## Windows打包步骤

### 1. 安装Tesseract OCR
- 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
- 推荐安装到默认路径：`C:\Program Files\Tesseract-OCR\`
- 下载中文语言包：https://github.com/tesseract-ocr/tessdata
- 将 `chi_sim.traineddata` 放到 `C:\Program Files\Tesseract-OCR\tessdata\` 目录

### 2. 安装Python依赖
```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行打包脚本
```bash
python build.py
```

### 4. 生成的文件
- 可执行文件：`dist/身份证信息提取工具.exe`
- 发布包：`release/` 目录

## 注意事项

1. **Tesseract路径**：程序会自动检测以下路径的Tesseract：
   - `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
   - `C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe`

2. **中文语言包**：确保安装了中文简体语言包 `chi_sim.traineddata`

3. **权限问题**：如果遇到权限问题，请以管理员身份运行命令提示符

4. **杀毒软件**：部分杀毒软件可能会误报，需要添加信任

## 当前macOS版本

在当前macOS系统上已经成功生成了以下文件：
- macOS可执行文件：`dist/身份证信息提取工具`
- macOS应用包：`dist/身份证信息提取工具.app`
- 发布包：`release/身份证信息提取工具`

这些可以在macOS系统上直接运行。