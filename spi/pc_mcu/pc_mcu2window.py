#!/usr/bin/env python3.13
"""
filename: pc_mcu2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-02
description: PC-MCU连接主窗口，处理PC-MCU相关的UI连接和逻辑
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
    """PC-MCU连接主窗口类，负责处理与PC-MCU相关的UI连接和业务逻辑."""

    def __init__(self, main_window):
        """初始化PC-MCU连接窗口.

        Args:
            main_window: MainWindow测例
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
        """启动循环发送功能"""
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
            self.main_window.log("没有可发送的测试用例，请先扫描", 2)
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
        """停止循环发送功能"""
        if self.cycle_send_thread and self.cycle_send_thread.isRunning():
            self.main_window.log("正在停止循环发送任务...", 0)
            self.cycle_send_thread.stop()
    
    def on_cycle_send_finished(self):
        """循环发送线程结束后的处理"""
        self.is_cycle_sending = False
        # 更新UI状态
        self.ui.MCU_button_send.setEnabled(True)
        self.ui.MCU_button_stop.setEnabled(False)
        self.main_window.log("循环发送任务已完成或终止", 0)
    
    def setup_connections(self):
        """设置PC_MCU相关控件的连接."""
        # 连接"连接"按钮的信号
        self.ui.button_mcu_connect.clicked.connect(self.scan_device)
        # 连接"扫描"按钮的信号
        self.ui.button_mcu_scan.clicked.connect(self.scan_case)
        self.ui.MCU_button_send.clicked.connect(self.start_cycle_send)
        self.ui.MCU_button_stop.clicked.connect(self.stop_cycle_send)

        # 连接扫描测例信号，调用test函数
        # self.ui.button_mcu_scan.clicked.connect(self.test)

    def test(self):
        """测试函数，模拟扫描到的测例."""
        case_list_test = ['Case1', 'Case2', 'Case3']
        self.handle_scan_case_result(case_list_test)

    def setup_drop(self):
        """设置MCU_list_case的拖拽功能."""
        self.ui.MCU_list_case.setDragEnabled(True)
        self.ui.MCU_list_case.setAcceptDrops(False)
        self.ui.MCU_list_case.setDropIndicatorShown(True)

        # 设置MCU_list_test支持接收拖拽项目
        self.ui.MCU_list_test.setAcceptDrops(True)
        self.ui.MCU_list_test.setDropIndicatorShown(True)
        self.ui.MCU_list_test.dragEnterEvent = self.test_list_drag_enter_event
        self.ui.MCU_list_test.dragMoveEvent = self.test_list_drag_move_event
        self.ui.MCU_list_test.dropEvent = self.test_list_drop_event

    
    def test_list_drag_enter_event(self, event: QDragEnterEvent):
        """处理拖拽进入事件.

        Args:
            event: 拖拽进入事件
        """
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drag_move_event(self, event: QDragEnterEvent):
        """处理拖拽移动事件.

        Args:
            event: 拖拽移动事件
        """
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drop_event(self, event: QDropEvent):
        """处理拖拽释放事件.

        Args:
            event: 拖拽释放事件
        """
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            # 获取被拖拽的项目
            source = event.source()
            if source != self.ui.MCU_list_case:
                event.ignore()
                return

            # 从MCU_list_case拖拽到MCU_list_test
            selected_items = source.selectedItems()
            for item in selected_items:
                # 复制项目到MCU_list_test
                self.copy_item_to_test_list(item)
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def copy_item_to_test_list(self, source_item):
        """复制项目到测试列表.

        Args:
            source_item: 源列表项
        """
        # 获取原始的CaseItemWidget
        source_widget = self.ui.MCU_list_case.itemWidget(source_item)
        
        # 创建新的CaseItemWidget测例
        test_item_widget = CaseItemWidget(
            name=source_widget.name,
            id=source_widget.id,
            use_crc=source_widget.use_crc,
            mode="Test"
        )
        
        # 连接删除信号
        test_item_widget.delete_requested.connect(self.remove_test_item)
        
        # 创建新的列表项
        list_item = QListWidgetItem()
        self.ui.MCU_list_test.addItem(list_item)
        self.ui.MCU_list_test.setItemWidget(list_item, test_item_widget)
        list_item.setSizeHint(test_item_widget.sizeHint())

    def remove_test_item(self, test_item_widget):
        """从测试列表中移除项目.

        Args:
            test_item_widget: 要移除的测试项控件
        """
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
        """扫描设备功能."""

        # 检查SPI设备是否连接
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return

        # 检查扫描设备线程是否正在运行
        if hasattr(self, 'scan_device_thread') and self.scan_device_thread.isRunning():
            self.main_window.log("连接正在进行中，请稍候...", 0)
            return

        # 测试输入框的输入，控制扫描设备的时间间隔
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_input = 1.0
            self.main_window.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        # 启动扫描设备线程
        self.scan_device_thread = ScanDeviceThread(
            parent=self.main_window, 
            delay=delay_input
        )

        # 信号连接
        self.scan_device_thread.log_signal.connect(self.main_window.log)
        self.scan_device_thread.start()
    
    def scan_case(self):
        """扫描测例功能."""

        # 检查SPI设备是否连接
        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return        

        # 检查扫描测例线程是否正在运行
        if hasattr(self, 'scan_case_thread') and self.scan_case_thread.isRunning():
            self.main_window.log("扫描正在进行中，请稍候...", 0)
            return

        # 测试输入框的输入，控制扫描测例的时间间隔
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0

        if delay_value <= 0:
            delay_input = 1.0
            self.main_window.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        # 启动扫描测例线程
        self.scan_case_thread = ScanInstanceThread(
            parent=self.main_window, 
            delay=delay_input
        )

        # 信号连接
        self.scan_case_thread.case_signal.connect(self.handle_scan_case_result)
        self.scan_case_thread.log_signal.connect(self.main_window.log)
        self.scan_case_thread.start()
    
    def handle_scan_case_result(self, case_list):
        """处理扫描测例结果，将测例添加到MCU_list_case.

        Args:
            case_list: 测例列表
        """

        self.case_manager.clear_processed_case()

        if not case_list:
            self.main_window.log("未扫描到任何负载", 1)
            return

        self.ui.MCU_list_case.clear()
        
        self.case_manager.assign_id(case_list)
        processed_case = self.case_manager.get_processed_case()

        
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
        """通过SPI向MCU发送帧.

        Args:
            frame: 要发送的帧数据
            correct: 数据是否正确
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
            # print("数据发送失败", 2)
            return

        data = ' '.join([f"{byte:02X}" for byte in frame])

        # print(f"发送成功，数据: {data}")

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 3.0

        if delay_value <= 0:
            delay_input = 3.0
            print("使用默认值3秒", 1)
        else:
            delay_input = delay_value

        QTimer.singleShot(int(delay_value * 1000), self.receive_data)

    def receive_data(self):
        """接收数据."""

        if not hasattr(self.main_window, 'spi_device') or not self.main_window.spi_device:
            self.main_window.log("SPI设备未连接", 2)
            return

        received_data = self.main_window.spi_device.spi_receive(
            self.main_window.spi_clk_mode,
            self.main_window.spi_bit_order,
            1024
        )

        self.case_result_parse(received_data)
        
    def case_result_parse(self, received_data):
        """解析测例结果.

        Args:
            received_data: 接收到的数据
        """
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

        processed_result = self.case_manager.get_processed_case()

        # case_id = None
        # case_name = None
        case_message_false = ""

        for case_name, case_payload in processed_result.items():
            if payload[:2]== case_payload:
                # case_id = payload[1]
                case_name = case_name
                break


        if len(payload) < 2:
            # print(f"payload: {payload.hex()}")
            length_false = "RISC-V返回的数据负载数据长度不足"
            self.log.add_message(length_false, timestamp = True)
            self.main_window.log(length_false, 2)
            return
        
        if payload[2:4] != b'\x00\x00':
            error_massage = payload[4:]
            split_data = []
            # 分割计数
            num = len(error_massage) // 9

            # print(f"num: {num}")

            case_message_false = f"测例{case_name}运行结果出现错误"
            self.main_window.log(f"测例{case_name}运行结果出现错误", 2)

            self.log.add_message(case_message_false, timestamp = True)

            for i in range(num):
                start_index = i * 9
                end_index = start_index + 9
                # Spilt error message
                chunk = error_massage[start_index:end_index]
                split_data.append(chunk)

            # 遍历数组
            for data in split_data:
                # 分割数据
                error_round = data[0:2]        # 两个字节：错误编号
                write_address = data[2]      # 一个字节：写地址
                write_data = data[3:5]       # 两个字节：写数据
                read_address = data[5]       # 一个字节：读地址
                read_data = data[6:8]        # 两个字节：读数据
                test_type = data[8]          # 一个字节：测试类型

                print(f"test_type: {test_type}")

                if test_type == 0:
                    packet_type = "写包测试"
                elif test_type == 1:
                    packet_type = "读包测试"
                elif test_type == 2:
                    packet_type = "恢复测试"
                else:
                    packet_type = ""
                
                error_round = int.from_bytes(error_round, byteorder='big')
                # print(f"error_round: {error_round}")

                write_address = hex(write_address)[2:].upper()  # 去掉 '0x' 前缀并转为大写
                write_data = ''.join(f'{byte:02X}' for byte in write_data)

                # 将写数据和读数据位数格式化为2位16进制数
                read_address = hex(read_address)[2:].upper()  # 转换为16进制并补零
                read_data = ''.join(f'{byte:02X}' for byte in read_data)

                self.log.add_error_table_message(
                    error_round=error_round,
                    write_address=write_address,
                    write_data=write_data,
                    read_address=read_address,
                    read_data=read_data,
                    packet_type=packet_type
                )

        else:
            case_message_True = f"测例{case_name}运行结果正确"
            self.main_window.log(f"测例{case_name}运行结果正确", 1)
            self.log.add_message(case_message_True, timestamp = True)
