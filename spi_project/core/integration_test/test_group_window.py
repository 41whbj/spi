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

        self.setup_connections()

        self.handle_radio_button_clicked()

        self.ui.line_delay.setPlaceholderText("无输入，数据的延时固定为0.5秒")

    def setup_connections(self):
        """
        设置信号槽连接
        """

        self.ui.button_del_mode_group.clicked.connect(self.test_group_manager.delete_mode_group)
        self.ui.button_add_mode_group.clicked.connect(self.test_group_manager.add_mode_group)
        self.ui.button_del_select.clicked.connect(self.test_group_manager.delete_mode_group_item)

        self.ui.combo_box_mode_group.currentIndexChanged.connect(self.group_changed)

        self.ui.button_start.clicked.connect(self.sending_mode)
        self.ui.button_stop.clicked.connect(self.stop_sending)

        self.ui.radio_button_order.toggled.connect(self.handle_radio_button_clicked)
        self.ui.radio_button_order.setChecked(True)

        self.ui.radio_button_circ.clicked.connect(self.tooltip_change)
        self.ui.radio_button_random.clicked.connect(self.tooltip_change)

        self.ui.check_box_mode_poll.stateChanged.connect(self.tooltip_change)

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
            all_data = self.test_group_manager.get_test_group()

            # 遍历所有组，将每组的数据添加到item_send中
            group_names = list(all_data.keys())

            # 创建临时列表来存储所有数据项，保持与非轮询模式相同的数据结构
            temp_items = []
            for group_name in group_names:
                # 获取当前组的项目
                current_group_items = all_data[group_name]
                # 将组内项目添加到临时列表中
                temp_items.extend(current_group_items)
            
            # 为每个数据项创建QListWidgetItem对象，保持与非轮询模式相同的数据结构
            for data_tuple in temp_items:
                item = QListWidgetItem()
                item.setData(Qt.UserRole, data_tuple)
                item_send.append(item)

        else:

            # 将list_group中的项目添加到item_send
            for i in range(self.ui.list_group.count()):
                item = self.ui.list_group.item(i)
                if item and item.data(Qt.UserRole):
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

            if self.ui.line_number.text() == '':

                self.worker_thread.set_params(delay, item_send, "random", times='')
            elif times_text > 0:

                times = int(times_text)

                self.worker_thread.set_params(delay, item_send, "random", times=times)
            else:
                QMessageBox.warning(self.application, '警告', '请输入有效的数字')
                return
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

    def group_changed(self, index):
        """
        处理组别下拉框选择变化事件
        
        当用户在组别下拉框中选择不同的组时，此方法会被调用。
        它负责加载新选择组的数据到列表中，并更新当前组的引用。
        
        Args:
            index (int): 下拉框中选中项的索引，-1表示没有选中项
        """
        
        # 如果索引小于0，表示没有有效的组被选中
        if index < 0:
            # 清空当前组引用
            self.current_group = None
            # 清空列表控件中的所有项目
            self.ui.list_group.clear()
            # 直接返回，不执行后续操作
            return

        # 获取下拉框中当前选中的组名
        new_group = self.ui.combo_box_mode_group.currentText()

        # 如果新选择的组与当前组相同，则无需执行任何操作
        if new_group == self.test_group_manager.current_group:
            return

        # 更新测试组管理器的当前组引用为新选择的组
        self.test_group_manager.current_group = new_group
        
        # 调用测试组管理器加载新组的数据到列表中
        self.test_group_manager.load_mode_test_group_data(new_group)



