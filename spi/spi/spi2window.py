#!/usr/bin/env python3.13
"""
filename: spi2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-01
description: SPI connection main window, handling SPI related UI connections and logic
"""

from PySide6.QtCore import QObject
from ctypes import c_int, byref
from .spi_jtool import SPI
from crc.crc import CRC

class SPI2Window(QObject):
    """
        SPI connection main window class, 
        handling SPI related UI connections and business logic
    """
    
    def __init__(self, main_window):
        """
            Initialize the SPI connection main window
            
            Args:
                main_window: The main window instance
        """
        super().__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.setup_connections()
    
    def setup_connections(self):
        """
            Set up connections for SPI related controls
        """

        # Connect SPI related buttons
        self.ui.button_send.clicked.connect(self.spi_send_line)
        self.ui.button_receive.clicked.connect(self.spi_receive)

    # Send data which in the line edit
    def spi_send_line(self):
        """
            Send data which in the line edit
        """

        # Get the data from line edit
        raw_text = self.ui.line_edit_data.text().strip()
        
        if not raw_text:
            self.main_window.log("请输入要发送的数据", 2)
            return

        data_bytes = []

        # Clear illegal characters
        clean_text = ''.join(c for c in raw_text if c in '0123456789ABCDEFabcdef')

        # Add leading zero if length is odd
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # Convert hex string to bytes
        for i in range(0, len(clean_text), 2):
            data_bytes.append(int(clean_text[i:i+2], 16))
        
        if self.main_window.current_crc_mode == 0:
            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            data_bytes.append(crc_high)
            data_bytes.append(crc_low)

        # Check if SPI device is connected
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("未发现SPI设备", 2)
            return
        
        if self.main_window.spi_device.jtool is None or self.main_window.spi_device.dev_handle is None:
            if not self.main_window.spi_device.open_device():
                self.main_window.log("SPI设备连接失败", 2)
                return
        
        result = self.main_window.spi_device.spi_send(
            data_bytes, self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order
        )

        if result:
            self.main_window.log(f"发送成功: {' '.join([f'{byte:02X}' for byte in data_bytes])}", 1)
        else:
            self.main_window.log("数据发送失败", 2)
    
    def spi_receive(self):
        """
            Receive data from SPI device
        """
        
        # Check if is receive mode
        if self.ui.check_box_receive.isChecked() is False:
            self.main_window.log("请先勾选接收数据", 2)
            return

        # Start receive data
        received_data = self.main_window.spi_device.spi_receive(
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order,
            self.main_window.spi_rx_size
        )
        
        if received_data is None:
            self.main_window.log("数据接收失败", 2)
            return
        
        formatted_data = ' '.join([f"{byte:02X}" for byte in received_data])

        self.main_window.log(f"数据接收: {formatted_data}", 1)
    
    # Setting vcc value
    def vcc_changed(self, index):
        if hasattr(self.main_window, 'spi_device') and self.main_window.spi_device and self.main_window.spi_device.dev_handle:
            try:
                result = self.main_window.spi_device.jtool.JSPISetVcc(
                    self.main_window.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.main_window.log(f"VCC设置失败,{SPI.ERROR_CODES.get(result)}", 2)

                self.main_window.log(f"VCC设置为: {self.ui.combo_box_vcc.currentText()}")

            except Exception as e:
                self.main_window.log(f"VCC设置失败: {str(e)}", 2)

    # Setting io value
    def io_changed(self, index):
        if hasattr(self.main_window, 'spi_device') and self.main_window.spi_device and self.main_window.spi_device.dev_handle:
            try:
                result = self.main_window.spi_device.jtool.JSPISetVio(
                    self.main_window.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.main_window.log(f"IO电压设置失败,{SPI.ERROR_CODES.get(result)}", 2)
                    
                self.main_window.log(f"IO电压设置为: {self.ui.combo_box_io.currentText()}")

            except Exception as e:
                self.main_window.log(f"IO电压设置失败: {str(e)}", 2)

    # Setting speed value
    def speed_changed(self, index):
        if hasattr(self.main_window, 'spi_device') and self.main_window.spi_device and self.main_window.spi_device.dev_handle:
            try:
                result = self.main_window.spi_device.jtool.JSPISetSpeed(
                    self.main_window.spi_device.dev_handle, c_int(index)
                )
                if result != 0:
                    self.main_window.log(f"SPI速度设置失败,{SPI.ERROR_CODES.get(result)}", 2)
                
                self.main_window.log(f"SPI速度设置为: {self.ui.combo_box_speed.currentText()}")

            except Exception as e:
                self.main_window.log(f"SPI速度设置失败: {str(e)}", 2)

    # Setting clk value
    def clk_changed(self, index):
        self.main_window.spi_clk_mode = index
        if self.main_window.content_initialized and self.main_window.spi_device is not None:
            self.main_window.log(f"SPI时钟模式设置为: {self.ui.combo_box_clk.currentText()}")

    # Setting bit order value
    def bit_changed(self, index):
        self.main_window.spi_bit_order = index
        if self.main_window.content_initialized and self.main_window.spi_device is not None:
            self.main_window.log(f"SPI位序设置为: {self.ui.combo_box_bit.currentText()}")

    # Setting spi mode value
    def s_or_q_changed(self, index):
        self.main_window.spi_mode = index
        if self.main_window.content_initialized and self.main_window.spi_device is not None:
            self.main_window.log(f"SPI模式设置为: {self.ui.combo_box_s_or_q.currentText()}")

    # Setting receive data size value
    def size_changed(self, index):
        if index == 0:
            self.main_window.spi_rx_size = 2
        elif index == 1:
            self.main_window.spi_rx_size = 4
        elif index == 2:
            self.main_window.spi_rx_size = 8
        elif index == 3:
            self.main_window.spi_rx_size = 16
        elif index == 4:
            self.main_window.spi_rx_size = 32
        elif index == 5:
            self.main_window.spi_rx_size = 64
        
        if self.main_window.content_initialized and self.main_window.spi_device is not None:
            self.main_window.log(f"接收数据字节数设置为: {self.ui.combo_box_size.currentText()}")

    # Setting spi combo box items
    def spi_combo_box(self):
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

    # Clear all combo boxes if spi device is not connected
    def clear_combo_boxes(self):
        if hasattr(self.main_window, 'content_initialized') and self.main_window.content_initialized:
            self.ui.combo_box_vcc.clear()
            self.ui.combo_box_io.clear()
            self.ui.combo_box_speed.clear()
            self.ui.combo_box_clk.clear()
            self.ui.combo_box_bit.clear()
            self.ui.combo_box_s_or_q.clear()
            self.ui.combo_box_size.clear()
            self.main_window.content_initialized = False

    # Monitor SPI device connection status
    def monitor_spi_devices(self):
        if not hasattr(self.main_window, 'temp_scanner') or self.main_window.temp_scanner is None:
            self.main_window.temp_scanner = SPI(log_callback=self.main_window.log)

        if self.main_window.temp_scanner.jtool is None:
            return

        dev_cnt = c_int(0)
        self.main_window.temp_scanner.jtool.DevicesScan(self.main_window.temp_scanner.dev_spi, byref(dev_cnt))
        current_cnt = dev_cnt.value

        if self.main_window.last_device_cnt == -1:
            self.main_window.last_device_cnt = current_cnt
            if current_cnt > 0:
                self.handle_device_connected(current_cnt)
            return
        
        if current_cnt > 0 and self.main_window.last_device_cnt == 0:
            self.handle_device_connected(current_cnt)
        elif current_cnt == 0 and self.main_window.last_device_cnt > 0:
            self.handle_device_disconnected()

        self.main_window.last_device_cnt = current_cnt

    def handle_device_connected(self, device_count):
        self.main_window.log(f"发现 {device_count} 个 SPI 设备")

        if not hasattr(self.main_window, 'spi_device') or self.main_window.spi_device is None:
            self.main_window.spi_device = SPI(log_callback=self.main_window.log)
        
        if self.main_window.spi_device.open_device() and not self.main_window.content_initialized:
            device_name = self.main_window.spi_device.get_device_name()
            self.spi_combo_box()
            self.ui.line_device.setText(str(device_name))
            self.main_window.content_initialized = True

    def handle_device_disconnected(self):
        self.main_window.log("设备已断开", 2)
        self.main_window.spi_device = None
        self.clear_combo_boxes()
        self.ui.line_device.clear()
        self.widget_disconnect()
        self.main_window.content_initialized = False

    # Stop device monitoring timer
    def stop_device_monitor(self):
        if hasattr(self.main_window, 'device_monitor_timer'):
            self.main_window.device_monitor_timer.stop()

    # Continue device monitoring
    def continue_monitor(self):
        self.monitor_spi_devices()

    def widget_disconnect(self):
        self.ui.combo_box_vcc.currentIndexChanged.disconnect(self.vcc_changed)
        self.ui.combo_box_io.currentIndexChanged.disconnect(self.io_changed)
        self.ui.combo_box_speed.currentIndexChanged.disconnect(self.speed_changed)
        self.ui.combo_box_clk.currentIndexChanged.disconnect(self.clk_changed)
        self.ui.combo_box_bit.currentIndexChanged.disconnect(self.bit_changed)
        self.ui.combo_box_s_or_q.currentIndexChanged.disconnect(self.s_or_q_changed)
        self.ui.combo_box_size.currentIndexChanged.disconnect(self.size_changed)
        
