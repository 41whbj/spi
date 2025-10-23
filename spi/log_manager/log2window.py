#!/usr/bin/env python3.13
"""
filename: log2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-10
description: 日志窗口，处理日志相关的UI连接和逻辑
"""

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox
from .log import CsvManager

class Log2Window(QObject):
    """日志窗口类，负责处理与日志相关的UI连接和业务逻辑."""
    
    def __init__(self, main_window):
        """初始化日志窗口.

        Args:
            main_window: MainWindow实例
        """
        super().__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.csv_manager = CsvManager()
        self.message_list = self.csv_manager.message_list
        self.setup_connections()

    def setup_connections(self):
        """设置日志相关控件的连接."""

        self.ui.button_mcu_export_pdf.clicked.connect(self.export)

    def export(self):
        """设置日志相关控件的连接."""

        # 检查是否有日志消息
        if not self.csv_manager.message_list:
            QMessageBox.information(self.main_window, "提示", "没有日志内容可导出")
            return
        
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self.main_window, 
            "导出日志", 
            "log_export", 
            "PDF文件 (*.pdf);;CSV文件 (*.csv)"
        )

        if file_path:
            try:
                if selected_filter == "PDF文件 (*.pdf)" or file_path.endswith(".pdf"):
                    self.csv_manager.export_pdf(file_path)
                    QMessageBox.information(self.main_window, "成功", "日志已成功导出到PDF文件")
                else:
                    self.csv_manager.export_csv(file_path)
                    QMessageBox.information(self.main_window, "成功", "日志已成功导出到CSV文件")
            except Exception as e:
                QMessageBox.critical(self.main_window, "错误", f"导出失败：{str(e)}")