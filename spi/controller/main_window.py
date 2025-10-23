#!/usr/bin/env python3.13
"""
filename: main.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-10-22
description: Main window and function realization
"""

import datetime
from ctypes import c_int, byref
from PySide6.QtWidgets import (QWidget, 
        QFileDialog, QMessageBox, QListWidgetItem,
        QListWidget
    )
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtCore import (Signal, QTimer, Qt, 
    )
from ui.Ui_spi_v1_main import Ui_MainForm
from .custom_widgets import User_ListItemWidget
from subwindow.sub_spi import SubWindowSpiText
from subwindow.sub_name import SubWindowName
from .crc import CRC
from subwindow.sub_crc import SubWindowCRC
from thread.scan_device import ScanDeviceThread
from thread.scan_instance import ScanInstanceThread
from thread.send_mode import SendModeThread
from .spi_jtool import SPI
from .group_manager import GroupManager
from .yaml_config import YamlConfig

# MainWindow class, handling the main window of the application
class MainWindow(QWidget):
    signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        
        self.data_map = {}

        self.ui.combo_box_data_group.addItem("分组1")

        # PC and MCU test buttons
        self.ui.button_connect.clicked.connect(self.scan_device)
        self.ui.button_scan.clicked.connect(self.scan_case)

        self.ui.line_edit_data.setPlaceholderText("00 00 00 00 ...")

        # Common button widgets
        self.ui.text_log.setPlaceholderText("日志显示区域")
        self.ui.button_add.clicked.connect(self.add_text)
        self.ui.button_det.clicked.connect(self.delete_text)
        self.ui.button_send.clicked.connect(self.spi_send_line)
        self.ui.button_clear.clicked.connect(self.log_clear)
        self.ui.button_save.clicked.connect(self.log_save)
        self.ui.button_import.clicked.connect(self.import_config)
        self.ui.button_export.clicked.connect(self.export_config)
        self.ui.button_rename.clicked.connect(self.handle_rename_button)
        self.ui.button_receive.clicked.connect(self.spi_receive)

        self.ui.radio_button_order.clicked.connect(self.on_radio_button_clicked)
        self.ui.radio_button_circ.clicked.connect(self.on_radio_button_clicked)
        self.ui.radio_button_random.clicked.connect(self.on_radio_button_clicked)

        # fold and unfold SPI widget
        self.ui.button_fold_common.clicked.connect(self.show_common_widget)
        self.common_widget_visible = False
        self.ui.tabWidget_common.setVisible(False)

        # fold and unfold log widget
        self.ui.button_fold_log.clicked.connect(self.show_log_widget)
        self.log_widget_visible = True

        self.ui.button_start.clicked.connect(self.sending_mode)
        self.ui.button_stop.clicked.connect(self.stop_sending)

        self.ui.button_spi.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentIndex(0)
        )
        self.ui.button_hard.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentIndex(1)
        )
        self.ui.button_prj.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentIndex(2)
        )

        self.ui.button_crc.clicked.connect(self.open_crc_window)
        self.current_crc_mode = -1

        # Default order mode
        self.ui.radio_button_order.setChecked(True)
        self.on_radio_button_clicked()

        self.init_spi_monitoring()
        self.worker_thread = None
        self.is_sending = False
        self.content_initialized = False
        self.signals_connected = False
        self.destroyed.connect(self.stop_device_monitor)

        # SPI default settings
        self.spi_clk_mode = 0
        self.spi_bit_order = 0
        self.spi_mode = 0
        self.spi_rx_size = 2

        self.group_manager = GroupManager(self.ui.combo_box_group, self.ui.list_group, self.ui.list_data, self)

        self.ui.button_add_group.clicked.connect(self.group_manager.add_group)
        self.ui.button_del_group.clicked.connect(self.group_manager.delete_group)
        self.ui.combo_box_group.currentIndexChanged.connect(self.group_changed)

        self.ui.button_del_select.clicked.connect(self.group_manager.delete_group_item)

        # User-defined list widget settings 
        # Realize drag-and-drop function
        self.ui.list_data.setDragDropMode(QListWidget.InternalMove)
        self.ui.list_data.setSelectionMode(QListWidget.SingleSelection)
        self.ui.list_data.setDefaultDropAction(Qt.MoveAction)
        self.ui.list_data.setDragEnabled(True)
        self.ui.list_data.setAcceptDrops(True)
        self.ui.list_data.setDropIndicatorShown(True)

        self.data_map = {}
        self.yaml_config = YamlConfig(
            parent=self,
            ui=self.ui,
            data_map=self.data_map,
            group_manager=self.group_manager
        )

        self.ui.button_top_import.clicked.connect(
            self.yaml_config.import_folder
        )

        self.yaml_config.log_signal.connect(self.log)
        self.yaml_config.setup_auto_save_connections()

        self.ui.line_prj.setReadOnly(True)

    def group_changed(self, index):
        if index < 0:
            self.current_group = None
            self.ui.list_group.clear()
            return

        new_group = self.ui.combo_box_group.currentText()

        if new_group == self.group_manager.current_group:
            return

        if self.group_manager.current_group is not None:
            self.group_manager.save_current_group_data()

        self.group_manager.current_group = new_group
        self.group_manager.load_group_data(new_group)

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

    # Send the frame and receive the response
    def scan_device(self):
        if not hasattr(self, 'spi_device') or not self.spi_device:
            self.log("SPI设备未连接", 2)
            return

        if hasattr(self, 'scan_device_thread') and self.scan_device_thread.isRunning():
            self.log("扫描正在进行中，请稍候...", 0)
            return

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_input = 1.0
            self.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        self.scan_device_thread = ScanDeviceThread(
            parent=self, 
            delay=delay_input
        )

        self.scan_device_thread.log_signal.connect(self.log)

        self.scan_device_thread.start()

    # Only parse the payload but not the Caselist
    def scan_case(self):
        if not hasattr(self, 'spi_device') or not self.spi_device:
            self.log("SPI设备未连接", 2)
            return        

        if hasattr(self, 'scan_case_thread') and self.scan_case_thread.isRunning():
            self.log("扫描正在进行中，请稍候...", 0)
            return

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0

        if delay_value <= 0:
            delay_input = 1.0
            self.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        self.scan_case_thread = ScanInstanceThread(
            parent=self, 
            delay=delay_input
        )

        self.scan_case_thread.log_signal.connect(self.log)

        self.scan_case_thread.start()

    # Change the project name
    def handle_rename_button(self):
        current_index = self.ui.combo_box_data_group.currentIndex()

        if current_index >= 0:
            current_text = self.ui.combo_box_data_group.currentText().strip()
            self.name_window = SubWindowName(self, current_text)
            self.name_window.name_updated.connect(lambda new_name: self.on_name_updated(new_name, current_index))
            self.name_window.show()

    # Update the project name
    def on_name_updated(self, new_name, index=None):
        if index is not None and 0 <= index < self.ui.combo_box_data_group.count():
            self.ui.combo_box_data_group.setItemText(index, new_name)
        # if hasattr(self.ui, 'line_prj'):
        #     self.ui.line_prj.setText(new_name)

    # Handle radio button click event
    def on_radio_button_clicked(self):
        if self.ui.radio_button_order.isChecked():
            self.ui.line_number.setEnabled(False)
        else:
            self.ui.line_number.setEnabled(True)
    
    # Send the selected data items
    def sending_mode(self):
        if self.is_sending:
            QMessageBox.warning(self, '警告', '发送正在进行中，请先停止当前发送任务')
            return
         
        try:
            delay = float(self.ui.line_delay.text())
            if delay < 0:
                QMessageBox.warning(self, '警告', '延迟时间设置失败')
                return
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的延迟时间')
            return

        item_send = []

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
            self.worker_thread.set_params(delay, item_send, "order")
        elif self.ui.radio_button_circ.isChecked():
            try:
                cycles = int(self.ui.line_number.text())
                if cycles <= 0:
                    QMessageBox.warning(self, '警告', '循环次数设置失败')
                    return
                self.worker_thread.set_params(delay, item_send, "circ", cycles=cycles)
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入有效的循环次数')
                return
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
        
        self.update_all_crc_tooltips()

    # Update CRC tooltip when combo box selection changes
    def update_all_crc_tooltips(self):
        for i in range(self.ui.list_data.count()):
            item = self.ui.list_data.item(i)
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
            item.setToolTip("")

    # Setting spi combo box items
    def spi_combo_box(self):
        if hasattr(self, 'signals_connected') and self.signals_connected:
            self.ui.combo_box_vcc.currentIndexChanged.disconnect(self.vcc_changed)
            self.ui.combo_box_io.currentIndexChanged.disconnect(self.io_changed)
            self.ui.combo_box_speed.currentIndexChanged.disconnect(self.speed_changed)
            self.ui.combo_box_clk.currentIndexChanged.disconnect(self.clk_changed)
            self.ui.combo_box_bit.currentIndexChanged.disconnect(self.bit_changed)
            self.ui.combo_box_s_or_q.currentIndexChanged.disconnect(self.s_or_q_changed)
            self.ui.combo_box_size.currentIndexChanged.disconnect(self.size_changed)
            self.signals_connected = False

        self.ui.combo_box_vcc.addItem("5V", 0)
        self.ui.combo_box_vcc.addItem("=IO", 1)
        self.ui.combo_box_vcc.addItem("关闭", 2)

        self.ui.combo_box_io.addItem("3.3V", 0)
        self.ui.combo_box_io.addItem("1.8V", 1)

        self.ui.combo_box_speed.addItem("468.75K", 0)
        self.ui.combo_box_speed.addItem("937.5K", 1)
        self.ui.combo_box_speed.addItem("1.875M", 2)
        self.ui.combo_box_speed.addItem("3.75M", 3)
        self.ui.combo_box_speed.addItem("7.5M", 4)
        self.ui.combo_box_speed.addItem("15M", 5)
        self.ui.combo_box_speed.addItem("30M", 6)
        self.ui.combo_box_speed.addItem("60M", 7)

        self.ui.combo_box_clk.addItem("LOW/1EDG", 0)
        self.ui.combo_box_clk.addItem("LOW/2EDG", 1)
        self.ui.combo_box_clk.addItem("HIGH/1EDG", 2)
        self.ui.combo_box_clk.addItem("HIGH/2EDG", 3)

        self.ui.combo_box_bit.addItem("MSB", 0)
        self.ui.combo_box_bit.addItem("LSB", 1)

        self.ui.combo_box_s_or_q.addItem("全单线SPI", 0)

        self.ui.combo_box_size.addItem("2字节", 0)
        self.ui.combo_box_size.addItem("4字节", 1)
        self.ui.combo_box_size.addItem("8字节", 2)
        self.ui.combo_box_size.addItem("16字节", 3)
        self.ui.combo_box_size.addItem("32字节", 4)
        self.ui.combo_box_size.addItem("64字节", 5)

        self.ui.combo_box_vcc.currentIndexChanged.connect(self.vcc_changed)
        self.ui.combo_box_io.currentIndexChanged.connect(self.io_changed)
        self.ui.combo_box_speed.currentIndexChanged.connect(self.speed_changed)
        self.ui.combo_box_clk.currentIndexChanged.connect(self.clk_changed)
        self.ui.combo_box_bit.currentIndexChanged.connect(self.bit_changed)
        self.ui.combo_box_s_or_q.currentIndexChanged.connect(self.s_or_q_changed)
        self.ui.combo_box_size.currentIndexChanged.connect(self.size_changed)

        self.ui.combo_box_vcc.setCurrentIndex(2)
        self.ui.combo_box_io.setCurrentIndex(1)
        self.ui.combo_box_speed.setCurrentIndex(1)

        self.signals_connected = True

        if hasattr(self, 'spi_device') and self.spi_device:
            self.clk_changed(self.ui.combo_box_clk.currentIndex())
            self.bit_changed(self.ui.combo_box_bit.currentIndex())
            self.s_or_q_changed(self.ui.combo_box_s_or_q.currentIndex())
            self.size_changed(self.ui.combo_box_size.currentIndex())

    # Clear all combo boxes if spi device is not connected
    def clear_combo_boxes(self):
        if hasattr(self, 'content_initialized') and self.content_initialized:
            self.ui.combo_box_vcc.clear()
            self.ui.combo_box_io.clear()
            self.ui.combo_box_speed.clear()
            self.ui.combo_box_clk.clear()
            self.ui.combo_box_bit.clear()
            self.ui.combo_box_s_or_q.clear()
            self.ui.combo_box_size.clear()
            self.content_initialized = False

    # Setting vcc value
    def vcc_changed(self, index, log_set = True):
        if hasattr(self, 'spi_device') and self.spi_device and self.spi_device.dev_handle:
            try:
                result = self.spi_device.jtool.JSPISetVcc(
                    self.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.log(f"VCC设置失败,{SPI.ERROR_CODES.get(result)}", 2)

                if log_set:
                    self.log(f"VCC设置为: {self.ui.combo_box_vcc.currentText()}")

                self.yaml_config.auto_save_config()

            except Exception as e:
                self.log(f"VCC设置失败: {str(e)}", 2)

    # Setting io value
    def io_changed(self, index, log_set = True):
        if hasattr(self, 'spi_device') and self.spi_device and self.spi_device.dev_handle:
            try:
                result = self.spi_device.jtool.JSPISetVio(
                    self.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.log(f"IO电压设置失败,{SPI.ERROR_CODES.get(result)}", 2)
                    
                if log_set:
                    self.log(f"IO电压设置为: {self.ui.combo_box_io.currentText()}")

                self.yaml_config.auto_save_config()

            except Exception as e:
                self.log(f"IO电压设置失败: {str(e)}", 2)

    # Setting speed value
    def speed_changed(self, index, log_set = True):
        if hasattr(self, 'spi_device') and self.spi_device and self.spi_device.dev_handle:
            try:
                result = self.spi_device.jtool.JSPISetSpeed(
                    self.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.log(f"SPI速度设置失败,{SPI.ERROR_CODES.get(result)}", 2)
                
                if log_set:
                    self.log(f"SPI速度设置为: {self.ui.combo_box_speed.currentText()}")

                self.yaml_config.auto_save_config()

            except Exception as e:
                self.log(f"SPI速度设置失败: {str(e)}", 2)

    # Setting clk value
    def clk_changed(self, index, log_set = True):
        self.spi_clk_mode = index
        if self.content_initialized and self.spi_device is not None:
            if log_set:
                self.log(f"SPI时钟模式设置为: {self.ui.combo_box_clk.currentText()}")

            self.yaml_config.auto_save_config()

    # Setting bit order value
    def bit_changed(self, index, log_set = True):
        self.spi_bit_order = index
        if self.content_initialized and self.spi_device is not None:
            if log_set:
                self.log(f"SPI位序设置为: {self.ui.combo_box_bit.currentText()}")

            self.yaml_config.auto_save_config()

    # Setting spi mode value
    def s_or_q_changed(self, index, log_set = True):
        self.spi_mode = index
        if self.content_initialized and self.spi_device is not None:
            if log_set:
                self.log(f"SPI模式设置为: {self.ui.combo_box_s_or_q.currentText()}")
            self.yaml_config.auto_save_config()

    # Setting receive data size value
    def size_changed(self, index, log_set = True):
        if index == 0:
            self.spi_rx_size = 2
        elif index == 1:
            self.spi_rx_size = 4
        elif index == 2:
            self.spi_rx_size = 8
        elif index == 3:
            self.spi_rx_size = 16
        elif index == 4:
            self.spi_rx_size = 32
        elif index == 5:
            self.spi_rx_size = 64
        
        if self.content_initialized and self.spi_device is not None:
            if log_set:
                self.log(f"接收数据字节数设置为: {self.ui.combo_box_size.currentText()}")

            self.yaml_config.auto_save_config()

    # Open sub window for adding SPI text data
    def add_text(self):
        self.sub_window = SubWindowSpiText(self)
        self.sub_window.signal.connect(self.mainwindow_data)
        self.sub_window.show()
        self.yaml_config.auto_save_config()

    # Delete selected text item from list
    def delete_text(self):
        selected_items = self.ui.list_data.selectedItems()
        if not selected_items:
            return

        reply = QMessageBox.information(
            self, 'Tip', '是否删除选中项？',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Ok:
            for item in selected_items:
                data_pair = item.data(Qt.UserRole)
                if data_pair and data_pair[0] in self.data_map:
                    del self.data_map[data_pair[0]]

                row = self.ui.list_data.row(item)
                button = self.ui.list_data.itemWidget(item)
                if button:
                    button.deleteLater()
                self.ui.list_data.takeItem(row)

            # self.auto_save_config()

    # Open sub window for adding SPI text data and user_defined listwidget item
    def mainwindow_data(self, data_name, data_text, show_all=True):
        def is_valid_hex(text):
            parts = text.strip().split()
            if not parts:
                return False
            
            valid_chars = set('0123456789abcdefABCDEF')
            for part in parts:
                if len(part) > 2 or not all(char in valid_chars for char in part):
                    return False
            return True

        if not is_valid_hex(data_text):
            QMessageBox.critical(
                self, '错误', '请输入正确的格式，如00 00 00.'
            )
            return

        item = QListWidgetItem()
        item.setData(Qt.UserRole, (data_name, data_text))
        self.ui.list_data.addItem(item)
        self.data_map[data_name] = data_text

        list_item_widget = User_ListItemWidget(
            self.ui.list_data,
            data_name,
            data_text,
            show_all,
            checkable= False
        )

        list_item_widget.set_user_data(item)

        list_item_widget.send_clicked.connect(self.spi_send_item)
        # list_item_widget.check_state_changed.connect(self.on_item_check_state_changed)

        self.ui.list_data.setItemWidget(item, list_item_widget)

        self.update_all_crc_tooltips()

        self.yaml_config.auto_save_config()

    # def on_item_check_state_changed(self, item, state):
    #     item.setData(Qt.UserRole + 1, state)

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

        try:
            for part in hex_parts:
                data_bytes.append(int(part, 16))
        except ValueError:
            QMessageBox.warning(self, '警告', "输入包含非十六进制字符")
            return

        if not hasattr(self, 'spi_device') and not self.spi_device:
            self.log("未发现SPI设备", 2)
            return

        if self.spi_device.jtool is None or self.spi_device.dev_handle is None:
            if not self.spi_device.open_device():
                self.log("SPI设备连接失败", 2)
                return
        
        result = self.spi_device.spi_send(
            data_bytes,self.spi_clk_mode,
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

    # # Monitor SPI device connection status
    def monitor_spi_devices(self):
        if not hasattr(self, 'temp_scanner') or self.temp_scanner is None:
            self.temp_scanner = SPI(log_callback=self.log)

        if self.temp_scanner.jtool is None:
            return

        dev_cnt = c_int(0)
        self.temp_scanner.jtool.DevicesScan(self.temp_scanner.dev_spi, byref(dev_cnt))
        current_cnt = dev_cnt.value

        if self.last_device_cnt == -1:
            self.last_device_cnt = current_cnt
            if current_cnt > 0:
                self.handle_device_connected(current_cnt)
            return
        
        if current_cnt > 0 and self.last_device_cnt == 0:
            self.handle_device_connected(current_cnt)
        elif current_cnt == 0 and self.last_device_cnt > 0:
            self.handle_device_disconnected()

        self.last_device_cnt = current_cnt

    def handle_device_connected(self, device_count):
        self.log(f"发现 {device_count} 个 SPI 设备")

        if not hasattr(self, 'spi_device') or self.spi_device is None:
            self.spi_device = SPI(log_callback=self.log)
        
        if self.spi_device.open_device() and not self.content_initialized:
            device_name = self.spi_device.get_device_name()
            self.spi_combo_box()
            self.ui.line_device.setText(str(device_name))
            self.content_initialized = True

    def handle_device_disconnected(self):
        self.log("设备已断开", 2)
        self.spi_device = None
        self.clear_combo_boxes()
        self.ui.line_device.clear()
        self.content_initialized = False

    # Stop device monitoring timer
    def stop_device_monitor(self):
        if hasattr(self, 'device_monitor_timer'):
            self.device_monitor_timer.stop()

    # Continue device monitoring
    def continue_monitor(self):
        self.monitor_spi_devices()

    # Initialize SPI device monitoring
    def init_spi_monitoring(self):
        self.spi_device = None
        self.temp_scanner = SPI(log_callback=self.log)
        self.device_monitor_timer = QTimer(self)
        self.device_monitor_timer.timeout.connect(
            self.monitor_spi_devices
        )
        self.device_monitor_timer.start(1000)
        self.last_device_cnt = -1
        self.signals_connected = False

    # Send data which in the line edit
    def spi_send_line(self):
        raw_text = self.ui.line_edit_data.text().strip()
        
        if not raw_text:
            self.log("请输入要发送的数据", 2)
            return

        data_bytes = []

        try:
            clean_text = ''.join(c for c in raw_text if c in '0123456789ABCDEFabcdef')

            if len(clean_text) % 2 != 0:
                clean_text = '0' + clean_text

            for i in range(0, len(clean_text), 2):
                data_bytes.append(int(clean_text[i:i+2], 16))
        except ValueError:
            QMessageBox.warning(self, '警告', "输入包含非十六进制字符")
            return
        
        if self.current_crc_mode == 0:

            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            data_bytes.append(crc_high)
            data_bytes.append(crc_low)

        if not hasattr(self, 'spi_device') or not self.spi_device:
            self.log("未发现SPI设备", 2)
            return
        
        if self.spi_device.jtool is None or self.spi_device.dev_handle is None:
            if not self.spi_device.open_device():
                self.log("SPI设备连接失败", 2)
                return
        
        result = self.spi_device.spi_send(
            data_bytes, self.spi_clk_mode,
            self.spi_bit_order
        )

        if result:
            self.log(f"发送成功: {' '.join([f'{byte:02X}' for byte in data_bytes])}", 1)
        else:
            self.log("数据发送失败", 2)

    def spi_receive(self):
        if self.ui.check_box_receive.isChecked() is False:
            self.log("请先勾选接收数据", 2)
            return

        received_data = self.spi_device.spi_receive(
            self.spi_clk_mode,
            self.spi_bit_order,
            self.spi_rx_size
        )
        
        if received_data is None:
            self.log("数据接收失败", 2)
            return
        
        formatted_data = ' '.join([f"{byte:02X}" for byte in received_data])

        self.log(f"数据接收: {formatted_data}", 1)

    def import_config(self):
            self.yaml_config.import_config()

    def export_config(self):
        self.yaml_config.export_config()
