#!/usr/bin/env python3.13
"""
filename: application.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-22
description: 
"""

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from .ui.Ui_application import Ui_Application
from spi.spi_window import SPIWindow
from spi.spi_controller import SPIController
from spi.spi_driver import SPIDriver
from utils.yaml.yaml_window import YAMLWindow
from utils.yaml.yaml_template import YAMLTemplate
from .sub_window.sub_window import SubWindow
from .log.log_window import LogWindow
from .integration_debug.data_group_window import DataGroupWindow
from .integration_debug.test_group_window import TestGroupWindow
from utils.crc.crc_manager import CRC

class Applicaton(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Application()
        self.ui.setupUi(self)
        self.driver = SPIDriver()

        self.start = False

        self.yaml_template = YAMLTemplate()

        # self.init_template()

        # 初始化当前CRC模式为0 (默认使用CRC)
        self.current_crc_mode = 0

        # 初始化日志窗口
        self.log_window = LogWindow(self)

        # 初始化SPI窗口
        self.spi_controller = SPIController(self, self.driver)
        self.spi_controller.log_signal.connect(self.log_window.log)
        self.spi_window = SPIWindow(self, self.driver)

        # 初始化测试组窗口
        self.test_group_window = TestGroupWindow(self, self.spi_controller)
        
        # 初始化YAML窗口
        self.yaml_window = YAMLWindow(self)

        # 初始化子窗口
        self.sub_window = SubWindow(self)

        # 初始化数据组窗口
        self.data_group_window = DataGroupWindow(self, self.sub_window)

        self.start_tip()

    def start_tip(self):

        def show_startup_tip(self):
            """
            程序启动时,提示用户先建立或导入文件
            """
            
            # 显示提示信息，告知用户需要先建立或导入项目文件
            QMessageBox.information(
                self, 
                "提示", 
                "欢迎使用本程序！\n进行调试前，请先新建或导入项目文件。"
            )

        QTimer.singleShot(0, lambda: show_startup_tip(self))

        self.start = True
    def closeEvent(self, event):
        """
        处理窗口关闭事件，在关闭前提示用户确认
        
        Args:
            event: 关闭事件对象
        """

        # 关闭确认
        reply = QMessageBox.question(
            self, 
            '关闭确认', 
            '请确认是否关闭',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 用户确认关闭，接受关闭事件
            event.accept()
        elif reply == QMessageBox.StandardButton.No:
            # 用户取消关闭，忽略关闭事件
            event.ignore()

    def crc_mode_updated(self, crc_value):
        """
        接收CRC窗口更新信号，更新current_crc_mode
        
        Args:
            crc_value: 新的CRC值
        """
        self.current_crc_mode = crc_value

        if crc_value == 0:
            self.log_window.log("CRC-16(自定义)校验已启用", 1)
        elif crc_value == -1:
            self.log_window.log("CRC-16(自定义)校验已关闭", 1)
        
        self.update_all_crc_tooltips()

    def update_all_crc_tooltips(self):
        """
        更新所有数据项的CRC工具提示
        
        遍历所有数据项，根据当前CRC模式计算CRC值并更新工具提示显示。
        包括数据列表中的项目和组列表中的项目。
        """

        # 获取数据组管理器中的所有数据项
        list_data_items = self.data_group_window.data_group_manager.get_list_data_items()

        # 遍历所有数据项并更新其CRC工具提示
        for item in list_data_items:

            # 获取项目关联的数据元组
            data_tuple = item.data(Qt.UserRole)

            # 提取数据文本（第二个元素）
            _, data_text = data_tuple

            # 为该项目设置CRC工具提示
            self.set_item_crc_tooltip(item, data_text)

    def set_item_crc_tooltip(self, item, data_text):
        """
        为单个项目设置CRC工具提示
        
        根据当前CRC模式计算数据的CRC值，并将结果作为工具提示显示在项目上
        
        Args:
            item (QListWidgetItem): 需要设置工具提示的列表项
            data_text (str): 项目关联的数据文本，格式为十六进制字符串（如："AA BB CC"）
        """

        # 检查当前CRC模式是否为启用状态（0表示启用）
        if self.current_crc_mode == 0:

            # 将数据文本按空格分割并去除首尾空白字符
            hex_parts = data_text.strip().split()

            # 将十六进制字符串转换为整数字节列表
            data_bytes = [int(part, 16) for part in hex_parts]

            # 计算数据的CRC值
            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF

            # 将CRC值附加到原始数据文本后形成新的数据文本
            crc_data_text = data_text + f" {crc_high:02X} {crc_low:02X}"

            # 将带CRC的数据文本设置为项目的工具提示
            item.setToolTip(f"校验后数据：{crc_data_text}")
        else:

            # 如果CRC模式未启用，则清除项目的工具提示
            item.setToolTip(None)

        


    