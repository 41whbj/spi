#!/usr/bin/env python3.13
"""
filename: data_group_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-07
description: 数据组管理器，和主程序界面交互
"""

from PySide6.QtCore import QObject
from .data_group_manager import DataGroupManager

class DataGroupWindow(QObject):
    """
    数据组窗口类，和主程序界面交互
    """

    def __init__(self, application,sub_window):
        """
        初始化数据组窗口
        
        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.sub_window = sub_window

        self.data_group_manager = DataGroupManager(application,sub_window)

        self.setup_connections()

        # 启动数据组列表的拖拽功能
        self.data_group_manager.setup_list_data_drag_drop()

    #===============================================================================
    # 信号槽连接功能
    #===============================================================================

    def setup_connections(self):
        """
        设置信号槽连接
        """
        # 数据组管理相关连接
        self.ui.combo_box_data_group.currentIndexChanged.connect(self.data_group_manager.group_changed)
        self.ui.button_add_data_group.clicked.connect(self.data_group_manager.add_data_group)
        self.ui.button_del_data_group.clicked.connect(self.data_group_manager.delete_data_group)
        self.ui.button_rename.clicked.connect(self.data_group_manager.handle_rename_button)

        # 发送数据连接
        self.ui.button_send.clicked.connect(self.send_line_data)

        # 数据项管理相关连接
        self.ui.button_add.clicked.connect(
            lambda: self.sub_window.add_data_window(
                self.data_group_manager.add_data_widget
            )
        )
        self.ui.button_det.clicked.connect(self.data_group_manager.remove_selected_items)

    #===============================================================================
    # 数据发送功能
    #===============================================================================

    def send_line_data(self):
        """
        发送输入框内的数据
        """

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 获取输入框内的数据
        data = self.ui.line_data.text()

        # 发送数据
        self.application.spi_controller.spi_send(data, self.clk_mode ,self.bit_order)