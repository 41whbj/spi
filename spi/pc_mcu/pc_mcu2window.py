#!/usr/bin/env python3.13
"""
filename: pc_mcu2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-02
description: PC-MCU connection main window, handling PC-MCU related UI connections and logic
"""

from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from PySide6.QtCore import QObject
from .scan_device import ScanDeviceThread
from .scan_instance import ScanInstanceThread
from .case_manager import CaseID_Manager, CaseItemWidget
from .frame import Frame, CMD

class PC_MCU2Window(QObject):
    """
        PC_MCU connection main window class, 
        responsible for handling the UI connections and business logic 
        related to PC-MCU
    """
    
    def __init__(self, main_window):
        """
            Init PC_MCU connection window
            
            Args:
                main_window: MainWindow instance
        """
        super().__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.case_manager = CaseID_Manager()
        self.setup_connections()
    
    def setup_connections(self):
        """
            Set up connections for PC_MCU related controls
        """
        # Connect signal for "Connect" button
        self.ui.button_mcu_connect.clicked.connect(self.scan_device)
        # Connect signal for "Scan" button
        self.ui.button_mcu_scan.clicked.connect(self.scan_case)
        self.ui.button_mcu_log.clicked.connect(self.ask_log)
        self.ui.button_mcu_rx.clicked.connect(self.rx_test)

        # Test
        # self.ui.button_mcu_scan.clicked.connect(self.test)

    # def test(self):
    #     """
    #         Test function
    #     """
    #     case_list_test = ['Case1', 'Case2', 'Case3']

    #     self.handle_scan_case_result(case_list_test)

    def scan_device(self):
        """
            Scan device function
        """

        # Check if SPI device is connected
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return

        # Check if scan device thread is running
        if hasattr(self, 'scan_device_thread') and self.scan_device_thread.isRunning():
            self.main_window.log("扫描正在进行中，请稍候...", 0)
            return

        # Test 
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_input = 1.0
            self.main_window.log("使用默认值1秒", 1) # TODO
        else:
            delay_input = delay_value

        # Start scan device thread
        self.scan_device_thread = ScanDeviceThread(
            parent=self.main_window, 
            delay=delay_input
        )

        self.scan_device_thread.log_signal.connect(self.main_window.log)
        self.scan_device_thread.start()
    
    def scan_case(self):
        """
            Scan instance function
        """
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return        

        if hasattr(self, 'scan_case_thread') and self.scan_case_thread.isRunning():
            self.main_window.log("扫描正在进行中，请稍候...", 0)
            return

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0

        if delay_value <= 0:
            delay_input = 1.0
            self.main_window.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        self.scan_case_thread = ScanInstanceThread(
            parent=self.main_window, 
            delay=delay_input
        )

        # Signal connection
        self.scan_case_thread.case_signal.connect(self.handle_scan_case_result)
        self.scan_case_thread.log_signal.connect(self.main_window.log)
        self.scan_case_thread.start()
    
    def handle_scan_case_result(self, case_list):
        """
            Handle scan case result, add case to MCU_list_case
        """

        if not case_list:
            self.main_window.log("未扫描到任何负载", 1)
            return

        self.ui.MCU_list_case.clear()
        
        self.case_manager.assign_id(case_list)
        processed_case = self.case_manager.get_processed_case()

        print(f"processed_case: {processed_case}")
        
        if processed_case is None:
            self.main_window.log("没有处理任何case", 1)
            return
        
        for name, id_bytes in processed_case.items():
            case_item = CaseItemWidget(name, id_bytes, use_crc=getattr(self.main_window, 'current_crc_mode', 0) == 0)

            case_item.send_frame.connect(self.send_frame)

            list_item = QListWidgetItem()
            self.ui.MCU_list_case.addItem(list_item)
            self.ui.MCU_list_case.setItemWidget(list_item, case_item)
            
            list_item.setSizeHint(case_item.sizeHint())
            
        self.main_window.log(f"成功添加 {len(processed_case)} 个负载到列表", 0)

    def send_frame(self, frame, correct):
        """
            Send frame to MCU by SPI
        """
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return
        
        if correct is False:
            QMessageBox.warning(self.main_window, "警告", "请输入正确的数据")
            return
        
        result = self.main_window.spi_device.spi_send(
            frame,
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order
        )

        if result is not True:
            self.main_window.log("数据发送失败", 2)
            return

        data = ' '.join([f"{byte:02X}" for byte in frame])

        self.main_window.log(f"发送成功，数据: {data}",1)

    def ask_log(self):
        """
            Scan device function
        """

        # Check if SPI device is connected
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return

        if self.main_window.current_crc_mode == 0:
            send_data = Frame.generate_frame(CMD["Getlog"], use_crc=True)
        else:
            send_data = Frame.generate_frame(CMD["Getlog"])

        self.main_window.spi_device.spi_send(
            send_data,
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order
        )

        self.main_window.log(f"send_data: {send_data.hex()}", 0)

    def rx_test(self):
        """
            test received log data
        """

        # Check if SPI device is connected
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return
                # Provide a 128-byte receiving area
        received_data = self.main_window.spi_device.spi_receive(
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order,
            128
        )
        
        self.main_window.log(f"测试接收128字节数据：received_data: {received_data.hex()}", 0)

        if self.main_window.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # Parse receive frame
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        if success is False:
            self.main_window.log(f"获取实例失败：{result}", 2)
            return
        
        if cmd != (CMD["Log"] or CMD["CaseResult"]):
            self.main_window.log("命令字错误", 2)
            return
        
        self.main_window.log(f"原始负载: {payload.hex()}", 1)
        # print(payload)

        log = Frame.parse_normally(payload)

        self.main_window.log(f"负载提取: {log}", 1)
