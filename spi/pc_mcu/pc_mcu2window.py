#!/usr/bin/env python3.13
"""
filename: pc_mcu2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-02
description: PC-MCU connection main window, handling PC-MCU related UI connections and logic
"""

from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from PySide6.QtCore import QObject, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .scan_device import ScanDeviceThread
from .scan_instance import ScanInstanceThread
from .case_manager import CaseID_Manager, CaseItemWidget
from .frame import Frame, CMD
from .test_thread import CycleSendThread
from log_manager.log import CsvManager

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
        self.log_manager = []
        self.setup_drop()
        self.log = CsvManager()

        self.is_cycle_sending = False

    def start_cycle_send(self):
        """
            启动循环发送功能
        """
        # 检查SPI设备是否连接
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return
        
        # 检查是否已经在发送
        if self.is_cycle_sending:
            self.main_window.log("循环发送正在进行中，请先停止当前发送任务", 0)
            return
        
        # 检查MCU_list_case是否为空
        if self.ui.MCU_list_case.count() == 0:
            self.main_window.log("没有可发送的测试用例，请先扫描", 1)
            return
        
        # 获取延迟值
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_value = 1.0
            self.main_window.log("使用默认值1秒作为发送间隔", 1)
        
        # 创建并启动循环发送线程
        self.cycle_send_thread = CycleSendThread(
            parent=self
        )
        
        self.cycle_send_thread.log_signal.connect(self.main_window.log)
        self.cycle_send_thread.finished.connect(self.on_cycle_send_finished)
        self.cycle_send_thread.receive_data_signal.connect(self.case_result_parse)
        
        self.is_cycle_sending = True
        
        # 更新UI状态
        self.ui.MCU_button_send.setEnabled(False)
        self.ui.MCU_button_stop.setEnabled(True)
        
        self.main_window.log("开始循环发送测试用例...", 0)
        self.cycle_send_thread.start()
    
    def stop_cycle_send(self):
        """
            停止循环发送功能
        """
        if self.cycle_send_thread and self.cycle_send_thread.isRunning():
            self.main_window.log("正在停止循环发送任务...", 0)
            self.cycle_send_thread.stop()
    
    def on_cycle_send_finished(self):
        """
            循环发送线程结束后的处理
        """
        self.is_cycle_sending = False
        # 更新UI状态
        self.ui.MCU_button_send.setEnabled(True)
        self.ui.MCU_button_stop.setEnabled(False)
        self.main_window.log("循环发送任务已完成或终止", 0)
    
    def setup_connections(self):
        """
            Set up connections for PC_MCU related controls
        """
        # Connect signal for "Connect" button
        self.ui.button_mcu_connect.clicked.connect(self.scan_device)
        # Connect signal for "Scan" button
        self.ui.button_mcu_scan.clicked.connect(self.scan_case)
        # self.ui.button_mcu_log.clicked.connect(self.ask_log)
        # self.ui.button_mcu_rx.clicked.connect(self.rx_test)
        self.ui.MCU_button_send.clicked.connect(self.start_cycle_send)
        self.ui.MCU_button_stop.clicked.connect(self.stop_cycle_send)

        # Test
        # self.ui.button_mcu_scan.clicked.connect(self.test)

    def test(self):
        """
            Test function
        """
        case_list_test = ['Case1', 'Case2', 'Case3']

        self.handle_scan_case_result(case_list_test)

    def setup_drop(self):
        """
            Set up fuction for MCU_list_case drop out
        """
        self.ui.MCU_list_case.setDragEnabled(True)
        self.ui.MCU_list_case.setAcceptDrops(False)
        self.ui.MCU_list_case.setDropIndicatorShown(True)

        # 设置MCU_list_test支持接收拖拽项目
        # self.ui.MCU_list_test.setDragEnabled(True)
        self.ui.MCU_list_test.setAcceptDrops(True)
        self.ui.MCU_list_test.setDropIndicatorShown(True)
        self.ui.MCU_list_test.dragEnterEvent = self.test_list_drag_enter_event
        self.ui.MCU_list_test.dragMoveEvent = self.test_list_drag_move_event
        self.ui.MCU_list_test.dropEvent = self.test_list_drop_event

    
    def test_list_drag_enter_event(self, event: QDragEnterEvent):
        """处理拖拽进入事件"""
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drag_move_event(self, event: QDragEnterEvent):
        """处理拖拽移动事件"""
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drop_event(self, event: QDropEvent):
        """处理拖拽释放事件"""
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            # 获取被拖拽的项目
            source = event.source()
            if source == self.ui.MCU_list_case:
                # 从MCU_list_case拖拽到MCU_list_test
                selected_items = source.selectedItems()
                for item in selected_items:
                    # 复制项目到MCU_list_test
                    self.copy_item_to_test_list(item)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def copy_item_to_test_list(self, source_item):
        """复制项目到测试列表"""
        # 获取原始的CaseItemWidget
        source_widget = self.ui.MCU_list_case.itemWidget(source_item)

        test_item_widget = CaseItemWidget(
            name=source_widget.name,
            id=source_widget.id,
            use_crc=source_widget.use_crc,
            mode="Test"
        )
        
        # 连接信号（如果需要的话）
        # 这里可以根据需要添加信号连接
        test_item_widget.delete_requested.connect(self.remove_test_item)
        
        # 创建新的列表项
        list_item = QListWidgetItem()
        self.ui.MCU_list_test.addItem(list_item)
        self.ui.MCU_list_test.setItemWidget(list_item, test_item_widget)
        list_item.setSizeHint(test_item_widget.sizeHint())

    def remove_test_item(self, test_item_widget):
        """从测试列表中移除项目"""
        # 查找项目在列表中的索引
        for index in range(self.ui.MCU_list_test.count()):
            item = self.ui.MCU_list_test.item(index)
            widget = self.ui.MCU_list_test.itemWidget(item)
            if widget == test_item_widget:
                # 移除项目
                self.ui.MCU_list_test.takeItem(index)
                del item
                break

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

        self.case_manager.clear_processed_case()

        if not case_list:
            self.main_window.log("未扫描到任何负载", 1)
            return

        self.ui.MCU_list_case.clear()
        
        self.case_manager.assign_id(case_list)
        processed_case = self.case_manager.get_processed_case()

        # print(f"processed_case: {processed_case}")
        
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
            
        self.main_window.log(f"获取 {len(processed_case)} 个测例", 1)

    def send_frame(self, frame, correct):
        """
            Send frame to MCU by SPI
        """
        self.main_window.log("发送成功", 1)

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
            print("数据发送失败", 2)
            return

        data = ' '.join([f"{byte:02X}" for byte in frame])

        print(f"发送成功，数据: {data}")

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 3.0

        if delay_value <= 0:
            delay_input = 3.0
            print("使用默认值3秒", 1)
        else:
            delay_input = delay_value

        QTimer.singleShot(int(delay_value * 1000), self.receive_data)

    def receive_data(self):
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return

        received_data = self.main_window.spi_device.spi_receive(
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order,
            1024
        )

        self.case_result_parse(received_data)
        
        # self.main_window.log(f"测试接收1024字节数据：received_data: {received_data.hex()}", 0)

    def case_result_parse(self, received_data):
        if self.main_window.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # Parse receive frame
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        if success is False:
            self.main_window.log(f"接收数据失败：{result}", 2)
            self.log.add_message(f"接收数据失败：{result}", timestamp = True)
            return
        
        if cmd == (CMD["Nack"]):
            self.main_window.log("RISC-V答应失败", 2)
            self.log.add_message("RISC-V答应失败", timestamp = True)
            return

        # hex_cmd = "{:04X}".format(cmd)

        # hex_cmd_spilt = f"{hex_cmd[:2]} {hex_cmd[2:]}"

        # print(f"received cmd: {hex_cmd}")    
        # print(f"received cmd_spilt: {hex_cmd_spilt}")
        
        # print(f"原始负载: {payload}")
        # self.main_window.log(f"原始负载_hex: {payload.hex()}", 1)

        processed_result = self.case_manager.get_processed_case()

        case_id = None
        case_message_false = ""

        for _ , case_payload in processed_result.items():
            if payload[:2]== case_payload:
                case_id = payload[1]
            # else:
            #     id_message_false = f"RISC-V返回的实例ID{payload[:2]}不匹配"
            #     self.log.add_message(id_message_false, timestamp = True)
            #     self.main_window.log(id_message_false, 2)
            #     return

        if len(payload) < 2:
            print(f"payload: {payload.hex()}")
            length_false = "RISC-V返回的数据负载数据长度不足"
            self.log.add_message(length_false, timestamp = True)
            self.main_window.log(length_false, 2)
            return
        
        if payload[2:4] != b'\x00\x00':
            error_massage = payload[4:]
            split_data = []
            # Spilt count
            num = len(error_massage) // 6

            case_message_false = f"实例{case_id:02X}运行结果出现错误"
            self.main_window.log(f"实例{case_id:02X}运行结果出现错误", 2)

            self.log.add_message(case_message_false, timestamp = True)

            for i in range(num):
                start_index = i * 6
                end_index = start_index + 6
                # Spilt error message
                chunk = error_massage[start_index:end_index]
                split_data.append(chunk)

            # Traverse the array
            for data in split_data:
                # Split the data
                write_address = data[0]    # One byte: Write address
                write_data = data[1:3]       # Two bytes: Write data
                read_address = data[3]       # One byte: Read address
                read_data = data[4:6]      # Two bytes: Read data

                # print(f"write_address: {write_address}, write_data: {write_data}, read_address: {read_address}, read_data: {read_data}")

                write_address = hex(write_address)[2:].upper()  # 去掉 '0x' 前缀并转为大写
                write_data = ''.join(f'{byte:02X}' for byte in write_data)

                # 将写数据和读数据位数格式化为2位16进制数
                read_address = hex(read_address)[2:].upper()  # 转换为16进制并补零
                read_data = ''.join(f'{byte:02X}' for byte in read_data)
                
                message = f"写数据地址: {write_address}, 写数据: {write_data}, 读数据地址: {read_address}, 读数据: {read_data}"
                
                # print(message)
                
                self.log.add_message(message)
        else:

            case_message_True = f"实例{case_id:02X}运行结果正确"
            self.main_window.log(f"实例{case_id:02X}运行结果正确", 1)
            self.log.add_message(case_message_True, timestamp = True)
