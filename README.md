# 身份证信息提取工具

## 项目简介

这是一个基于Python开发的身份证信息提取工具，可以批量处理身份证图片，自动识别姓名和民族信息，并将结果导出为Excel文件。

## 功能特点

- ✅ 图形化用户界面，操作简单直观
- ✅ 批量处理身份证图片
- ✅ 自动识别姓名和民族信息
- ✅ 支持多种图片格式（JPG、PNG、BMP、TIFF等）
- ✅ 结果导出为Excel格式
- ✅ 处理进度实时显示
- ✅ 详细的处理日志
- ✅ 一键打包为Windows可执行文件

## 技术架构

```
身份证信息提取工具/
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── gui/               # 图形界面模块
│   │   ├── main_window.py # 主窗口
│   │   └── __init__.py
│   ├── ocr/               # OCR识别模块
│   │   ├── preprocessor.py # 图像预处理
│   │   ├── recognizer.py   # OCR识别器
│   │   └── __init__.py
│   ├── utils/             # 工具模块
│   │   ├── file_handler.py # 文件处理
│   │   ├── excel_writer.py # Excel导出
│   │   └── __init__.py
│   └── config/            # 配置模块
│       ├── settings.py    # 配置文件
│       └── __init__.py
├── requirements.txt       # Python依赖包
├── build.py              # 打包脚本
└── README.md             # 项目说明
```

## 安装与运行

### 环境要求

- Python 3.8+
- Tesseract OCR引擎

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd idcard
   ```

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **安装Tesseract OCR**
   
   **Windows系统：**
   - 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
   - 安装到默认路径（通常是 C:\\Program Files\\Tesseract-OCR\\）
   - 下载中文语言包：https://github.com/tesseract-ocr/tessdata
   - 将chi_sim.traineddata放到Tesseract安装目录下的tessdata文件夹

   **macOS系统：**
   ```bash
   brew install tesseract
   brew install tesseract-lang
   ```

   **Linux系统：**
   ```bash
   sudo apt-get install tesseract-ocr
   sudo apt-get install tesseract-ocr-chi-sim
   ```

4. **运行程序**
   ```bash
   python src/main.py
   ```

## 打包为可执行文件

使用提供的打包脚本可以将程序打包为Windows可执行文件：

```bash
python build.py
```

打包完成后，可执行文件将生成在 `dist/` 目录中，发布包将在 `release/` 目录中。

## 使用说明

1. **启动程序**：双击运行可执行文件或使用Python运行源码
2. **选择图片文件夹**：点击"浏览"按钮选择包含身份证图片的文件夹
3. **设置输出文件**：选择Excel结果文件的保存位置
4. **开始处理**：点击"开始处理"按钮开始批量识别
5. **查看结果**：处理完成后打开生成的Excel文件查看识别结果

## 技术细节

### 图像预处理

- 自动调整图片大小以提高处理速度
- 增强对比度和去噪处理
- 身份证区域检测和透视变换矫正
- 文字区域定位和优化

### OCR识别

- 使用Tesseract OCR引擎
- 支持中文字符识别
- 基于身份证标准格式的区域定位
- 智能文本清理和验证

### 结果处理

- Excel格式化输出
- 识别成功率统计
- 详细的错误日志
- 支持大批量文件处理

## 配置选项

可以通过修改 `src/config/settings.py` 文件来调整程序参数：

- 支持的图片格式
- OCR识别参数
- 身份证信息区域坐标
- Excel输出格式
- 界面尺寸设置

## 常见问题

### Q: 识别准确率不高怎么办？
A: 
- 确保身份证图片清晰，避免模糊、反光
- 图片中身份证应该占据大部分区域
- 避免倾斜和扭曲的图片
- 可以尝试调整图片的对比度和亮度

### Q: 程序运行出错怎么办？
A:
- 检查是否正确安装了Tesseract OCR
- 确保Python依赖包已正确安装
- 查看程序日志窗口中的错误信息
- 检查图片文件是否损坏或格式不支持

### Q: 如何提高处理速度？
A:
- 使用较小尺寸的图片（建议宽度不超过1200像素）
- 确保图片格式为JPG或PNG
- 关闭其他占用CPU的程序

## 开发说明

### 添加新功能

1. 在相应模块下创建新文件
2. 在主界面中添加对应的UI控件
3. 更新配置文件
4. 测试功能完整性

### 代码规范

- 使用UTF-8编码
- 遵循PEP 8代码规范
- 添加必要的注释和文档字符串
- 进行充分的错误处理

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 版本历史

- v1.0.0：初始版本，支持基本的身份证信息提取功能

## 技术支持

如有问题或建议，请联系开发团队。