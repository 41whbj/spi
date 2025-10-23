#!/usr/bin/env python3.13
"""
filename: test_group_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-29
description: 测试数据组窗口类，和主程序界面交互
"""

from PySide6.QtWidgets import QMessageBox, QListWidgetItem
from PySide6.QtCore import QObject, Qt
from .test_group_manager import TestGroupManager, SendModeThread


class TestGroupWindow(QObject):
    """
    测试数据组窗口类，和主程序界面交互
    """

    def __init__(self, application, spi_controller):
        """
        初始化测试数据组窗口
        
        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.spi_controller = spi_controller

        self.test_group_manager = TestGroupManager(self.application)

        self.is_sending = False

        self.updating_selection = False

        self.setup_connections()

        self.handle_radio_button_clicked()

        self.ui.line_delay.setPlaceholderText("无输入，数据的延时固定为0.5秒")

    def setup_connections(self):
        """
        设置信号槽连接
        """

        self.ui.button_del_test_group.clicked.connect(self.test_group_manager.delete_item)
        self.ui.button_add_test_group.clicked.connect(self.test_group_manager.add_test_group)

        # self.ui.combo_box_mode_group.currentIndexChanged.connect(self.group_changed)

        self.ui.button_start.clicked.connect(self.sending_mode)
        self.ui.button_stop.clicked.connect(self.stop_sending)

        self.ui.radio_button_order.toggled.connect(self.handle_radio_button_clicked)
        self.ui.radio_button_order.setChecked(True)

        self.ui.radio_button_circ.clicked.connect(self.tooltip_change)
        self.ui.radio_button_random.clicked.connect(self.tooltip_change)

        self.ui.check_box_mode_poll.stateChanged.connect(self.tooltip_change)

        # 连接全选复选框
        self.ui.check_box_select_all.stateChanged.connect(self.select_all_changed)

    def select_all_changed(self, state):
        """
        处理全选复选框状态变化
        
        Args:
            state: 复选框的状态 (Qt.Checked 或 Qt.Unchecked)
        """
        # 如果正在更新选择状态，避免循环触发
        if self.updating_selection:
            return

        # 如果tree_group中没有项，直接返回
        if self.ui.tree_group.topLevelItemCount() == 0:
            return
        
        # 遍历所有顶级项（测试组）
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            # 根据全选复选框的状态设置每个测试组的勾选状态
            if state == 2:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)

    def update_select_all_state(self):
        """
        更新全选复选框的状态
        当某个item的勾选状态改变时调用此方法来更新全选复选框的状态
        """
        # 设置标志以避免循环触发
        self.updating_selection = True
        
        try:
            # 如果没有项，直接返回并将全选复选框设为未选中
            if self.ui.tree_group.topLevelItemCount() == 0:
                self.ui.check_box_select_all.setChecked(False)
                return
            
            # 检查是否所有项都被选中
            all_checked = True
            for i in range(self.ui.tree_group.topLevelItemCount()):
                item = self.ui.tree_group.topLevelItem(i)
                if item.checkState(0) != Qt.Checked:
                    all_checked = False
                    break
            
            # 更新全选复选框的状态
            self.ui.check_box_select_all.setChecked(all_checked)
        finally:
            # 重置标志
            self.updating_selection = False


    def handle_radio_button_clicked(self):
        """
        根据发送模式，根据启用或禁用输入框。顺序发送时禁用行号输入框，其他模式下启用。

        更新行号输入框的提示信息
        """
        
        # print("radio button 触发")

        if self.ui.radio_button_order.isChecked():

            # 顺序发送时禁用输入框
            self.ui.line_number.setEnabled(False)

            # 清空输入框
            self.ui.line_number.clear()

            self.ui.line_number.setPlaceholderText("")
        else:
            # 开启输入框
            self.ui.line_number.setEnabled(True)

            # 清空输入框
            self.ui.line_number.clear()

    def tooltip_change(self):
        """
        根据勾选框状态，改变行号输入框的提示信息
        """
        if self.ui.check_box_mode_poll.isChecked():
            self.ui.line_delay.setPlaceholderText("无输入，组间延迟为0.5秒")
        else:
            self.ui.line_delay.setPlaceholderText("无输入，数据延时为0.5秒")
        
        if self.ui.radio_button_random.isChecked() or self.ui.radio_button_circ.isChecked():
            # print("radio button random 或者 circ 触发")
            self.ui.line_number.setPlaceholderText("无输入，一直发送，直到停止")

    def sending_mode(self):
        """
        根据选定的模式发送数据
        
        检查当前是否正在发送数据，验证用户输入的延迟时间，
        根据选择的模式（顺序、循环、随机）和选项（轮询）准备数据，
        然后启动相应的发送线程。
        """

        # 检查是否已经在发送数据
        if self.is_sending:
            QMessageBox.warning(self.application, '警告', '发送正在进行中，请先停止当前发送任务')
            return
        
        # 获取并验证延迟时间输入
        time = self.ui.line_delay.text()

        if not time:

            # 如果没有输入延迟时间，使用默认值0.5秒
            delay = 0.5
            # self.application.log_window.log(f"使用默认值{delay}秒")
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

        # 检查是否启用数据轮询模式
        if self.ui.check_box_mode_poll.isChecked():
            """            
            启动数据轮询模式用于顺序和循环模式，发送所有组中的所有项目。
            延迟已更改为组间延迟。
            组内延迟固定为0.01秒。
            """

            data_poll = True

            # 获取所有组的数据
            all_data = self.test_group_manager.get_test_group_manager()

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
                self.application.log_window.log("请勾选至少一个数据组", 2)
                return
            
            # 为每个数据项创建QListWidgetItem对象，保持与非轮询模式相同的数据结构
            for group_data_tuple in temp_items:
                item = QListWidgetItem()
                item.setData(Qt.UserRole, group_data_tuple)
                item_send.append(item)
        else:
            # 非轮询模式：将tree_group中被勾选的项目添加到item_send
            checked_items_count = 0
            checked_items = []
            
            # 遍历所有顶级项（测试组）
            for i in range(self.ui.tree_group.topLevelItemCount()):
                group_item = self.ui.tree_group.topLevelItem(i)
                # 检查组是否被勾选
                if group_item.checkState(0) == Qt.Checked:
                    checked_items_count += 1
                    checked_items.append(group_item)
            
            # 检查勾选的项数
            if checked_items_count == 0:
                self.application.log_window.log("请勾选至少一个数据组", 2)
                return
            elif checked_items_count > 1:
                # 如果勾选项数大于1，弹出警告
                QMessageBox.warning(self.application, '警告', '非组间发送模式下只能选择一个数据组')
                return

            # 只处理被勾选的组
            for group_item in checked_items:
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

        # 检查是否有要发送的数据项
        if not item_send:
            self.application.log_window.log("请添加数据项", 2)
            return

        # 创建发送线程并连接信号
        self.worker_thread = SendModeThread(self.application, self.spi_controller)
        self.worker_thread.log_signal.connect(self.application.log_window.log)
        self.worker_thread.finished_signal.connect(self.on_sending_finished)
        self.worker_thread.progress_signal.connect(self.application.log_window.log)

        # 根据选择的发送模式设置线程参数
        if self.ui.radio_button_order.isChecked():

            # 顺序发送模式
            self.worker_thread.set_params(delay, item_send, "order", data_poll=data_poll)
        elif self.ui.radio_button_circ.isChecked():

            # 循环发送模式
            if  not self.ui.line_number.text():
                # 如果没有指定循环次数，则持续循环发送
                self.worker_thread.set_params(delay, item_send, "circ", cycles = '', data_poll=data_poll)
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

                self.worker_thread.set_params(delay, item_send, "random", times='')
            else:
                times = int(times_text)

                self.worker_thread.set_params(delay, item_send, "random", times=times)
        else:
            QMessageBox.warning(
                self.application, 
                "警告",
                "未选择发送模式"
            )
            return

        self.is_sending = True
        self.ui.button_start.setEnabled(False)
        self.ui.button_stop.setEnabled(True)
        self.application.log_window.log("开始发送数据...", 0)

        self.worker_thread.start()

    def stop_sending(self):
        """
        停止发送任务
        """
        if hasattr(self, 'worker_thread') and self.worker_thread and self.worker_thread.isRunning():
            self.application.log_window.log("正在停止发送任务...", 0)
            self.worker_thread.stop()

    def on_sending_finished(self):
        """
        发送任务完成后的回调函数
        """
        self.is_sending = False
        self.ui.button_start.setEnabled(True)
        self.ui.button_stop.setEnabled(False)
        self.application.log_window.log("发送任务已完成或终止")

        # 不需要在这里再次调用stop()，线程已经自然结束
        if hasattr(self, 'worker_thread') and self.worker_thread:
            self.worker_thread.wait()  # 等待线程完全结束
            self.worker_thread = None  # 清理线程引用
