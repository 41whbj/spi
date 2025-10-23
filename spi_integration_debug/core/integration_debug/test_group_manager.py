#!/usr/bin/env python3.13
"""
filename: test_group_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-07
description: 测试数据组管理器，用于处理测试数据组操作
"""

from PySide6.QtWidgets import (
    QMessageBox, QTreeWidgetItem,QListWidgetItem,
)
from PySide6.QtCore import Qt

from .test_group_thread import SendModeThread
# import time

#===============================================================================
# 核心管理类定义
#===============================================================================

class TestGroupManager:
    """
    测试组管理器类
    
    该类负责管理测试数据组的创建、删除、重命名、加载和保存等功能。
    """
    
    def __init__(self, application, spi_controller):
        """
        初始化TestGroupManager实例
        
        Args:
            application: 应用实例引用
        """
        self.application = application
        self.ui = self.application.ui

        self.spi_controller = spi_controller

        self.send_mode_thread = SendModeThread(self.application,self.spi_controller)

        # 存储所有测试组数据的字典，键为组名，值为数据项列表
        self.test_group_manager = {}

        # 当前选中的测试组名称  
        self.current_group = None

        # 当前点击发送按钮的测试组名称
        self.current_clicked_group = None

        self.log = self.application.log_window

         # 用于生成新组名的计数器
        self.group_count = 0 

        self.is_sending = False

        self.updating_selection = False

#===============================================================================
# 测试组管理功能
#===============================================================================

    def add_test_group(self):
        """
        添加新的测试组
        
        创建一个新的测试组，为其生成唯一的名称，同时更新当前测试组。
        """

        # 增加组名计数器，确保新组名唯一
        self.group_count += 1

        new_group_name = f"新建分组{self.group_count}"
        
        self.test_group_manager[new_group_name] = []

        # 设置新组为当前组
        self.current_group = new_group_name

        item = QTreeWidgetItem([new_group_name])

        # 为item添加勾选框
        item.setCheckState(0, Qt.Checked)

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

        # 强制刷新树形控件
        self.ui.tree_group.viewport().update()

        # 注意：不再在这里调用create_button_widget，而是在TestGroupWindow中处理

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

#===============================================================================
# UI交互处理功能
#===============================================================================

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

        original_name = item._original_name

        # 从界面获取新名称
        new_name = item.text(0).strip()
        if not new_name or new_name == "":
            QMessageBox.warning(self.application, "警告", "名称不能为空！")
            # 恢复原始名称
            item.setText(0, original_name)
            return

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

#===============================================================================
# 数据查找和删除功能
#===============================================================================

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

#===============================================================================
# 数据导入导出功能
#===============================================================================

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

            # 注意：不再在这里创建按钮widget，而是在TestGroupWindow中处理
            
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
                    Qt.ItemIsSelectable |
                    Qt.ItemIsDragEnabled | Qt.ItemIsEnabled
                )
            
            # 展开测试组项
            item.setExpanded(True)

        # 注意：不再在这里创建按钮widget，而是在TestGroupWindow中处理

        # 更新当前组引用
        if self.ui.tree_group.topLevelItemCount() > 0:
            first_item = self.ui.tree_group.topLevelItem(0)
            self.current_group = first_item.text(0)
            
            # 选中第一个数据组
            self.ui.tree_group.setCurrentItem(first_item)
        else:
            self.current_group = None

        # print(f"导入后的测试组: {self.test_group_manager}")

#===============================================================================
# 发送模式处理功能
#===============================================================================

    def sending_mode(self, is_global_mode=False):
        """
        根据选定的模式发送数据
        
        检查当前是否正在发送数据，验证用户输入的延迟时间，
        根据选择的模式（顺序、循环、随机）和选项（轮询）准备数据，
        然后启动相应的发送线程。
        
        Args:
            is_global_mode (bool): 是否为全局发送模式（处理所有勾选的组）
        """

        # 检查是否已经在发送数据
        if self.is_sending:
            QMessageBox.warning(self.application, '警告', '发送正在进行中，请先停止当前发送任务')
            return
        
        if self.spi_controller.driver.dev_handle is None:
            self.log.log("SPI设备未连接")
            return
        
        # 获取并验证延迟时间输入
        time = self.ui.line_delay.text()

        if not time:
            # 如果没有输入延迟时间，使用默认值0.5秒
            delay = 0.5
        elif float(time) < 0:
            # 检查延迟时间是否为有效值
            QMessageBox.warning(self.application, '警告', '请输入有效的延迟时间')
            return
        elif float(time) < 0.01:
            # 检查延迟时间是否为有效值
            QMessageBox.warning(self.application, '警告', '请输入大于等于0.01s的延迟时间')
            return
        else:
            # 使用用户输入的延迟时间
            delay = float(self.ui.line_delay.text())

        # 初始化发送数据列表和轮询标志
        item_send = []
        data_poll = False

        if is_global_mode:
            # 全局模式：处理所有勾选的测试组
            # 检查是否启用数据轮询模式
            if self.ui.check_box_mode_poll.isChecked():
                """            
                启动数据轮询模式用于顺序和循环模式，发送所有组中的所有项目。
                延迟已更改为组间延迟。
                组内延迟固定为0.01秒。
                """

                data_poll = True

                # 获取所有组的数据
                all_data = self.get_test_group_manager()

                # 遍历所有组，只将被勾选的组的数据添加到item_send中
                checked_groups_count = 0
                temp_items = []
                for i in range(self.ui.tree_group.topLevelItemCount()):
                    group_item = self.ui.tree_group.topLevelItem(i)
                    # 检查组是否被勾选
                    if group_item.checkState(0) == Qt.Checked:
                        checked_groups_count += 1
                        group_name = group_item.text(0)
                        # 获取当前组的项目
                        if group_name in all_data:
                            current_group_items = all_data[group_name]
                            for item in current_group_items:
                                temp_items.append((group_name, item))

                # 检查是否有被勾选的组
                if checked_groups_count == 0:
                    self.application.log_window.log("请勾选至少一个数据组")
                    return
                
                # 为每个数据项创建QListWidgetItem对象，保持与非轮询模式相同的数据结构
                for group_data_tuple in temp_items:
                    item = QListWidgetItem()
                    item.setData(Qt.UserRole, group_data_tuple)
                    item_send.append(item)
                    # print(f"轮询模式下的 {group_data_tuple}")
        else:
            # 单组模式：只处理当前点击按钮对应的组
            group_item = self.find_group_item(self.current_clicked_group)
            if group_item:
                # 遍历组内的所有子项
                for i in range(group_item.childCount()):
                    child_item = group_item.child(i)
                    # 从QTreeWidgetItem中提取数据
                    data_tuple = child_item.data(0, Qt.UserRole)
                    if data_tuple:
                        # 创建QListWidgetItem并设置数据
                        item = QListWidgetItem()
                        item.setData(Qt.UserRole, data_tuple)
                        item_send.append(item)

                        # print(f"非轮询模式下的 {data_tuple}")
            else:
                self.application.log_window.log("未找到指定的数据组")
                return

        # 检查是否有要发送的数据项
        if not item_send:
            self.log.log("请添加数据项")
            return
        
        self.cleanup_worker_thread()

        # 创建发送线程并连接信号
        self.worker_thread = self.send_mode_thread

        # 断开旧连接（防止残留）
        try:
            self.worker_thread.log_signal.disconnect()
        except (TypeError, RuntimeError):
            pass  # 忽略未连接的情况
        
        try:
            self.worker_thread.finished_signal.disconnect()
        except (TypeError, RuntimeError):
            pass  # 忽略未连接的情况

        try:
            self.worker_thread.log_signal.disconnect()
        except (TypeError, RuntimeError):
            pass  # 忽略未连接的情况

        # 连接信号
        self.worker_thread.log_signal.connect(self.application.log_window.log)
        self.worker_thread.finished_signal.connect(self.sending_finished)

        # 根据选择的发送模式设置线程参数
        if self.ui.radio_button_order.isChecked():
            # 顺序发送模式
            self.worker_thread.set_params(delay, item_send, "order", data_poll=data_poll)
        elif self.ui.radio_button_circ.isChecked():
            # 循环发送模式
            if not self.ui.line_number.text():
                # 如果没有指定循环次数，则持续循环发送
                self.worker_thread.set_params(delay, item_send, "circ", cycles='', data_poll=data_poll)
            else:
                # 指定循环次数
                cycles = int(self.ui.line_number.text())
                if cycles <= 0:
                    QMessageBox.warning(self.application, '警告', '循环次数设置失败')
                    return
                self.worker_thread.set_params(delay, item_send, "circ", cycles=cycles, data_poll=data_poll)
        elif self.ui.radio_button_random.isChecked():
            times_text = self.ui.line_number.text()
            if not self.ui.line_number.text():
                self.worker_thread.set_params(delay, item_send, "random", times='', data_poll=data_poll)
            else:
                times = int(times_text)
                self.worker_thread.set_params(delay, item_send, "random", times=times, data_poll=data_poll)
        else:
            QMessageBox.warning(
                self.application, 
                "警告",
                "未选择发送模式"
            )
            return

        self.is_sending = True
        
        # 根据模式设置UI状态
        if is_global_mode:
            # 全局模式下的UI状态
            # self.ui.button_start.setEnabled(False)
            self.ui.button_stop.setEnabled(True)
        else:
            # 单组模式下的UI状态
            self.ui.button_start.setEnabled(False)
            self.ui.button_stop.setEnabled(True)
            
        # self.application.log_window.log("开始发送数据...", 0)
        self.worker_thread.start()

    def send_button_clicked(self, group_name):
        """
        处理发送按钮点击事件
        
        Args:
            group_name (str): 被点击按钮对应的组名
        """
        # 记录当前点击的组
        self.current_clicked_group = group_name
        # print(f"点击了组 '{group_name}' 的发送按钮")
        
        # 直接调用发送模式方法
        data_poll = self.ui.check_box_mode_poll.isChecked()

        # print(f"data_poll状态为:{data_poll}")

        if data_poll :
            QMessageBox.warning(
                self.application, 
                "警告",
                "轮询模式下不能通过此按钮发送"
            )
            return
        self.sending_mode()

    def cleanup_worker_thread(self):
        """
        安全线程清理方法：主动停止线程并等待其结束，随后删除引用。
        防止线程泄露和信号重复绑定问题。
        """
        if hasattr(self, 'worker_thread'):
            thread = self.worker_thread
            if thread.isRunning():
                thread.stop()             # 请求线程停止
                thread.wait(1)            # 等待最多1秒让线程自然退出
            del self.worker_thread        # 删除线程对象引用


    def stop_sending_mode(self):
        """
        停止当前正在进行的发送模式
        """
        self.cleanup_worker_thread()      # 使用统一清理逻辑


    def sending_finished(self):
        """
        发送完成后回调函数，用于更新界面状态和释放资源
        """
        self.is_sending = False
        self.cleanup_worker_thread()      # 清理线程资源
        # self.application.log_window.log("发送任务已完成或终止")