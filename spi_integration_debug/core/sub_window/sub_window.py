#!/usr/bin/env python3.13
"""
filename: sub_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-25
description: 子窗口基类，提供所有子窗口的通用功能和接口
"""

from PySide6.QtWidgets import QWidget
from .sub_add_data import SubWindowAddData
from .sub_name import SubWindowName 
from .sub_crc import SubWindowCRC 
from .sub_function_config import SubWindowFunctionConfig

class SubWindow(QWidget):
    """
    子窗口基类，提供所有子窗口的通用功能和接口

    """

    # ========================================
    # UI初始化功能
    # ========================================
    def __init__(self, application):
        """
        初始化子窗口基类
        
        Args:
            application: 主应用程序实例
        """
        super().__init__()
        self.application = application
        self.ui = application.ui

        self.ui.button_function_config.setEnabled(False)

        self.function_config_window_instance = SubWindowFunctionConfig(self.application)

        self.setup_connections()

    # ========================================
    # 信号连接功能
    # ========================================
    def setup_connections(self):
        """
        设置信号槽连接
        """
    #     self.ui.button_add.clicked.connect(self.add_data_window)
    #     self.ui.button_rename.clicked.connect(self.name_window)
        self.ui.button_crc.clicked.connect(self.crc_window)
        self.ui.button_function_config.clicked.connect(self.function_config_window)

    # ========================================
    # 子窗口管理功能
    # ========================================
    def add_data_window(self, callback_function=None):
        """
        打开添加数据窗口
        """
        self.add_data_window_instance = SubWindowAddData(self.application)
        self.add_data_window_instance.data_added.connect(callback_function)
        self.add_data_window_instance.show()

    def name_window(self, callback_function=None, current_name="修改名称"):
        """
        打开项目名称窗口
        """
        self.name_window_instance = SubWindowName(self.application)
        self.name_window_instance.setWindowTitle(current_name)
        self.name_window_instance.name_updated.connect(callback_function)
        self.name_window_instance.show()

    def crc_window(self, callback_function=None):
        """
        打开CRC窗口
        """
        self.crc_window_instance = SubWindowCRC(self.application)
        self.crc_window_instance.crc_updated.connect(self.application.crc_mode_updated)
        self.crc_window_instance.show()

    def function_config_window(self, callback_function=None):
        """
        打开添加数据窗口
        """
        # self.function_config_window_instance.function_config_updated.connect(lambda: print("函数配置更新"))
        self.function_config_window_instance.show()
        print("打开函数配置窗口")