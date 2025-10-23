#!/usr/bin/env python3.13
"""
filename: test_group_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-07
description: 测试数据组管理器，用于处理测试数据组操作
"""

from PySide6.QtWidgets import (
    QMessageBox, QTreeWidgetItem,
    QAbstractItemView,QListWidgetItem
)
from PySide6.QtCore import QThread, Signal, QElapsedTimer, Qt, QTimer
import random

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
        current_group_name = None
        for i, item in enumerate(items):
            if not self.running:
                break

            op_timer = QElapsedTimer()
            op_timer.start()

            # 检查数据项是否包含组名信息
            data_tuple = item.data(Qt.UserRole)
        
            # 包含组名信息的数据项
            group_name, actual_data = data_tuple
            
            # 如果组名发生变化，表示进入新的组，需要添加组间延迟
            if current_group_name is not None and current_group_name != group_name:
                # 如果未停止发送，发送进度提示
                if cyclic_mode is True:
                    self.progress_signal.emit("发送下一组数据")


                op_time = op_timer.elapsed() / 1000.0
                actual_delay = max(0, self.delay - op_time)
                self.delay_fuction(actual_delay)

                # 重置计时器用于下一个数据项的发送
                op_timer.restart()
            
            current_group_name = group_name
            
            # 创建临时QListWidgetItem来发送实际数据
            temp_item = QListWidgetItem()
            temp_item.setData(Qt.UserRole, actual_data)
            self.send_item_data(temp_item)

            # 数据项之间使用固定0.01秒(10ms)延迟
            if i < (len(items) - 1):
                op_time = op_timer.elapsed() / 1000.0
                # 每个项之间有0.01秒延迟
                actual_delay = max(0, 0.01 - op_time)
                self.delay_fuction(actual_delay)

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

        # print(self.clk_mode, self.bit_order)

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
        self.test_group_manager = {}

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
        self.ui.tree_group.setColumnCount(2)
        self.ui.tree_group.setHeaderLabels(["测试组", "数据"])
        self.ui.tree_group.setColumnWidth(0, 130)  # 第一列宽度

        # 在初始化时设置行高
        self.ui.tree_group.setUniformRowHeights(True)
        # 或者设置固定行高
        self.ui.tree_group.setStyleSheet("QTreeWidget::item { height: 25px; }")

        # 设置拖拽模式为内部移动
        self.ui.tree_group.setDragDropMode(QAbstractItemView.InternalMove)

        # 设置选择模式为单选
        self.ui.tree_group.setSelectionMode(QAbstractItemView.SingleSelection)

        # 设置选择行为为选择整行
        self.ui.tree_group.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 禁用拖拽覆盖模式
        self.ui.tree_group.setDragDropOverwriteMode(False)

        # 设置缩进为0，防止放置嵌套
        self.ui.tree_group.setIndentation(0)
        
        # 启用接收拖拽
        self.ui.tree_group.setAcceptDrops(True)
        
        # 连接拖拽事件
        self.ui.tree_group.setDragDropOverwriteMode(False)

        self.ui.tree_group.itemClicked.connect(self.item_clicked)

        # 连接项编辑完成事件
        self.ui.tree_group.itemChanged.connect(self.test_group_item_changed)

        self.ui.tree_group.currentItemChanged.connect(lambda current, previous: QTimer.singleShot(0, self.item_moved))

        # 添加调试信息
        # print("已连接rowsMoved信号")

    def item_clicked(self, item):
        """
        处理测试组列表项点击事件，更新当前选中的测试组
        """
        # 确保点击的是父项
        if item.parent() is None:
            self.current_group = item.text(0)

            # 单击时切换展开/收起状态
        if item.childCount() > 0:  # 只有当项有子项时才执行
            if item.isExpanded():
                item.setExpanded(False)  # 收起子项
            else:
                item.setExpanded(True)    # 展开子项

    def item_moved(self):
        """
        处理测试组或者移动事件，更新内部数据结构以反映新的顺序

        移动测试组，更新test_group_manager中的测试组顺序，
        如果测试组有数据项，数据项需要跟着测试组移动，
        
        如果移动的数据项，需要更新测试组中数据项。
        """

        # print('检查是否触发了test_group_moved信号')

        # 重新构建test_group_manager以匹配UI中的新顺序
        new_group_data = {}

        # 遍历UI中的所有顶级项（测试组）
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            group_name = item.text(0)
            
            # 将其添加到新字典中
            new_group_data[group_name] = self.test_group_manager[group_name]

        self.test_group_manager = new_group_data

        # print(f"移动后的测试组: {self.test_group_manager}")

        # 对于数据项的移动，需要检查每个测试组的子项
        for group_name in self.test_group_manager:
            # 获取对应的UI项
            group_item = self.find_group_item(group_name)
            
            # 如果找不到group_item，跳过处理
            if group_item is None:
                continue

            # 重新构建该组的数据项列表以匹配UI顺序
            new_item_list = []
            for i in range(group_item.childCount()):
                child_item = group_item.child(i)
                item_data = child_item.data(0, Qt.UserRole)
                
                # 只有当item_data存在时才添加到列表中
                if item_data is not None:
                    new_item_list.append(item_data)

            # 更新该组的数据项列表
            self.test_group_manager[group_name] = new_item_list


        self.application.yaml_window.update_test_group()
        # print(f"移动后的测试组: {self.test_group_manager}")

    def add_test_group(self):
        """
        添加新的测试组
        
        创建一个新的测试组，为其生成唯一的名称，同时更新当前测试组。
        """

        # 增加组名计数器，确保新组名唯一
        self.group_count += 1

        new_group_name = f"新建分组{self.group_count}"

        # # print(f"group_count: {self.group_count}")
        
        self.test_group_manager[new_group_name] = []

        # 设置新组为当前组
        self.current_group = new_group_name

        item = QTreeWidgetItem([new_group_name])

        # 为item添加勾选框
        item.setCheckState(0,Qt.Checked)

        # 设置项为可编辑状态,可勾选，可拖拽
        item.setFlags(
            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | 
            Qt.ItemIsEditable | Qt.ItemIsDragEnabled | 
            Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
        )

        item._original_name = new_group_name

        # 设置item为选中状态
        item.setSelected(True)

        # 将item添加到列表中
        self.ui.tree_group.addTopLevelItem(item)

        # 确保选中的item可见
        self.ui.tree_group.setCurrentItem(item)

        self.application.yaml_window.update_test_group()
    
    def send_item(self,data):
        """
        处理添加按钮点击事件，将数据添加到当前选中的测试组中
        
        Args:
            data (dict): 包含要添加的数据，格式为 {'name': 名称, 'content': 内容}
        """

        if self.current_group is None:
            return
        
        name = data['name']
        content = data['content']

        self.test_group_manager[self.current_group].append((name, content))

        # print(f"self.test_group_manager: {self.test_group_manager}")

        self.application.yaml_window.update_test_group()

        self.load_test_group_data(name, content)

    def load_test_group_data(self, name, data):
        """
        加载发送过来的数据到当前选中的测试组父项中
        """

        item = self.ui.tree_group.currentItem()

        if item is None:
            return
        
        # 保证添加的子项在父项下
        if item.parent():
            return

        # 展开子项
        item.setExpanded(True)    

        # 创建子项
        child = QTreeWidgetItem(item)
        
        # 设置显示文本
        child.setText(0, name)
        child.setText(1, data)

        # 将数据以元组形式存储为用户数据
        child.setData(0, Qt.UserRole, (name, data))

        # 设置子项的标志，使其不可再有子项
        child.setFlags(
            Qt.ItemIsSelectable| Qt.ItemIsEditable |
            Qt.ItemIsDragEnabled | Qt.ItemIsEnabled
        )

    def test_group_item_changed(self, item, column):
        """
        处理测试组名称更改及勾选框状态变化事件

        Args:
            item (QTreeWidgetItem): 被编辑的项
        """

        if column == 0:
            # 调用TestGroupWindow中的方法来更新全选复选框状态
            if hasattr(self.application, 'test_group_window'):
                self.application.test_group_window.update_select_all_state() 
        
        # 只处理顶级项（测试组）的名称更改，不处理子项（数据项）
        if item.parent() is not None:
            return

        # 从界面获取新名称
        new_name = item.text(0).strip()
        if not new_name:
            return

        original_name = item._original_name

        # 遍历所有组，找到与当前项匹配的原始组名
        for group_name, _ in self.test_group_manager.items():
            # 查找与当前项文本匹配的组名（在修改之前应该是原始名称）
            tree_item = self.find_group_item(group_name)
            if tree_item == item:
                original_name = group_name
                break

        # 如果新名称与原始名称相同，无需处理
        if new_name == original_name:
            return

        # 检查新名称是否与现有名称冲突
        if new_name in self.test_group_manager:
            QMessageBox.warning(self.application, "警告", "分组名称已存在！")
            # 恢复原始名称
            item.setText(0, original_name)
            return

        # 更新内部数据结构中的组名
        # 使用del和重新插入的方式保持字典顺序
        if original_name in self.test_group_manager:
            # 保存原始数据
            original_data = self.test_group_manager[original_name]
            items = list(self.test_group_manager.items())
            
            # 找到原始名称的位置
            original_index = -1
            for i, (key, _) in enumerate(items):
                if key == original_name:
                    original_index = i
                    break
            
            # 如果找到了原始名称
            if original_index != -1:
                # 删除旧键
                del self.test_group_manager[original_name]
                
                # 在原位置插入新键值对
                items.pop(original_index)  # 移除旧项
                items.insert(original_index, (new_name, original_data))  # 在原位置插入新项
                
                # 重建字典以保持顺序
                self.test_group_manager.clear()
                self.test_group_manager.update(items)

        # 更新当前组引用
        if self.current_group == original_name:
            self.current_group = new_name

        # 重要：更新item的_original_name属性，以便后续可以再次修改名称
        item._original_name = new_name

        self.application.yaml_window.update_test_group()
        # print(f"改名后的测试组: {self.test_group_manager}")

    def find_group_item(self, group_name):
        """
        根据组名查找对应的QTreeWidgetItem
        
        Args:
            group_name (str): 组名
            
        Returns:
            QTreeWidgetItem: 对应的项，如果未找到则返回None
        """
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            if item.text(0) == group_name:
                return item
        return None

    def delete_item(self):
        """
        删除当前选中的测试组，或者数据项
        
        如果当前选中的测试组内存在数据，触发提示，确定后删除该组。
        如果当前选中的是数据项或者测试组为空，则直接删除。
        """
        # 获取当前选中的项
        selected_items = self.ui.tree_group.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        
        # 判断是删除测试组还是数据项
        if item.parent() is None:  # 删除测试组
            group_name = item.text(0)
            
            # 检查组内是否有数据，如果有则提示
            if self.test_group_manager[group_name]:
                reply = QMessageBox.question(
                    self.application, 
                    '确认删除', 
                    f'测试组 "{group_name}" 中存在有数据，确定要删除吗？',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            
            # 从内部数据结构中删除组数据
            if group_name in self.test_group_manager:
                del self.test_group_manager[group_name]
            
            # 从界面中删除项
            index = self.ui.tree_group.indexOfTopLevelItem(item)
            self.ui.tree_group.takeTopLevelItem(index)
            
            # 更新当前组引用
            if self.current_group == group_name:
                self.current_group = None
                # 如果还有其他组，设置第一个组为当前组
                if self.ui.tree_group.topLevelItemCount() > 0:
                    first_item = self.ui.tree_group.topLevelItem(0)
                    self.current_group = first_item.text(0)
        else:  
            # 删除数据项
            parent_item = item.parent()
            parent_name = parent_item.text(0)
            
            # 从界面中删除项
            parent_item.removeChild(item)
            
            # 从self.test_group_manager中删除数据
            if parent_name in self.test_group_manager:
            # 查找要删除的数据项并移除它
                item_data = item.data(0, Qt.UserRole)
                if item_data in self.test_group_manager[parent_name]:
                    self.test_group_manager[parent_name].remove(item_data)

        # 如果没有剩余组，重置状态
        if self.ui.tree_group.topLevelItemCount() <= 0:
            self.current_group = None
            self.group_count = 0

        self.application.yaml_window.update_test_group()
        # print(f"删除后的测试组: {self.test_group_manager}")

    def get_test_group_manager(self):
        """
        获取所有测试组
        
        Returns:
            dict: 包含所有测试组的字典，键为组名，值为数据项列表
        """        
                
        return self.test_group_manager
    
    def set_test_group(self, test_group):
        """
        设置测试组数据
        
        用提供的数据替换当前所有测试组数据，并更新界面显示。
        导入完整的test_group数据，包括测试组和组内的子项。
        
        Args:
            test_group (dict): 包含所有测试组数据的字典
        """
        # 清空当前的界面和数据
        self.ui.tree_group.clear()
        self.test_group_manager = {}
        self.group_count = 0
        
        # 遍历导入的测试组数据
        for group_name, group_data in test_group.items():
            # 如果导入的分组名称没有修改，更新组计数器，确保新组名唯一
            if group_name.startswith("新建分组"):
                group_num = int(group_name.replace("新建分组", ""))
                self.group_count = max(self.group_count, group_num)

            
            # 将数据添加到内部数据结构
            self.test_group_manager[group_name] = group_data
            
            # 创建测试组项
            item = QTreeWidgetItem([group_name])
            
            # 为item添加勾选框
            item.setCheckState(0, Qt.Checked)
            
            # 设置项为可编辑状态,可勾选，可拖拽
            item.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | 
                Qt.ItemIsEditable | Qt.ItemIsDragEnabled | 
                Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
            )
            
            item._original_name = group_name
            
            # 将item添加到列表中
            self.ui.tree_group.addTopLevelItem(item)
            
            # 为每个数据项创建子项
            for data_item in group_data:
                if isinstance(data_item, dict):
                    # 字典格式: {'name': name, 'content': content}
                    name = data_item['name']
                    content = data_item['content']
                else:
                    # 元组格式: (name, content)
                    name, content = data_item
                
                # 创建子项
                child = QTreeWidgetItem(item)
                
                # 设置显示文本
                child.setText(0, name)
                child.setText(1, content)
                
                # 将数据以元组形式存储为用户数据
                child.setData(0, Qt.UserRole, (name, content))
                
                # 设置子项的标志，使其不可再有子项
                child.setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsEditable |
                    Qt.ItemIsDragEnabled | Qt.ItemIsEnabled
                )
            
            # 展开测试组项
            item.setExpanded(True)
        
        # 更新当前组引用
        if self.ui.tree_group.topLevelItemCount() > 0:
            first_item = self.ui.tree_group.topLevelItem(0)
            self.current_group = first_item.text(0)
            
            # 选中第一个数据组
            self.ui.tree_group.setCurrentItem(first_item)
        else:
            self.current_group = None

        # print(f"导入后的测试组: {self.test_group_manager}")

