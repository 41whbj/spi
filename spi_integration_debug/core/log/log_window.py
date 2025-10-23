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
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

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


        self.ui.widget_log.setVisible(True)
        self.widget_log_visible = True

        self.ui.listWidget_log.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_log.customContextMenuRequested.connect(self.show_listWidget_log_menu)

        self.ui.listWidget_log_normal.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_log_normal.customContextMenuRequested.connect(self.show_listWidget_log_normal_menu)

        # 设置信号连接
        self.setup_connect()

        self.listWidget_log = []

        self.listWidget_log_normal_list = []

    def setup_connect(self):
        """
        设置按钮信号与槽函数的连接
        """

        self.ui.pushButton_log.clicked.connect(self.widget_log_visible_toggle)

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
        """
        # 获取当前时间并格式化为年-月-日 时:分:秒格式
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.listWidget_log_normal_list.append(f"[{current_time}] {message}")

        # print(f"[{current_time}] {message}")

        # print(f"当前的消息列表为:{self.listWidget_log_normal_list}")  

        self.ui.listWidget_log_normal.clear()

        self.ui.listWidget_log_normal.addItem(f"[{current_time}] {message}")

        self.log_to_listWidget_log(message,current_time)

    def log_to_listWidget_log(self, message,current_time):
        """
        根据YAML文件配置，选则对应的消息记录到listWidget_log中
        Args:
            message (str): 要记录的消息内容
        """

        file_path = self.application.yaml_window.file_path

        if not file_path or file_path == "":
            return
        
        comma_count = message.count(",")
        if comma_count == 0 :
            return

        try:
            _, data_name, data = message.split(",")
        except ValueError:
            # 如果消息格式不符合预期，直接返回
            return

        data = data.split()

        if data[0] != "40":  # 检查帧头是否为40
            return
        
        address = data[1]  # 地址是第二字节 

        # 读取选定的YAML文件
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # 设置到功能配置窗口中
        if 'function_config' not in config:
            return

        function_config = config['function_config']
        
        # 检查地址是否在function_config中
        config_item = None
        for item in function_config:
            if item['address'] == address:
                config_item = item
                break
        
        # 如果地址在配置中且record为"是"，则在listWidget_log中显示
        if config_item and config_item['record'] == '是':
            
            # 检查listWidget_log中是否已有该地址的项
            existing_item = None
            for i in range(self.ui.listWidget_log.count()):
                item = self.ui.listWidget_log.item(i)
                if item.text().startswith(f"地址[{address}]:"):
                    existing_item = item
                    break
            
            # 更新或创建新项
            if existing_item:
                existing_text = f"地址[{address}]:{data_name} - {current_time}"
                self.listWidget_log.append(existing_text)
                # 更新现有项
                existing_item.setText(existing_text)
            else:
                # 创建新项
                new_item_text = f"地址[{address}]:{data_name} - {current_time}"
                self.listWidget_log.append(new_item_text)

                insert_index = 0

                for i in range(self.ui.listWidget_log.count()):
                    item = self.ui.listWidget_log.item(i)
                    item_text = item.text()
                    # 提取地址部分进行比较
                    if item_text.startswith("地址[") and "]" in item_text:
                        item_address = item_text[3:item_text.find("]")]
                        # 比较地址值，找到第一个比当前地址大的项
                        if self.compare_addresses(address, item_address) < 0:
                            insert_index = i
                            break
                        else:
                            insert_index = i + 1
                    else:
                        insert_index = i + 1
                 # 在正确位置插入新项
                self.ui.listWidget_log.insertItem(insert_index, new_item_text)

    def compare_addresses(self, addr1, addr2):
        """
        比较两个地址的大小
        
        Args:
            addr1 (str): 第一个地址（十六进制字符串）
            addr2 (str): 第二个地址（十六进制字符串）
            
        Returns:
            int(val1 - val2)
        """

        val1 = int(addr1, 16)  # 将十六进制字符串转换为整数
        val2 = int(addr2, 16)
        
        return int(val1 - val2)

    #===============================================================================
    # 右键菜单功能
    #===============================================================================
    def show_listWidget_log_menu(self, position):
        """
        显示右键菜单
        """

        # 创建菜单
        menu = self.create_listWidget_log_menu()
        # 在鼠标位置显示菜单
        menu.exec(self.ui.listWidget_log.viewport().mapToGlobal(position))

    def create_listWidget_log_menu(self):
        """
        创建右键菜单
        """
        menu = QMenu(self)
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self.clear_listWidget_log)
        menu.addAction(delete_action)

        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_listWidget_log)
        menu.addAction(save_action)
        return menu

    def clear_listWidget_log(self):
        """
        清除日志列表内容
        """

        # 确认清除日志列表内容
        reply = QMessageBox.question(
            self, 
            "确认清除", 
            "确定要清除日志列表内容吗？", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 清除日志列表内容
            self.ui.listWidget_log.clear()
            self.listWidget_log = []

    def save_listWidget_log(self):
        """
        保存日志列表内容到文件
        """
        # 获取日志列表内容
        log_content = self.listWidget_log

        if log_content == []:
            QMessageBox.information(self.application, "提示", "没有日志内容可导出")
            return
        
        log_content = "\n".join(log_content)

        # 弹出文件保存对话框，让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "算法发送记录", "文本文件 (*.txt);;所有文件 (*)"
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

    def show_listWidget_log_normal_menu(self, position):
        """
        显示listWidget_log_normal的右键菜单
        """
        # 创建菜单
        menu = self.create_listWidget_log_normal_menu()
        # 在鼠标位置显示菜单
        menu.exec(self.ui.listWidget_log_normal.viewport().mapToGlobal(position))

    def create_listWidget_log_normal_menu(self):
        """
        创建listWidget_log_normal的右键菜单
        """
        menu = QMenu(self)
        
        # 添加清除功能
        clear_action = QAction("清除", self)
        clear_action.triggered.connect(self.clear_listWidget_log_normal)
        menu.addAction(clear_action)
        
        # 添加保存功能
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_listWidget_log_normal)
        menu.addAction(save_action)
        
        return menu

    def clear_listWidget_log_normal(self):
        """
        清除listWidget_log_normal中的内容
        """

        # 显示确认对话框询问用户是否清除日志
        reply = QMessageBox.information(
            self, '提示', '是否清除日志？',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        # 如果用户确认清除，则清空日志文本框
        if reply == QMessageBox.StandardButton.Ok:
            self.ui.listWidget_log_normal.clear()
            self.listWidget_log_normal_list = []

    def save_listWidget_log_normal(self):
        """
        保存listWidget_log_normal中的内容到文件
        """
        # 获取日志文本内容
        log_content = "\n".join(self.listWidget_log_normal_list)

        if not log_content:
            QMessageBox.information(self, "提示", "没有日志内容可保存")
            return

        # 弹出文件保存对话框，让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "log_export", "文本文件 (*.txt);;所有文件 (*)"
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