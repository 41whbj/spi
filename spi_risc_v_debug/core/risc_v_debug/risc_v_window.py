#!/usr/bin/env python3.13
"""
filename: risc_v_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-01
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
# from .log.log_ import CsvManager

class RiscVWindow(QObject):
    """
    PC-RISC-V连接主窗口类，负责处理与PC-RISC-V相关的UI连接和业务逻辑.
    """

    def __init__(self, application, spi_controller,):
        """初始化PC-RISC-V连接窗口.

        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.case_manager = CaseID_Manager()
        self.spi_controller = spi_controller

        # 设置信号连接
        self.setup_connections()
        self.log_manager = []

        # 设置拖拽功能
        self.setup_drop()
        # self.log = CsvManager()

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 循环发送状态标志
        self.is_cycle_sending = False

    def start_cycle_send(self):
        """
        启动循环发送功能，用于自动发送测试用例
        """

        # 检查是否已经在发送
        if self.is_cycle_sending:
            self.application.log_window.log("循环发送正在进行中，请先停止当前发送任务", 0)
            return
        
        # 检查MCU_list_case是否为空
        if self.ui.MCU_list_case.count() == 0:
            self.application.log_window.log("没有可发送的测试用例，请先扫描", 2)
            return
        
        # 获取延迟值
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_value = 1.0
            self.application.log_window.log("使用默认值1秒作为发送间隔", 1)

        # 创建并启动循环发送线程
        self.cycle_send_thread = CycleSendThread(
            application=self.application,
            delay=delay_value,
        )
        
        self.cycle_send_thread.log_signal.connect(self.application.log_window.log)
        self.cycle_send_thread.finished.connect(self.on_cycle_send_finished)
        self.cycle_send_thread.receive_data_signal.connect(self.case_result_parse)
        
        self.is_cycle_sending = True
        
        # 更新UI控件状态
        self.ui.MCU_button_send.setEnabled(False)
        self.ui.MCU_button_stop.setEnabled(True)
        
        self.application.log_window.log("开始循环发送测试用例...", 0)
        self.cycle_send_thread.start()
    
    def stop_cycle_send(self):
        """
        停止循环发送功能
        """
        if self.cycle_send_thread and self.cycle_send_thread.isRunning():
            self.application.log_window.log("正在停止循环发送任务...", 0)
            self.cycle_send_thread.stop()
    
    def on_cycle_send_finished(self):
        """
        循环发送线程结束后的处理
        """
        self.is_cycle_sending = False
        # 更新控件状态
        self.ui.MCU_button_send.setEnabled(True)
        self.ui.MCU_button_stop.setEnabled(False)
        self.application.log_window.log("循环发送任务已完成或终止", 0)
    
    def setup_connections(self):
        """
        设置PC_MCU相关控件的连接.
        """

        # 连接"连接"按钮的信号
        self.ui.button_mcu_connect.clicked.connect(self.scan_device)

        # 连接"扫描"按钮的信号
        self.ui.button_mcu_scan.clicked.connect(self.scan_case)
        self.ui.MCU_button_send.clicked.connect(self.start_cycle_send)
        self.ui.MCU_button_stop.clicked.connect(self.stop_cycle_send)
        self.ui.MCU_button_test.clicked.connect(self.test_send)

    def test_send (self):
        """
        发送输入框内的数据
        """

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 获取输入框内的数据
        data = self.ui.MCU_line_test.text()

        # 发送数据
        self.application.spi_controller.spi_send(data, self.clk_mode ,self.bit_order)


    def setup_drop(self):
        """
        设置MCU_list_case的拖拽功能.
        """
        
        self.ui.MCU_list_case.setDragEnabled(True)
        self.ui.MCU_list_case.setAcceptDrops(False)
        self.ui.MCU_list_case.setDropIndicatorShown(True)

        # 设置MCU_list_test支持接收拖拽项目
        self.ui.MCU_list_test.setAcceptDrops(True)
        self.ui.MCU_list_test.setDropIndicatorShown(True)

        # 设置拖拽事件处理器
        self.ui.MCU_list_test.dragEnterEvent = self.test_list_drag_enter_event
        self.ui.MCU_list_test.dragMoveEvent = self.test_list_drag_move_event
        self.ui.MCU_list_test.dropEvent = self.test_list_drop_event

    
    def test_list_drag_enter_event(self, event: QDragEnterEvent):
        """处理拖拽进入事件，验证拖拽数据格式.

        Args:
            event: QDragEnterEvent 拖拽进入事件对象
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
        """
        扫描设备功能.
        """

        # 检查扫描设备线程是否正在运行
        if hasattr(self, 'scan_device_thread') and self.scan_device_thread.isRunning():
            self.application.log_window.log("连接正在进行中，请稍候...", 0)
            return

        # 测试输入框的输入，控制扫描设备的时间间隔
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0
        
        if delay_value <= 0:
            delay_input = 1.0
            self.application.log_window.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        # 启动扫描设备线程
        self.scan_device_thread = ScanDeviceThread(
            application=self.application, 
            delay=delay_input
        )

        # 信号连接
        self.scan_device_thread.log_signal.connect(self.application.log_window.log)
        self.scan_device_thread.start()
    
    def scan_case(self):
        """
        扫描测例功能.
        """
     
        # 检查扫描测例线程是否正在运行
        if hasattr(self, 'scan_case_thread') and self.scan_case_thread.isRunning():
            self.application.log_window.log("扫描正在进行中，请稍候...", 0)
            return

        # 测试输入框的输入，控制扫描测例的时间间隔
        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0

        if delay_value <= 0:
            delay_input = 1.0
            self.application.log_window.log("使用默认值1秒", 1)
        else:
            delay_input = delay_value

        # 启动扫描测例线程
        self.scan_case_thread = ScanInstanceThread(
            application=self.application, 
            delay=delay_input
        )

        # 信号连接
        self.scan_case_thread.case_signal.connect(self.handle_scan_case_result)
        self.scan_case_thread.log_signal.connect(self.application.log_window.log)
        self.scan_case_thread.start()
    
    def handle_scan_case_result(self, case_list):
        """处理扫描测例结果，将测例添加到MCU_list_case.

        Args:
            case_list: 测例列表
        """

        self.case_manager.clear_processed_case()

        if not case_list:
            self.application.log_window.log("未扫描到任何负载", 1)
            return

        # 清空现有列表
        self.ui.MCU_list_case.clear()
        
        # 为测例分配ID
        self.case_manager.assign_id(case_list)
        processed_case = self.case_manager.get_processed_case()

        # 检查处理后的用例是否为空
        if processed_case is None:
            self.application.log_window.log("没有处理任何case", 1)
            return
        
        # 为每个测例创建控件
        for name, id_bytes in processed_case.items():
            case_item = CaseItemWidget(name, id_bytes)

            case_item.send_frame.connect(self.send_frame)

            list_item = QListWidgetItem()
            self.ui.MCU_list_case.addItem(list_item)
            self.ui.MCU_list_case.setItemWidget(list_item, case_item)
            
            list_item.setSizeHint(case_item.sizeHint())
            
        self.application.log_window.log(f"获取 {len(processed_case)} 个测例", 1)

    def send_frame(self, frame, correct):
        """通过SPI向MCU发送帧.

        Args:
            frame: 要发送的帧数据
            correct: 数据是否正确
        """

        if correct is False:
            QMessageBox.warning(self.application, "警告", "数据错误，请检查输入")
            return

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # print(f"发送的数据：{frame.hex()}")
        self.spi_controller.spi_send(frame.hex(),self.clk_mode,self.bit_order)

        # print(f"发送的数据：{frame.hex()}")

        delay_input = self.ui.line_test_interval.text()
        delay_value = float(delay_input) if delay_input else 1.0

        if delay_value <= 0:
            delay_input = 1.0
            # print("使用默认值1秒")
        else:
            delay_input = delay_value

        QTimer.singleShot(int(delay_value * 1000), self.receive_ack_response)

    def receive_ack_response(self):
        """接收Ack响应."""

        # 创建一个内部方法来处理重试逻辑

        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(self.clk_mode, self.bit_order, 128, log=False)

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        self.application.log_window.log(f"接收到命令字:{hex(int(cmd))}")
        self.application.log_window.log(f"接收到数据:{bytes(payload).hex()}")
        
        # 检查命令字是否为Ack
        if cmd == CMD["Ack"]:
            # 检查Ack是否有负载
            if len(payload) > 0:
                self.application.log_window.log(f"Ack命令有负载数据：{bytes(payload).hex()}", 2)
                return
            else:
                self.application.log_window.log("收到正确的Ack响应，无负载", 1)
                # Ack确认成功，开始流程二：获取CaseResult
                self.get_case_result_retry_count = 0
                QTimer.singleShot(5000, self.send_get_case_result)
        else:
            self.application.log_window.log(f"收到非Ack命令：{hex(int(cmd))}", 2)
            return
    
    def send_get_case_result(self):
        """发送GetCaseResult指令."""
        generate_frame = Frame.generate_frame(CMD["GetCaseResult"])
        self.spi_controller.spi_send(generate_frame.hex(), self.clk_mode, self.bit_order)
        
        # 立即准备接收响应
        QTimer.singleShot(5000, self.receive_case_result)

    def receive_case_result(self):
        """接收CaseResult响应."""
        
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(self.clk_mode, self.bit_order, 128, log=False)

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查帧解析是否成功
        if not success:
            self.application.log_window.log(f"接收CaseResult失败：{result}", 2)
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 10:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                return
            # 重新尝试获取CaseResult
            QTimer.singleShot(5000, self.send_get_case_result)
            return

        # 检查命令字类型
        if cmd == CMD["CaseResult"]:
            self.application.log_window.log("收到CaseResult响应", 1)
            self.case_result_parse(received_data)
            self.get_case_result_retry_count = 0
        elif cmd == CMD["CaseRunning"]:
            self.application.log_window.log(f"测例仍在运行中，负载: {bytes(payload).hex()}", 1)
            # 测例仍在运行，重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 10:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                return
            QTimer.singleShot(5000, self.send_get_case_result)
        elif cmd == CMD["Nack"]:
            self.application.log_window.log(f"收到Nack响应，负载: {bytes(payload).hex()}", 2)
            # Nack响应，重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 10:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                return
            QTimer.singleShot(5000, self.send_get_case_result)
        else:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 10:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                return
            QTimer.singleShot(5000, self.send_get_case_result)

    def case_result_parse(self, received_data):
        """解析测例结果.

        Args:
            received_data: 接收到的数据
        """

        # 检查是否使用CRC校验
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # 解析接收到的帧数据
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查解析结果是否成功
        if success is False:
            self.application.log_window.log(f"接收数据失败：{result}", 2)
            # self.log.add_message(f"接收数据失败：{result}", timestamp = True)
            return
        
        # 检查命令是否为否定应答(Nack)
        if cmd == (CMD["Nack"]):
            self.application.log_window.log("RISC-V答应失败", 2)
            self.application.log_window.log(f"负载: {bytes(payload[:2])}")
            # self.log.add_message("RISC-V答应失败", timestamp = True)
            return

        # 获取已处理的用例信息
        processed_result = self.case_manager.get_processed_case()

        # case_id = None
        # case_name = None
        # 初始化变量
        case_message_false = ""

        # print(f"payload[:2]: {payload[:2]}")

        # 查找对应的测例
        for case_name, case_payload in processed_result.items():
            if bytes(payload[:2]) == case_payload:
                case_name = case_name
                break

        # print(f"processed_result: {processed_result}")

        # if len(payload) < 2:
        #     # print(f"payload: {payload.hex()}")
        #     length_false = "RISC-V返回的数据负载数据长度不足"
        #     # self.log.add_message(length_false, timestamp = True)
        #     self.application.log_window.log(length_false, 2)
        #     return
        
        self.application.log_window.log(f"负载返回：{bytes(payload)}", 1)
        
        # 检查执行结果（payload[2:4]为结果码
        if bytes(payload[2:4]) != b'\x00\x00':

            # 提取错误信息
            error_massage = payload[4:]
            split_data = []

            # 分割计数
            num = len(error_massage) // 11

            # print(f"num: {num}")

            # print(f"case_name: {case_name}")
            case_message_false = f"测例{case_name}运行结果出现错误"
            self.application.log_window.log(f"测例{case_name}运行结果出现错误", 2)

            # self.application.log_window.special_log.add_message(case_message_false, timestamp = True)

            for i in range(num):
                start_index = i * 11
                end_index = start_index + 11

                # 分割错误消息
                chunk = error_massage[start_index:end_index]
                split_data.append(chunk)

            # 遍历数组
            for data in split_data:
                # 分割数据
                error_round = data[0:2]      # 两个字节：错误次数
                hw_count = data[2]           # 一个字节：写入半字次数
                write_base_address = data[3] # 一个字节：写基地址
                write_address = data[4]      # 一个字节：写地址
                write_data = data[5:7]       # 两个字节：写数据
                read_base_address = data[7]  # 一个字节：读基地址
                read_address = data[8]       # 一个字节：读地址
                read_data = data[9:11]       # 两个字节：读数据
                test_type = data[11]         # 一个字节：测试类型


                # print(f"test_type: {test_type}")

                if test_type == 0:
                    packet_type = "写包测试"
                elif test_type == 1:
                    packet_type = "读包测试"
                elif test_type == 2:
                    packet_type = "恢复测试"
                else:
                    packet_type = ""
                
                # 转换错误编号为整数
                error_round = int.from_bytes(error_round, byteorder='big')
                # print(f"error_round: {error_round}")

                hw_count = int.from_bytes(hw_count, byteorder='big')

                # 格式化地址和数据为十六进制字符串
                write_base_address = hex(write_base_address)[2:].upper()  # 去掉 '0x' 前缀并转为大写
                write_address = hex(write_address)[2:].upper()  # 去掉 '0x' 前缀并转为大写
                write_data = ''.join(f'{byte:02X}' for byte in write_data)

                # 将写数据和读数据位数格式化为2位16进制数
                read_base_address = hex(read_base_address)[2:].upper()  # 去掉 '0x' 前缀并转为大写
                read_address = hex(read_address)[2:].upper()  # 转换为16进制并补零
                read_data = ''.join(f'{byte:02X}' for byte in read_data)

                self.application.log_window.special_log.add_error_message(
                    error_round=error_round,
                    hw_count=hw_count,
                    write_base_address=write_base_address,
                    write_address=write_address,
                    write_data=write_data,
                    read_address=read_address,
                    read_base_address=read_base_address,
                    read_data=read_data,
                    packet_type=packet_type
                )

        else:
            self.application.log_window.log(f"测例{case_name}运行结果正确", 1)
            # self.application.log_window.special_log.add_message(case_message_True, timestamp = True)
