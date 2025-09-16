# -*- coding: utf-8 -*-
"""
主界面窗口
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

# 修复PyInstaller打包后的导入问题
try:
    from ..config.settings import *
    from ..utils.file_handler import FileHandler
    from ..ocr.recognizer import IDCardRecognizer
    from ..utils.excel_writer import ExcelWriter
except ImportError:
    # 备选导入方式
    try:
        from src.config.settings import *
        from src.utils.file_handler import FileHandler
        from src.ocr.recognizer import IDCardRecognizer
        from src.utils.excel_writer import ExcelWriter
    except ImportError:
        # 最后的备选方式
        import importlib.util
        
        # 动态导入配置
        config_spec = importlib.util.find_spec("config.settings")
        if config_spec is None:
            # 手动查找并添加路径
            current_dir = os.path.dirname(__file__)
            parent_dir = os.path.dirname(current_dir)
            sys.path.insert(0, parent_dir)
        
        from config.settings import *
        from utils.file_handler import FileHandler
        from ocr.recognizer import IDCardRecognizer
        from utils.excel_writer import ExcelWriter


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.file_handler = FileHandler()
        self.recognizer = IDCardRecognizer()
        self.excel_writer = ExcelWriter()
        self.processing = False
        
    def setup_window(self):
        """设置窗口基本属性"""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # 居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text=APP_NAME, font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件夹选择
        ttk.Label(main_frame, text="选择图片文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, state='readonly')
        self.folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="浏览", command=self.select_folder).grid(row=1, column=2, pady=5)
        
        # 输出文件选择
        ttk.Label(main_frame, text="输出Excel文件:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_var, state='readonly')
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="保存为", command=self.select_output_file).grid(row=2, column=2, pady=5)
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="开始处理", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止处理", command=self.stop_processing, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        # 日志文本框
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        main_frame.rowconfigure(6, weight=1)
        
    def select_folder(self):
        """选择图片文件夹"""
        folder = filedialog.askdirectory(title="选择包含身份证图片的文件夹")
        if folder:
            self.folder_var.set(folder)
            self.log(f"已选择文件夹: {folder}")
            
            # 自动设置输出文件名
            if not self.output_var.get():
                default_output = os.path.join(folder, "身份证信息提取结果.xlsx")
                self.output_var.set(default_output)
                
    def select_output_file(self):
        """选择输出Excel文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存Excel文件",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if file_path:
            self.output_var.set(file_path)
            self.log(f"输出文件: {file_path}")
            
    def log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, status):
        """更新状态"""
        self.status_var.set(status)
        self.root.update_idletasks()
        
    def update_progress(self, current, total):
        """更新进度条"""
        if total > 0:
            progress = (current / total) * 100
            self.progress_var.set(progress)
        else:
            self.progress_var.set(0)
        self.root.update_idletasks()
        
    def start_processing(self):
        """开始处理"""
        if not self.folder_var.get():
            messagebox.showerror("错误", "请先选择图片文件夹！")
            return
            
        if not self.output_var.get():
            messagebox.showerror("错误", "请先选择输出文件！")
            return
            
        self.processing = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()
        
    def stop_processing(self):
        """停止处理"""
        self.processing = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.update_status("已停止")
        self.log("处理已停止")
        
    def process_images(self):
        """处理图片的主要逻辑"""
        try:
            folder = self.folder_var.get()
            output_file = self.output_var.get()
            
            self.log("开始扫描图片文件...")
            self.update_status("扫描图片文件...")
            
            # 获取所有图片文件
            image_files = self.file_handler.get_image_files(folder)
            if not image_files:
                self.log("未找到任何图片文件！")
                self.processing = False
                self.start_button.config(state='normal')
                self.stop_button.config(state='disabled')
                return
                
            self.log(f"找到 {len(image_files)} 个图片文件")
            
            # 处理结果列表
            results = []
            
            # 处理每个图片文件
            for i, image_path in enumerate(image_files):
                if not self.processing:
                    break
                    
                self.update_progress(i, len(image_files))
                self.update_status(f"处理中... ({i+1}/{len(image_files)})")
                
                filename = os.path.basename(image_path)
                self.log(f"处理文件: {filename}")
                
                try:
                    # 记录处理开始
                    self.log(f"  正在处理: {os.path.basename(image_path)}")
                    self.log(f"  完整路径: {image_path}")
                    
                    # 检查文件是否存在
                    if not os.path.exists(image_path):
                        raise FileNotFoundError(f"File not found: {image_path}")
                    
                    # OCR识别
                    result = self.recognizer.recognize(image_path)
                    
                    if result['success']:
                        name = result.get('name', '')
                        ethnicity = result.get('ethnicity', '')
                        status = "成功"
                        note = ""
                        self.log(f"  ✅ 识别成功 - 姓名: {name}, 民族: {ethnicity}")
                    else:
                        name = ""
                        ethnicity = ""
                        status = "失败"
                        note = result.get('error', '识别失败')
                        self.log(f"  ❌ 识别失败: {note}")
                        
                    results.append({
                        'filename': filename,
                        'name': name,
                        'ethnicity': ethnicity,
                        'status': status,
                        'note': note
                    })
                    
                except FileNotFoundError as fnf_error:
                    error_msg = f"文件未找到: {str(fnf_error)}"
                    self.log(f"  ❌ {error_msg}")
                    results.append({
                        'filename': filename,
                        'name': "",
                        'ethnicity': "",
                        'status': "文件不存在",
                        'note': error_msg
                    })
                    
                except Exception as e:
                    error_msg = f"处理异常: {str(e)}"
                    self.log(f"  ❌ {error_msg}")
                    # 记录更详细的错误信息用于调试
                    import traceback
                    self.log(f"  详细错误: {traceback.format_exc()}")
                    
                    results.append({
                        'filename': filename,
                        'name': "",
                        'ethnicity': "",
                        'status': "处理错误",
                        'note': error_msg
                    })
                    
            if self.processing:
                # 生成Excel文件
                self.update_status("生成Excel文件...")
                self.log("生成Excel文件...")
                
                try:
                    self.excel_writer.write_results(results, output_file)
                    self.log(f"Excel文件已保存: {output_file}")
                    self.update_status("处理完成")
                    self.update_progress(len(image_files), len(image_files))
                    
                    # 显示完成对话框
                    success_count = sum(1 for r in results if r['status'] == '成功')
                    messagebox.showinfo("处理完成", 
                                      f"处理完成！\n"
                                      f"总文件数: {len(results)}\n"
                                      f"成功识别: {success_count}\n"
                                      f"失败数量: {len(results) - success_count}\n"
                                      f"结果已保存到: {output_file}")
                                      
                except Exception as e:
                    self.log(f"保存Excel文件时出错: {str(e)}")
                    messagebox.showerror("错误", f"保存Excel文件时出错: {str(e)}")
                    
        except Exception as e:
            self.log(f"处理过程中出现错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中出现错误: {str(e)}")
            
        finally:
            self.processing = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            
    def run(self):
        """运行主窗口"""
        self.root.mainloop()