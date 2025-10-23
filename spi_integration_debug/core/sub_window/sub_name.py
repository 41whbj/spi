#!/usr/bin/env python3.13
"""
filename: sub_name.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-25
description: 项目名称修改子窗口，处理项目名称的修改和更新
"""

from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from core.ui.Ui_sub_add_name import Ui_SubForm_Name

class SubWindowName(QWidget):
    """
    项目名称修改子窗口类，负责处理项目名称的修改和更新
    """
    # 定义名称更新信号，用于通知主窗口项目名称已更改
    name_updated = Signal(str)

    # ========================================
    # UI初始化功能
    # ========================================
    def __init__(self, application, current_name=""):
        """
        初始化项目名称修改子窗口
        
        Args:
            application: 主应用程序实例
            current_name: 当前项目名称
        """
        super().__init__()
        
        # 保存当前项目名称
        self.current_name = current_name
        
        # 保存父窗口引用
        self.application = application

        # 初始化UI界面
        self.ui = Ui_SubForm_Name()
        self.ui.setupUi(self)
        
        # 设置窗口标题
        self.setWindowTitle("修改名称")

        # 连接按钮信号与槽函数
        self.ui.button_name_confirm.clicked.connect(self.on_confirm)
        self.ui.button_name_cancel.clicked.connect(self.close)

    # ========================================
    # 信号处理功能
    # ========================================
    def on_confirm(self):
        """
        确认按钮槽函数
        
        获取用户输入的新名称，验证后发送信号通知主窗口
        """
        # 获取用户输入的新名称并去除首尾空白字符
        new_name = self.ui.line_input.text().strip()
        
        # 验证名称是否为空
        if not new_name:
            QMessageBox.warning(self, "警告", "名称不能为空！")
            return
        
        # 发送名称更新信号到主窗口
        self.name_updated.emit(new_name)

        # 更新数据组列表
        self.application.yaml_window.update_data_group()
        
        # 关闭当前窗口
        self.close()