#!/usr/bin/env python3.13
"""
filename: main.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-10-22
description: Main window and function realization
"""

import datetime
from PySide6.QtWidgets import (QWidget, 
        QFileDialog, QMessageBox, QListWidgetItem,
    )
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtCore import (Signal, QTimer, Qt, 
    )
from ui.Ui_spi_v1_main import Ui_MainForm
from data_group.custom_widgets import User_ListItemWidget
from sub_window.sub_add_data import SubWindowSpiText
from crc_manager.crc import CRC
from sub_window.sub_crc import SubWindowCRC
from test_group.send_mode import SendModeThread
from test_group.test_group_manager import TestGroupManager
from data_group.data_group_manager import DataGroupManager
from pc_mcu.pc_mcu2window import PC_MCU2Window  # 引入PC-MCU连接窗口类
from spi.spi2window import SPI2Window  # 引入SPI窗口类
from yaml_manager.yaml2window import YAML2Window  # 引入YAML窗口类
from log_manager.log2window import Log2Window  # 引入日志窗口类

# MainWindow class, handling the main window of the application
class MainWindow(QWidget):
    signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        
        self.data_map = {}

        # Initialize PC-MCU connection window
        self.pc_mcu = PC_MCU2Window(self)
        
        # Initialize SPI window
        self.spi = SPI2Window(self)

        # Initialize YAML window
        self.yaml = YAML2Window(self)

        # Initialize log window
        self.Log2Window = Log2Window(self)

        self.ui.combo_box_data_group.addItem("默认组")

        self.ui.line_edit_data.setPlaceholderText("00 00 00 00 ...")

        # Common button widgets
        self.ui.text_log.setPlaceholderText("日志显示区域")
        self.ui.button_add.clicked.connect(self.add_text)
        self.ui.button_det.clicked.connect(self.delete_text)
        self.ui.button_clear.clicked.connect(self.log_clear)
        self.ui.button_save.clicked.connect(self.log_save)
        self.ui.radio_button_order.clicked.connect(self.on_radio_button_clicked)
        self.ui.radio_button_circ.clicked.connect(self.on_radio_button_clicked)
        self.ui.radio_button_random.clicked.connect(self.on_radio_button_clicked)

        # fold and unfold log widget
        self.ui.log_widget.setVisible(True)
        self.ui.button_fold_log.clicked.connect(self.show_log_widget)
        self.log_widget_visible = True

        self.ui.button_start.clicked.connect(self.sending_mode)
        self.ui.button_stop.clicked.connect(self.stop_sending)

        self.ui.button_pc_fpga.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentIndex(0)
        )

        self.ui.button_pc_mcu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentIndex(1)
        )

        self.ui.button_crc.clicked.connect(self.open_crc_window)
        self.current_crc_mode = 0

        # Default order mode
        self.ui.radio_button_order.setChecked(True)
        self.on_radio_button_clicked()

        self.init_spi_monitoring()
        self.worker_thread = None
        self.is_sending = False
        self.content_initialized = False
        self.signals_connected = False
        self.destroyed.connect(self.spi.stop_device_monitor)

        # SPI default settings
        self.spi_clk_mode = 0
        self.spi_bit_order = 0
        self.spi_mode = 0
        self.spi_rx_size = 2
        self.last_device_cnt = -1

        self.data_group_manager = DataGroupManager(self.ui.combo_box_data_group,  self.ui.list_data, self)
        self.ui.button_rename.clicked.connect(lambda: self.data_group_manager.handle_rename_button(self))
        self.ui.button_add_data_group.clicked.connect(lambda: self.data_group_manager.add_data_group(self))
        self.ui.button_del_data_group.clicked.connect(self.data_group_manager.delete_data_group)
        self.data_group_manager.setup_list_data_drag_drop()

        self.test_group_manager = TestGroupManager(self.ui.combo_box_mode_group, self.ui.list_group, self.ui.list_data, self)

        self.ui.button_add_mode_group.clicked.connect(self.test_group_manager.add_mode_group)
        self.ui.button_del_mode_group.clicked.connect(self.test_group_manager.delete_mode_group)
        self.ui.combo_box_mode_group.currentIndexChanged.connect(self.group_changed)

        self.ui.button_del_select.clicked.connect(self.test_group_manager.delete_mode_group_item)

    def group_changed(self, index):
        if index < 0:
            self.current_group = None
            self.ui.list_group.clear()
            return

        new_group = self.ui.combo_box_mode_group.currentText()

        if new_group == self.test_group_manager.current_group:
            return

        if self.test_group_manager.current_group is not None:
            self.test_group_manager.save_current_mode_group()

        self.test_group_manager.current_group = new_group
        self.test_group_manager.load_mode_group_data(new_group)

    def show_common_widget(self):
        self.common_widget_visible = not self.common_widget_visible
        if self.common_widget_visible:
            self.ui.tabWidget_common.setVisible(True)
        else:
            self.ui.tabWidget_common.setVisible(False)

    def show_log_widget(self):
        self.log_widget_visible = not self.log_widget_visible
        if self.log_widget_visible:
            self.ui.log_widget.setVisible(True)
        else:
            self.ui.log_widget.setVisible(False)

    # Handle radio button click event
    def on_radio_button_clicked(self):
        if self.ui.radio_button_order.isChecked():
            self.ui.line_number.setEnabled(False)
        else:
            self.ui.line_number.setEnabled(True)
    
    # Send the data with mode selected
    def sending_mode(self):
        if self.is_sending:
            QMessageBox.warning(self, '警告', '发送正在进行中，请先停止当前发送任务')
            return
        
        time = self.ui.line_delay.text()

        if not time:
            delay = 0.5
        elif float(time) < 0:
            QMessageBox.warning(self, '警告', '请输入有效的延迟时间')
            return
        else:
            delay = float(self.ui.line_delay.text())

        item_send = []
        data_poll = False

        if self.ui.check_box_mode_poll.isChecked():
            """            
                Start data polling mode for order and cyclic mode, send all items in all groups.
                The delay has changed to inter-group delay.
                Intra-group is fixed at 0.1 seconds.
            """

            data_poll = True

            # Add all items in all groups to item_send
            all_data = self.test_group_manager.get_test_group()

            # Get all group names
            group_names = list(all_data.keys())

            for group_name in group_names:

                # Get items incurrent group_name 
                current_group_items  = all_data[group_name]
                # Store the items in groups in the "item_send" 
                item_send.append(current_group_items)

        else:
            # items in list_group to item_send
            for i in range(self.ui.list_group.count()):
                item = self.ui.list_group.item(i)
                if item and item.data(Qt.UserRole):
                    item_send.append(item)

        if not item_send:
            self.log("请添加数据项", 2)
            return

        if not hasattr(self, 'spi_device') or not self.spi_device:
            self.log("未发现SPI设备", 2)
            return

        self.worker_thread = SendModeThread(self)
        self.worker_thread.log_signal.connect(self.log)
        self.worker_thread.finished_signal.connect(self.on_sending_finished)
        self.worker_thread.progress_signal.connect(self.log)

        if self.ui.radio_button_order.isChecked():
            self.worker_thread.set_params(delay, item_send, "order", data_poll=data_poll)
        elif self.ui.radio_button_circ.isChecked():
            if  not self.ui.line_number.text():
                self.worker_thread.set_params(delay, item_send, "circ", cycles = '', data_poll=data_poll)
            else:
                cycles = int(self.ui.line_number.text())
                if cycles <= 0:
                    QMessageBox.warning(self, '警告', '循环次数设置失败')
                    return

                self.worker_thread.set_params(delay, item_send, "circ", cycles=cycles, data_poll=data_poll)
        elif self.ui.radio_button_random.isChecked():
            try:
                times = int(self.ui.line_number.text())
                if times <= 0:
                    QMessageBox.warning(self, '警告', '随机次数设置失败')
                    return
                self.worker_thread.set_params(delay, item_send, "random", times=times)
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入有效的随机次数')
                return

        self.is_sending = True
        self.ui.button_start.setEnabled(False)
        self.ui.button_stop.setEnabled(True)
        self.log("开始发送数据...", 0)

        self.worker_thread.start()

    # Stop the sending process
    def stop_sending(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.log("正在停止发送任务...", 0)
            self.worker_thread.stop()

    # Show the finishing log
    def on_sending_finished(self):
        self.is_sending = False
        self.ui.button_start.setEnabled(True)
        self.ui.button_stop.setEnabled(False)
        self.log("发送任务已完成或终止")

        if self.worker_thread:
            self.worker_thread.wait()
            self.worker_thread = None

    def open_crc_window(self):
        self.crc_window = SubWindowCRC(self)
        self.crc_window.crc_updated.connect(self.on_crc_updated)
        self.crc_window.show()

    # Start CRC tips
    def on_crc_updated(self, crc_mode):
        self.current_crc_mode = crc_mode
        if crc_mode == 0:
            self.log("CRC-16(自定义)校验已启用", 1)
        elif crc_mode == -1:
            self.log("CRC-16(自定义)校验已关闭", 1)
        
        print(self.current_crc_mode)
        
        self.update_all_crc_tooltips()

    # Update CRC tooltip when combo box selection changes
    def update_all_crc_tooltips(self):
        list_data_items = self.data_group_manager.get_list_data_items()
        for item in list_data_items:
            # item = self.ui.list_data.item(i)
            data_tuple = item.data(Qt.UserRole)

            if data_tuple and len(data_tuple) >= 2:
                _, data_text = data_tuple
                self.set_item_crc_tooltip(item, data_text)

        if self.ui.list_group.count() > 0:
            for i in range(self.ui.list_group.count()):
                item = self.ui.list_group.item(i)
                data_tuple = item.data(Qt.UserRole)

                if data_tuple and len(data_tuple) >= 2:
                    _, data_text = data_tuple
                    self.set_item_crc_tooltip(item, data_text)

    def set_item_crc_tooltip(self, item, data_text):
        if self.current_crc_mode == 0:
            hex_parts = data_text.strip().split()
            data_bytes = [int(part, 16) for part in hex_parts]
            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            crc_data_text = data_text + f" {crc_high:02X} {crc_low:02X}"
            item.setToolTip(f"校验后数据：{crc_data_text}")
        else:
            item.setToolTip(None)

    def init_spi_monitoring(self):
        """
            Initialize SPI device monitoring
        """

        if not hasattr(self, 'temp_scanner') or self.temp_scanner is None:
            from spi.spi_jtool import SPI
            self.temp_scanner = SPI(log_callback=self.log)
        
        self.device_monitor_timer = QTimer(self)
        self.device_monitor_timer.timeout.connect(self.spi.monitor_spi_devices)
        self.device_monitor_timer.start(1000)
        self.last_device_cnt = -1

    # Open sub window for adding SPI text data
    def add_text(self):
        self.sub_window = SubWindowSpiText(self)
        self.sub_window.signal.connect(self.mainwindow_data)
        self.sub_window.show()

    # Delete selected items from list_data
    def delete_text(self):
        self.data_group_manager.remove_selected_items_from_list_data()

    # Open sub window for adding SPI text data and user_defined listwidget item
    def mainwindow_data(self, data_name, data_text, show_all=True):
        # Clean the illegal characters in data_text
        clean_text = ''.join(c for c in data_text if c in '0123456789ABCDEFabcdef')

        if not clean_text:
            QMessageBox.warning(self, '警告', "输入为空")
            return
        
        # Add leading zero if the length of clean_text is odd
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # Format the clean_text (XX XX XX ...)to show
        format_text = ' '.join(clean_text[i:i+2] for i in range(0, len(clean_text), 2))

        current_group_name = self.data_group_manager.get_current_group_name()
        if current_group_name and current_group_name in self.data_group_manager.group_manager:
            existing_data = self.data_group_manager.group_manager[current_group_name]['data']
            for item in existing_data:
                if isinstance(item, tuple) and len(item) >= 2:
                    existing_name, _ = item
                    if existing_name == data_name:
                        QMessageBox.warning(self, '警告', f"名称 '{data_name}' 已存在，请选择其他名称。")
                        return

        item = QListWidgetItem()
        item.setData(Qt.UserRole, (data_name, format_text))
        self.ui.list_data.addItem(item)
        self.data_map[data_name] = format_text

        list_item_widget = User_ListItemWidget(
            self.ui.list_data,
            data_name,
            format_text,
            show_all,
            checkable= False
        )

        list_item_widget.set_user_data(item)

        list_item_widget.send_clicked.connect(self.spi_send_item)

        self.ui.list_data.setItemWidget(item, list_item_widget)

        self.update_all_crc_tooltips()

    # Send data when click the send button on listwidget item
    def spi_send_item(self, item):
        data_tuple = item.data(Qt.UserRole)
        if data_tuple and len(data_tuple) >= 2:
            data_name, data_text = data_tuple

        hex_parts = data_text.strip().split()

        if self.current_crc_mode == 0:
            temp_bytes = []
            
            for part in hex_parts:
                temp_bytes.append(int(part, 16))
            crc_value = CRC.crc_16_user(temp_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            hex_parts.append(f"{crc_high:02X}")
            hex_parts.append(f"{crc_low:02X}")
        
        data_bytes = []

        for part in hex_parts:
            data_bytes.append(int(part, 16))

        if not hasattr(self, 'spi_device') and not self.spi_device:
            self.log("未发现SPI设备", 2)
            return

        if self.spi_device.jtool is None or self.spi_device.dev_handle is None:
            if not self.spi_device.open_device():
                self.log("SPI设备连接失败", 2)
                return
        
        result = self.spi_device.spi_send(
            data_bytes,
            self.spi_clk_mode,
            self.spi_bit_order
        )

        if result is not True:
            self.log("数据发送失败", 2)
            return
        
        data = ' '.join([f"{byte:02X}" for byte in data_bytes])

        self.log(f"{data_name} 发送成功，数据: {data}",1)

    # Log message with timestamp and color coding
    def log(self, message, state=0):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.ui.text_log.textCursor()

        if not cursor.atEnd():
            cursor.movePosition(QTextCursor.End)

        time_format = QTextCharFormat()
        time_format.setForeground(QColor('blue'))
        cursor.setCharFormat(time_format)
        cursor.insertText(f"[{current_time}]:")

        content_format = QTextCharFormat()
        if state == 0:
            content_format.setForeground(QColor('black'))
        elif state == 1:
            content_format.setForeground(QColor('green'))
        elif state == 2:
            content_format.setForeground(QColor('red'))

        cursor.setCharFormat(content_format)
        cursor.insertText(f" {message}\n")
        self.ui.text_log.setTextCursor(cursor)

    # Clear log after confirmation
    def log_clear(self):
        log_text = self.ui.text_log.toPlainText()
        if log_text:
            reply = QMessageBox.information(
                self, 'Tip', '是否清除日志？',
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                self.ui.text_log.clear()

    # Save log to file
    def log_save(self):
        log_content = self.ui.text_log.toPlainText()
        if not log_content:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
            except Exception as e:
                self.log(f"保存日志失败：{str(e)}", 2)
