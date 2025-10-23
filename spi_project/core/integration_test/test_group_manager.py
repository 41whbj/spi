#!/usr/bin/env python3.13
"""
filename: test_group_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-29
description: 测试数据组管理器，用于处理测试数据组操作
"""

from PySide6.QtWidgets import (
    QMessageBox, QListWidgetItem, QComboBox, QTreeWidgetItem,
    QAbstractItemView
)
from PySide6.QtCore import QThread, Signal, QElapsedTimer, Qt
import random
from .data_widget import Data_Widget

class SendModeThread(QThread):
    """
    数据发送工作线程类
    
    该类继承自QThread，提供了多线程的数据发送功能，支持多种发送模式。
    通过信号机制与UI线程通信，报告发送状态和日志信息。
    
    Signals:
        log_signal (str, int): 发送日志信息信号，参数为日志内容和日志级别
        finished_signal (): 线程完成信号
        progress_signal (str): 进度更新信号
    """
    
    log_signal = Signal(str, int)
    finished_signal = Signal()
    progress_signal = Signal(str)

    def __init__(self, application,spi_controller):
        """
        初始化SendModeThread实例
        
        Args:
            application: 主应用程序实例
        """
        super().__init__()
        self.application = application
        self.ui = self.application.ui
        self.spi_controller = spi_controller
        self.running = False
        # self.delay = 0
        # self.items = []
        # self.mode = "order"

        # self.times = 1

        self.num = 0

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

    def set_params(self, delay, items, mode, cycles='', times=1, data_poll=False):
        """
        设置发送参数
        
        Args:
            delay (float): 发送间隔延迟（秒）
            items (list): 要发送的数据项列表
            mode (str): 发送模式 ("order", "circ", "random")
            cycles (int/str): 循环次数，仅在循环模式下使用
            times (int): 随机发送次数，仅在随机模式下使用
            data_poll (bool): 是否轮询发送数据组
        """
        self.delay = delay
        self.items = items
        self.mode = mode
        self.cycles = cycles
        self.times = times
        self.data_poll = data_poll

    def delay_fuction(self, seconds):
        """
        延迟函数
        
        提供高精度的延迟控制，确保发送间隔的准确性。
        
        Args:
            seconds (float): 延迟时间（秒）
        """
        timer = QElapsedTimer()
        timer.start()

        target_ms = int(seconds * 1000)

        while self.running and timer.elapsed() < target_ms:
            remaining = target_ms - timer.elapsed()

            if remaining > 10:
                self.msleep(10)
            elif remaining > 1:
                self.msleep(1)

    def send_orderly(self):
        """
        顺序发送数据
        
        根据data_poll参数决定是发送数据组还是轮询发送数据。
        """
        if self.data_poll is False:
            self.send_group(self.items)
        else:
            self.send_poll(self.items)

    def send_cyclic(self):
        """
        循环发送数据
        
        支持指定循环次数或持续发送直到手动停止。
        在每次循环之间插入用户设定的延迟。
        """

        # 当未指定循环次数时，持续发送直到手动停止
        if not self.cycles:
            cycle_count = 0

            while self.running:
                cycle_count += 1
                # 先执行发送操作
                if self.data_poll is False:
                    self.send_group(self.items)
                else:
                    self.send_poll(self.items, cyclic_mode=True)
                    self.delay_fuction(self.delay)
                
                # 发送完成后再记录进度
                self.progress_signal.emit(f"持续发送中，循环第{cycle_count}次")
            return
        
        # 指定循环次数的发送
        for i in range(self.cycles):
            if not self.running:
                break
                
            # 先执行发送操作
            if self.data_poll is False:
                self.send_group(self.items)
            else:
                self.send_poll(self.items, cyclic_mode=True)
                if i < (self.cycles - 1) and self.delay > 0:
                    self.delay_fuction(self.delay)
            
            # 发送完成后再记录进度
            self.progress_signal.emit(f"循环:{i+1}/{self.cycles}")

    def send_randomly(self):
        """
        随机发送数据
        
        随机选择数据项进行发送，发送次数由times参数确定。
        每次发送后根据设定的延迟进行等待。
        """

        if not self.times:
            count = 0
            while self.running:
                count += 1
                
                op_timer = QElapsedTimer()
                op_timer.start()
            
                # 随机选择一个数据项
                group = random.choice(self.items)
                if isinstance(group, (list, tuple)) and len(group) > 0:
                    if isinstance(group[0], (list, tuple)) and len(group[0]) >= 2:
                        item = random.choice(group)
                else:
                    item = group

                self.send_item_data(item)
                
                # 发送进度提示
                self.progress_signal.emit(f"持续随机发送中，已发送{count}次")
            
                if self.delay > 0:
                    op_time = op_timer.elapsed() / 1000.0
                    actual_delay = max(0, self.delay - op_time)
                    self.delay_fuction(actual_delay)
        else:
            for _ in range(self.times):
                if not self.running:
                    break
                
                op_timer = QElapsedTimer()
                op_timer.start()
            
                # 随机选择一个数据项
                group = random.choice(self.items)
                if isinstance(group, (list, tuple)) and len(group) > 0:
                    if isinstance(group[0], (list, tuple)) and len(group[0]) >= 2:
                        item = random.choice(group)
                else:
                    item = group

                self.send_item_data(item)
            
                if self.delay > 0:
                    op_time = op_timer.elapsed() / 1000.0
                    actual_delay = max(0, self.delay - op_time)
                    self.delay_fuction(actual_delay)

    def send_poll(self, items, cyclic_mode=False):
        """
        轮询发送数据组
        
        按顺序发送每个数据组内的所有数据项，在组内数据项之间使用固定延迟，
        在数据组之间使用用户设定的延迟。
        
        Args:
            items (list): 数据组列表
            cyclic_mode (bool): 是否处于循环模式
        """
        # 发送所有数据组，用户延迟控制组间发送间隔
        for i, item in enumerate(items):
            if not self.running:
                break

            op_timer = QElapsedTimer()
            op_timer.start()

            self.send_item_data(item)

            # 数据项之间使用固定0.01秒(10ms)延迟
            if i < (len(items) - 1):
                op_time = op_timer.elapsed() / 1000.0
                # 每个项之间有0.01秒延迟
                actual_delay = max(0, 0.01 - op_time)
                self.delay_fuction(actual_delay)

        # 如果是循环模式，发送进度提示
        if cyclic_mode is True:
            self.progress_signal.emit("发送下一组数据")

    def send_group(self, items):
        """
        发送数据组
        
        按列表顺序发送数据组，用户延迟控制数据发送间隔。
        
        Args:
            items (list): 要发送的数据项列表
        """
        for item in items:
            if not self.running:
                break

            op_timer = QElapsedTimer()
            op_timer.start()

            self.send_item_data(item)

            # print(f"延迟: {self.delay}")

            # 使用用户设定的延迟控制发送间隔
            if self.delay > 0:
                op_time = op_timer.elapsed() / 1000.0
                actual_delay = max(0, self.delay - op_time)
                self.delay_fuction(actual_delay)

    def run(self):
        """
        线程执行入口
        
        根据设定的模式执行相应的发送操作。
        """
        self.running = True

        if self.mode == "order":
            self.send_orderly()
        elif self.mode == "circ":
            self.send_cyclic()
        elif self.mode == "random":
            self.send_randomly()

        self.running = False
        self.finished_signal.emit()

    def stop(self):
        """
        停止发送任务
        """
        self.running = False

    

    def send_item_data(self, item):
        """
        发送单个数据项
        
        处理数据项的发送过程，包括CRC校验、设备检查和实际发送。
        
        Args:
            item: 要发送的数据项
        """
        if self.running is False:
            return

        data_tuple = item.data(Qt.UserRole)

        _, data = data_tuple

        print(self.clk_mode, self.bit_order)

        self.spi_controller.spi_send(data,self.clk_mode,self.bit_order)

class TestGroupManager:
    """
    测试组管理器类
    
    该类负责管理测试数据组的创建、删除、重命名、加载和保存等功能。
    """
    
    def __init__(self,application):
        """
        初始化TestGroupManager实例
        
        Args:
            application: 应用实例引用
        """
        self.application = application
        self.ui = self.application.ui

        # 存储所有测试组数据的字典，键为组名，值为数据项列表
        self.test_group_data = {}

        # 当前选中的测试组名称  
        self.current_group = None

         # 用于生成新组名的计数器
        self.group_count = 0 

        self.init_widget()

    def init_widget(self):
        """
        初始化界面组件
        """

        # 设置列表控件为2列，分别为组名和数据
        self.ui.list_group.setColumnCount(1)
        self.ui.list_group.setHeaderLabels(["测试组"])

        # 在初始化时设置行高
        self.ui.list_group.setUniformRowHeights(True)
        # 或者设置固定行高
        self.ui.list_group.setStyleSheet("QTreeWidget::item { height: 25px; }")

        # 设置拖拽模式为内部移动
        self.ui.list_group.setDragDropMode(QAbstractItemView.InternalMove)
        # 设置选择模式为单选
        self.ui.list_group.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置选择行为为选择整行
        self.ui.list_group.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 禁用拖拽覆盖模式
        self.ui.list_group.setDragDropOverwriteMode(False)

        # 关键设置：允许放置到item上而不是仅在item之间
        # self.ui.list_group.setDragDropOverwriteMode(False)
        # self.ui.list_group.setSelectionMode(QAbstractItemView.SingleSelection)

        # # 设置组合框为可编辑状态，允许用户自定义组名
        # self.ui.combo_box_mode_group.setEditable(True)
        # # 设置插入策略为不自动插入，防止重复添加
        # self.ui.combo_box_mode_group.setInsertPolicy(QComboBox.NoInsert)

        # # 设置组合框行编辑器为可写状态
        # self.ui.combo_box_mode_group.lineEdit().setReadOnly(False)
        # # 连接行编辑器的编辑完成信号，用于处理组名修改
        # self.ui.combo_box_mode_group.lineEdit().editingFinished.connect(self.mode_group_name_changed)

        # # 设置列表控件的拖放模式为同时支持内部移动和外部拖放
        # self.ui.list_group.setDragDropMode(QListWidget.DragDrop)

        # # 连接列表模型的行插入信号，用于处理拖放添加数据项
        # self.ui.list_group.model().rowsInserted.connect(self.mode_group_insert)

        # # 设置默认拖放动作为移动操作
        # self.ui.list_group.setDefaultDropAction(Qt.MoveAction)
        
        # # 启用拖拽
        # self.ui.list_group.setDragEnabled(True)

        # # 允许接受拖放操作
        # self.ui.list_group.setAcceptDrops(True)

        # # 显示拖放指示器
        # self.ui.list_group.setDropIndicatorShown(True)

        # # 连接模型的行移动信号，用于在拖拽完成后更新内部数据结构
        # self.ui.list_group.model().rowsMoved.connect(self.list_group_rows_moved)

        # # 添加默认的模式组
        # self.add_mode_group()

    def list_group_rows_moved(self, source_parent, source_start, source_end, destination_parent, destination_row):
        """
        处理测试组列表行移动事件，更新内部数据结构以反映新的顺序
        """
        # 获取当前组名
        current_group_name = self.ui.combo_box_mode_group.currentText()
        
        # 重新构建组数据以匹配UI中的新顺序
        new_group_data = []
        for i in range(self.ui.list_group.count()):
            item = self.ui.list_group.item(i)
            if item and item.data(Qt.UserRole):
                new_group_data.append(item.data(Qt.UserRole))
        
        # 更新内部数据结构
        self.test_group_data[current_group_name] = new_group_data

        self.application.yaml_window.update_test_group()

    def add_mode_group(self):
        # """
        # 添加新的测试组
        
        # 创建一个新的测试组，为其生成唯一的名称，并将其添加到下拉框和内部数据结构中。
        # 同时更新当前测试组。
        # """

        # 增加组名计数器，确保新组名唯一
        self.group_count += 1

        new_group_name = f"新建分组{self.group_count}"

        # # print(f"group_count: {self.group_count}")
        
        self.test_group_data[new_group_name] = []

        # 设置新组为当前组
        self.current_group = new_group_name

        item = QTreeWidgetItem([new_group_name])

        # 为item添加勾选框
        item.setCheckState(0,Qt.Checked)

        # 设置项为可编辑状态,不允许作为放置目标（防止子item嵌套）
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | 
                     Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled)

        # 设置item为选中状态
        item.setSelected(True)

        # 确保选中的item可见
        self.ui.list_group.setCurrentItem(item)

    def load_mode_test_group_data(self, group_name):
        """
        加载指定测试组的数据到列表控件
        
        清空当前列表控件，并将指定组的所有数据项加载到列表中。
        为每个数据项创建自定义的Data_Widget控件。
        
        Args:
            group_name (str): 要加载数据的组名
        """

        # 清空当前列表控件
        self.ui.list_group.clear()

        # 检查组是否存在
        if group_name not in self.test_group_data:
            return

        # 遍历组内所有数据项
        for item_data in self.test_group_data[group_name]:
            # print(f"item_data: {item_data}")

            # print(f"load_mode_test_group_data中的item_data的类型: {type(item_data)}")
            clone_item = QListWidgetItem()

            clone_item.setData(Qt.UserRole, tuple(item_data))

            # 添加到列表控件
            self.ui.list_group.addItem(clone_item)

            # 获取数据项的用户角色数据
            data_tuple = clone_item.data(Qt.UserRole)

            # 为数据项创建自定义控件
            data_name, data_text = data_tuple

            list_item_widget = Data_Widget(
                self.ui.list_group,
                data_name,
                data_text,
                show_all=False,
                checkable=False,
                sendable=False
            )

            list_item_widget.set_user_data(clone_item)
            # list_item_widget.send_clicked_signal.connect(self.item_send_clicked)
            self.ui.list_group.setItemWidget(clone_item, list_item_widget)

        self.application.yaml_window.update_test_group()

        self.application.update_all_crc_tooltips()

    def mode_group_name_changed(self):
        """
        处理测试组名称更改事件
        
        当用户在组合框中编辑组名并完成编辑时调用此方法。
        会验证新名称的唯一性，并更新内部数据结构。
        """
        # 从界面获取新名称
        new_name = self.ui.combo_box_mode_group.lineEdit().text().strip()
        if not new_name:
            return

        # 获取当前索引
        current_index = self.ui.combo_box_mode_group.currentIndex()

        # 如果索引无效，重置为当前组名或空字符串
        if current_index < 0:
            self.ui.combo_box_mode_group.lineEdit().setText("" if not self.current_group else self.current_group)
            return
        
        # 将新名称与原始名称比较，确保名称唯一性
        original_name = self.ui.combo_box_mode_group.itemText(current_index)
        
        if new_name == original_name:
            return

        # 检查新名称是否与现有名称冲突
        for i in range(self.ui.combo_box_mode_group.count()):
            if i != current_index and self.ui.combo_box_mode_group.itemText(i) == new_name:
                QMessageBox.warning(self.parent, "警告", "分组名称已存在！")
                self.ui.combo_box_mode_group.lineEdit().setText(original_name)
                return

        # 更新内部数据结构中的组名
        if original_name in self.test_group_data:
            # 获取原始数据
            original_data = self.test_group_data.pop(original_name)
            # 使用新名称存储数据
            self.test_group_data[new_name] = original_data

        # 刷新界面上的组名显示
        self.ui.combo_box_mode_group.setItemText(current_index, new_name)

        # 更新当前组引用
        if self.current_group == original_name:
            self.current_group = new_name

        # 重新设置当前索引
        self.ui.combo_box_mode_group.setCurrentIndex(current_index)

        self.application.yaml_window.update_test_group()
        # print(f"改名后的测试组: {self.test_group_data}")

    def delete_mode_group(self):
        """
        删除当前选中的测试组
        
        从组合框和内部数据结构中移除当前选中的测试组。
        如果删除后没有剩余组，则清空当前组引用和列表控件。
        """
        current_index = self.ui.combo_box_mode_group.currentIndex()
        if current_index < 0:
            return

        group_name = self.ui.combo_box_mode_group.currentText()

        self.ui.combo_box_mode_group.removeItem(current_index)

        # print(f"current_index: {current_index}")

        # 从内部数据结构中删除组数据
        if group_name in self.test_group_data:
            del self.test_group_data[group_name]
        
        # 如果没有剩余组，重置状态
        if self.ui.combo_box_mode_group.count() <= 0:
            self.current_group = None
            self.group_count = 0
            self.ui.list_group.clear()

        self.application.yaml_window.update_test_group()

        # print(f"删除后的测试组: {self.test_group_data}")

    # def mode_group_insert(self, parent, start, end):
    #     """
    #     处理向测试组插入新项的事件
        
    #     当用户通过拖放操作向测试组添加新数据项时调用此方法。
    #     会创建相应的自定义控件并更新内部数据结构。
        
    #     Args:
    #         parent: 父模型索引
    #         start (int): 插入项的起始索引
    #         end (int): 插入项的结束索引
    #     """
    #     # 获取当前选中的测试组的索引
    #     current_index = self.ui.combo_box_mode_group.currentIndex()

    #     # 获取当前选中的测试组名称
    #     group_name = self.ui.combo_box_mode_group.itemText(current_index)

    #     # 将新项添加到组数据中
    #     if group_name not in self.test_group_data:
    #         return
        
    #     for i in range(start, end + 1):
    #         item = self.ui.list_group.item(i)
            
    #         # 跳过空项
    #         if not item or item.data(Qt.UserRole):
    #             continue
            
    #         select_item = self.ui.list_data.selectedItems()
    #         if not select_item:
    #             self.ui.list_group.takeItem(i)
    #             continue

    #         source_item = select_item[0]
    #         data_tuple = source_item.data(Qt.UserRole)
    #         if not data_tuple or len(data_tuple) < 2:
    #             self.ui.list_group.takeItem(i)
    #             continue

    #         # 创建自定义控件
    #         data_name, data_text = data_tuple
    #         list_item_widget = Data_Widget(
    #             self.ui.list_group,
    #             data_name,
    #             data_text,
    #             show_all=False,
    #             checkable=False,
    #             sendable=False
    #         )

    #         list_item_widget.set_user_data(item)
    #         list_item_widget.send_clicked_signal.connect(self.item_send_clicked)
    #         self.ui.list_group.setItemWidget(item, list_item_widget)
        
    #         # 将项添加到组数据中
    #         self.test_group_data[group_name].append(data_tuple)

    #         self.application.yaml_window.update_test_group()

    #         # print(f"插入后的测试组: {self.test_group_data}")

    def delete_mode_group_item(self):
        """
        删除测试组中的选中项
        
        从当前测试组中移除用户选中的一个数据项，同时更新内部数据结构。
        """
        selected_items = self.ui.list_group.selectedItems()

        current_group_name = self.ui.combo_box_mode_group.currentText()
        
        if not selected_items:
            return

        # 反向遍历以避免索引变化问题
        for item in reversed(selected_items):
            row = self.ui.list_group.row(item)
            if row >= 0:
                self.ui.list_group.takeItem(row)
    
        item_data = item.data(Qt.UserRole)
        if item_data:
            # 从当前组的数据列表中移除该项
            if item_data in self.test_group_data[current_group_name]:
                self.test_group_data[current_group_name].remove(item_data)

            self.application.yaml_window.update_test_group()

        # print(f"删除后的测试组: {self.test_group_data}")

    def get_test_group(self):
        """
        获取所有测试组数据
        
        Returns:
            dict: 包含所有测试组数据的字典，键为组名，值为数据项列表
        """        
        data = {}

        # 遍历所有组数据
        for group_name, items in self.test_group_data.items():
            # 创建列表
            data[group_name] = []
            for item in items:

                # 将项数据添加到列表中
                data[group_name].append(tuple(item))
                
        return data
    
    def set_test_group(self, test_group_data):
        """
        设置测试组数据
        
        用提供的数据替换当前所有测试组数据，并更新界面显示。
        
        Args:
            test_group_data (dict): 包含所有测试组数据的字典
        """
        self.test_group_data = test_group_data

        # 将所有组名添加到组合框中
        group_names = list(self.test_group_data.keys())
        for group_name in group_names:
            self.ui.combo_box_mode_group.addItem(group_name)

        # 如果有数据，加载第一个组
        if test_group_data:
            first_group = next(iter(test_group_data.keys()))
            self.current_group = first_group
            self.ui.combo_box_mode_group.setCurrentText(first_group)
            self.load_mode_test_group_data(first_group)

    def item_send_clicked(self, item):
        """
        处理项目发送按钮点击事件
        
        Args:
            item: 被点击的列表项
        """

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 从item中提取实际的数据
        item_data = item.data(Qt.UserRole)
        
        # item_data是一个元组，第二个元素是实际的数据
        data = item_data[1]
        self.application.spi_controller.spi_send(data,self.clk_mode,self.bit_order)