#!/usr/bin/env python3.13
"""
filename: normal_log.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-24
description: 窗口类，负责处理日志显示、保存、清除、导出等操作
"""

import datetime
import yaml
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QMenu
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QAction
from PySide6.QtCore import Qt
from .log_manager import SpecialLog

class LogWindow(QWidget):
    """
    日志窗口类，负责处理日志显示、保存、清除等操作
    """

    def __init__(self, application):
        """
        初始化日志窗口
        
        Args:
            application: 主应用程序实例
        """
        super().__init__()
        # 保存UI界面引用和应用程序实例
        self.ui = application.ui
        self.application = application

        # 初始化日志处理器
        self.special_log = SpecialLog()

        # 设置日志窗口初始可见状态
        self.ui.log_widget.setVisible(True)
        self.log_widget_visible = True

        # self.ui.widget_log.setVisible(True)
        # self.widget_log_visible = True

        self.message_list = self.special_log.message_list

        # self.ui.listWidget_log.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.ui.listWidget_log.customContextMenuRequested.connect(self.show_listWidget_log_menu)

        # self.ui.listWidget_log_normal.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.ui.listWidget_log_normal.customContextMenuRequested.connect(self.show_listWidget_log_normal_menu)

        # 设置信号连接
        self.setup_connect()

        # self.listWidget_log = []

        # self.listWidget_log_normal_list = []

    def setup_connect(self):
        """
        设置按钮信号与槽函数的连接
        """
        # 连接保存日志按钮点击信号
        self.ui.button_save.clicked.connect(self.log_save)

        # 连接清除日志按钮点击信号
        self.ui.button_clear.clicked.connect(self.log_clear)
        
        # 连接折叠日志按钮点击信号
        self.ui.button_fold_log.clicked.connect(self.log_fold)

        # 连接导出PDF按钮点击信号
        self.ui.button_mcu_export_pdf.clicked.connect(self.export_log)

        # self.ui.pushButton_log.clicked.connect(self.widget_log_visible_toggle)

    def widget_log_visible_toggle(self):
        """
        切换日志窗口可见状态
        """
        self.widget_log_visible = not self.widget_log_visible
        if self.widget_log_visible:
            self.ui.widget_log.setVisible(True)
        else:
            self.ui.widget_log.setVisible(False)

    def log(self, message, state=0):
        """
        在日志窗口中记录消息并显示
        
        Args:
            message (str): 要记录的消息内容
            state (int): 消息状态，决定文本颜色
                        0 - 默认黑色（普通消息）
                        1 - 绿色（成功消息）
                        2 - 红色（错误消息）
        """
        # 获取当前时间并格式化为年-月-日 时:分:秒格式
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取日志文本框的光标对象，用于控制文本插入位置和格式
        cursor = self.ui.text_log.textCursor()

        # 检查光标是否在文本末尾，如果不是则移动到末尾
        if not cursor.atEnd():
            cursor.movePosition(QTextCursor.End)

        # 创建时间戳文本格式对象，设置为蓝色字体
        time_format = QTextCharFormat()
        time_format.setForeground(QColor('blue'))
        # 应用时间戳格式并插入时间戳文本
        cursor.setCharFormat(time_format)
        cursor.insertText(f"[{current_time}]:")

        # 根据消息状态创建内容文本格式对象
        content_format = QTextCharFormat()
        if state == 0:
            # 状态0：默认黑色字体
            content_format.setForeground(QColor('black'))
        elif state == 1:
            # 状态1：绿色字体（表示成功）
            content_format.setForeground(QColor('green'))
        elif state == 2:
            # 状态2：红色字体（表示错误）
            content_format.setForeground(QColor('red'))

        # 应用内容格式并插入消息内容和换行符
        cursor.setCharFormat(content_format)
        cursor.insertText(f" {message}\n")

        # print(f"需要发送的消息:{message}")
        
        # 更新文本框的光标位置，确保新消息可见
        self.ui.text_log.setTextCursor(cursor)

        # self.ui.listWidget_log_normal.clear()

        # self.listWidget_log_normal_list.append(f"[{current_time}] {message}")

        # print(f"[{current_time}] {message}")

        # # print(f"当前的消息列表为:{self.listWidget_log_normal_list}")  

        # self.ui.listWidget_log_normal.addItem(f"[{current_time}] {message}")


        # #===============================================================================
        # # 临时新功能

        # file_path = self.application.yaml_window.file_path

        # if not file_path or file_path == "":
        #     return
        
        # comma_count = message.count(",")
        # if comma_count == 0:
        #     return

        # _,data_name , data = message.split(",")

        # # print(f"需要发送的数据为:{data}")

        # data = data.split()

        # # print(f"处理后的数据为:{data}")

        # if data[0] != "40":  # 检查帧头是否为40
        #     return
        
        # address = data[1]  # 地址是第二字节

        # # print(f"地址为:{address}")

        # # print(f"当前的文件路径为:{file_path}")    

        # # 读取选定的YAML文件
        # with open(file_path, 'r', encoding='utf-8') as f:
        #     config = yaml.safe_load(f) or {}

        # # 设置到功能配置窗口中
        # if 'function_config' not in config:
        #     return

        # function_config = config['function_config']
        
        # # 检查地址是否在function_config中
        # config_item = None
        # for item in function_config:
        #     if item['address'] == address:
        #         config_item = item
        #         break
        
        # # 如果地址在配置中且record为"是"，则在listWidget_log中显示
        # if config_item and config_item['record'] == '是':
        #     # 获取功能名称
        #     # function_name = config_item['function']
            
        #     # 检查listWidget_log中是否已有该地址的项
        #     existing_item = None
        #     for i in range(self.ui.listWidget_log.count()):
        #         item = self.ui.listWidget_log.item(i)
        #         if item.text().startswith(f"地址[{address}]:"):
        #             existing_item = item
        #             break
            
        #     # 更新或创建新项
        #     if existing_item:
        #         existing_text = f"地址[{address}]:{data_name} - {current_time}"
        #         self.listWidget_log.append(existing_text)
        #         # 更新现有项
        #         existing_item.setText(existing_text)
        #     else:
        #         # 创建新项
        #         new_item_text = f"地址[{address}]:{data_name} - {current_time}"
        #         self.listWidget_log.append(new_item_text)

        #         insert_index = 0

        #         for i in range(self.ui.listWidget_log.count()):
        #             item = self.ui.listWidget_log.item(i)
        #             item_text = item.text()
        #             # 提取地址部分进行比较
        #             if item_text.startswith("地址[") and "]" in item_text:
        #                 item_address = item_text[3:item_text.find("]")]
        #                 # 比较地址值，找到第一个比当前地址大的项
        #                 if self.compare_addresses(address, item_address) < 0:
        #                     insert_index = i
        #                     break
        #                 else:
        #                     insert_index = i + 1
        #             else:
        #                 insert_index = i + 1
        #          # 在正确位置插入新项
        #         self.ui.listWidget_log.insertItem(insert_index, new_item_text)

    # def compare_addresses(self, addr1, addr2):
    #     """
    #     比较两个地址的大小
        
    #     Args:
    #         addr1 (str): 第一个地址（十六进制字符串）
    #         addr2 (str): 第二个地址（十六进制字符串）
            
    #     Returns:
    #         int(val1 - val2)
    #     """

    #     val1 = int(addr1, 16)  # 将十六进制字符串转换为整数
    #     val2 = int(addr2, 16)
        
    #     return int(val1 - val2)

    def log_fold(self):
        """
        切换日志窗口的显示/隐藏状态
        """
        # 切换日志窗口可见状态
        self.log_widget_visible = not self.log_widget_visible
        if self.log_widget_visible:
            # 显示日志窗口
            self.ui.log_widget.setVisible(True)
        else:
            # 隐藏日志窗口
            self.ui.log_widget.setVisible(False)

    def log_clear(self):
        """
        清除日志内容（带确认提示）
        """
        # 获取当前日志文本内容
        log_text = self.ui.text_log.toPlainText()

        # 只有当日志内容非空时才显示确认对话框
        if log_text:
            # 显示确认对话框询问用户是否清除日志
            reply = QMessageBox.information(
                self, '提示', '是否清除日志？',
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            # 如果用户确认清除，则清空日志文本框
            if reply == QMessageBox.StandardButton.Ok:
                self.ui.text_log.clear()

    def log_save(self):
        """
        保存日志内容到文件
        """
        # 获取日志文本内容
        log_content = self.ui.text_log.toPlainText()

        # 弹出文件保存对话框，让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        # 如果用户选择了保存路径
        if file_path:
            try:
                # 尝试将日志内容写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
            except Exception as e:
                # 如果保存失败，记录错误日志
                self.log(f"保存日志失败：{str(e)}", 2)

    def export_log(self):
        """
        设置日志相关控件的连接.
        """

        # self.message_list = [11]

        # 检查是否有日志消息
        if not self.message_list:
            QMessageBox.information(self.application, "提示", "没有日志内容可导出")
            return
        
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self.application, 
            "导出日志", 
            "log_export", 
            "PDF文件 (*.pdf);;CSV文件 (*.csv)"
        )

        if file_path:
            try:
                if selected_filter == "PDF文件 (*.pdf)" or file_path.endswith(".pdf"):
                    self.special_log.export_pdf(file_path)
                    QMessageBox.information(self.application, "成功", "日志已成功导出到PDF文件")
                else:
                    self.special_log.export_csv(file_path)
                    QMessageBox.information(self.application, "成功", "日志已成功导出到CSV文件")
            except Exception as e:
                QMessageBox.critical(self.application, "错误", f"导出失败：{str(e)}")

    # #===============================================================================
    # # 右键菜单功能
    # #===============================================================================
    # def show_listWidget_log_menu(self, position):
    #     """
    #     显示右键菜单
    #     """

    #     # 创建菜单
    #     menu = self.create_listWidget_log_menu()
    #     # 在鼠标位置显示菜单
    #     menu.exec(self.ui.listWidget_log.viewport().mapToGlobal(position))

    # def create_listWidget_log_menu(self):
    #     """
    #     创建右键菜单
    #     """
    #     menu = QMenu(self)
    #     delete_action = QAction("删除", self)
    #     delete_action.triggered.connect(self.clear_listWidget_log)
    #     menu.addAction(delete_action)

    #     save_action = QAction("保存", self)
    #     save_action.triggered.connect(self.save_listWidget_log)
    #     menu.addAction(save_action)
    #     return menu

    # def clear_listWidget_log(self):
    #     """
    #     清除日志列表内容
    #     """

    #     # 确认清除日志列表内容
    #     reply = QMessageBox.question(
    #         self, 
    #         "确认清除", 
    #         "确定要清除日志列表内容吗？", 
    #         QMessageBox.Yes | QMessageBox.No, 
    #         QMessageBox.No
    #     )
        
    #     if reply == QMessageBox.Yes:
    #         # 清除日志列表内容
    #         self.ui.listWidget_log.clear()
    #         self.listWidget_log = []

    # def save_listWidget_log(self):
    #     """
    #     保存日志列表内容到文件
    #     """
    #     # 获取日志列表内容
    #     log_content = self.listWidget_log

    #     if log_content == []:
    #         QMessageBox.information(self.application, "提示", "没有日志内容可导出")
    #         return
        
    #     log_content = "\n".join(log_content)

    #     # 弹出文件保存对话框，让用户选择保存路径
    #     file_path, _ = QFileDialog.getSaveFileName(
    #         self, "保存日志", "算法发送记录", "文本文件 (*.txt);;所有文件 (*)"
    #     )
    #     # 如果用户选择了保存路径
    #     if file_path:
    #         try:
    #             # 尝试将日志内容写入文件
    #             with open(file_path, 'w', encoding='utf-8') as f:
    #                 f.write(log_content)
    #         except Exception as e:
    #             # 如果保存失败，记录错误日志
    #             self.log(f"保存日志失败：{str(e)}", 2)

    # def show_listWidget_log_normal_menu(self, position):
    #     """
    #     显示listWidget_log_normal的右键菜单
    #     """
    #     # 创建菜单
    #     menu = self.create_listWidget_log_normal_menu()
    #     # 在鼠标位置显示菜单
    #     menu.exec(self.ui.listWidget_log_normal.viewport().mapToGlobal(position))

    # def create_listWidget_log_normal_menu(self):
    #     """
    #     创建listWidget_log_normal的右键菜单
    #     """
    #     menu = QMenu(self)
        
    #     # 添加清除功能
    #     clear_action = QAction("清除", self)
    #     clear_action.triggered.connect(self.clear_listWidget_log_normal)
    #     menu.addAction(clear_action)
        
    #     # 添加保存功能
    #     save_action = QAction("保存", self)
    #     save_action.triggered.connect(self.save_listWidget_log_normal)
    #     menu.addAction(save_action)
        
    #     return menu

    # def clear_listWidget_log_normal(self):
    #     """
    #     清除listWidget_log_normal中的内容
    #     """

    #     # 显示确认对话框询问用户是否清除日志
    #     reply = QMessageBox.information(
    #         self, '提示', '是否清除日志？',
    #         QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
    #     )
    #     # 如果用户确认清除，则清空日志文本框
    #     if reply == QMessageBox.StandardButton.Ok:
    #         self.ui.listWidget_log_normal.clear()
    #         self.listWidget_log_normal_list = []

    # def save_listWidget_log_normal(self):
    #     """
    #     保存listWidget_log_normal中的内容到文件
    #     """
    #     # 获取日志文本内容
    #     log_content = "\n".join(self.listWidget_log_normal_list)

    #     if not log_content:
    #         QMessageBox.information(self, "提示", "没有日志内容可保存")
    #         return

    #     # 弹出文件保存对话框，让用户选择保存路径
    #     file_path, _ = QFileDialog.getSaveFileName(
    #         self, "保存日志", "log_export", "文本文件 (*.txt);;所有文件 (*)"
    #     )
    #     # 如果用户选择了保存路径
    #     if file_path:
    #         try:
    #             # 尝试将日志内容写入文件
    #             with open(file_path, 'w', encoding='utf-8') as f:
    #                 f.write(log_content)
    #         except Exception as e:
    #             # 如果保存失败，记录错误日志
    #             self.log(f"保存日志失败：{str(e)}", 2)

    # #===============================================================================
    # # 日志显示功能
    # #===============================================================================