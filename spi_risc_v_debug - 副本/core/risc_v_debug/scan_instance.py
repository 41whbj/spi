from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from PySide6.QtCore import QTimer
# from controller.crc import CRC
from .case_manager import CaseItemWidget, CaseID_Manager

from .frame import Frame, CMD


class ScanInstance:
    """实例扫描类，用于执行测例扫描操作"""
    
    def __init__(self, application, spi_controller):
        """初始化实例扫描

        Args:
            application: 应用程序对象
            delay: 扫描延迟时间（秒），默认为1秒
        """
        self.application = application
        self.ui = self.application.ui

        self.spi_controller = spi_controller

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        self.case_manager = CaseID_Manager()

    def scan(self):
        """执行测例扫描操作"""

        self.application.log_window.log("开始扫描测例", 1)

        send_data = Frame.generate_frame(CMD["GetCaseList"])

        # print(f"发送的数据：{send_data}，类型：{type(send_data)}")  # 打印发送数据（调试用）
        
        # 发送数据
        self.application.spi_controller.spi_send(
            send_data.hex(),
            self.clk_mode,              # SPI时钟模式
            self.bit_order,
            log = False 
        )

        # print(f"send_data: {send_data.hex()}")  # 打印发送数据（调试用）
        
        # 使用QTimer进行非阻塞延时
        QTimer.singleShot(int(1000), self.receive)

    def receive(self):
        """执行实际的扫描操作"""
        
        # 提供一个128字节的接收区域来接收数据
        received_data = self.application.spi_controller.spi_receive(
            self.clk_mode,
            self.bit_order,
            512,                        # 接收缓冲区大小为128字节
            log = False
        )
        
        # print(f"测试接收128字节数据：received_data: {received_data.hex()}")  # 打印接收数据（调试用）

        # 根据CRC模式设置解析标志
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # 恢复按钮
        self.ui.button_mcu_connect.setEnabled(True)
        self.ui.button_mcu_scan.setEnabled(True)

        # 解析接收到的帧数据
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查解析是否成功
        if success is False:
            self.application.log_window.log(f"获取测例失败：{result}", 2)
            return None
        
        # 检查命令是否为否定应答(Nack)
        if cmd == CMD["Nack"]:
            self.application.log_window.log("RISC-V答应失败", 2)
            return None
        
        # print(f"payload: {payload}")  # 打印负载数据（调试用）

        # 解析测例数据
        case = Frame.parse_case(payload)

        # print(f"case: {case}")  # 打印测例数据（调试用）

        self.handle_scan_case_result(case)

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

        QTimer.singleShot(int(1000), self.receive_ack_response)

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
                QTimer.singleShot(8000, self.send_get_case_result)
        else:
            self.application.log_window.log(f"收到非Ack命令：{hex(int(cmd))}", 2)
            return
    
    def send_get_case_result(self):
        """发送GetCaseResult指令."""
        generate_frame = Frame.generate_frame(CMD["GetCaseResult"])
        self.spi_controller.spi_send(generate_frame.hex(), self.clk_mode, self.bit_order)
        
        # 立即准备接收响应
        QTimer.singleShot(1000, self.receive_case_result)

    def receive_case_result(self):
        """接收CaseResult响应."""
        
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(self.clk_mode, self.bit_order, 1024, log=False)

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查帧解析是否成功
        if not success:
            self.application.log_window.log(f"接收CaseResult失败：{result}", 2)
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 3:
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
            num = len(error_massage) // 12

            # print(f"num: {num}")

            # print(f"case_name: {case_name}")
            case_message_false = f"测例{case_name}运行结果出现错误"
            self.application.log_window.log(f"测例{case_name}运行结果出现错误", 2)
            self.application.log_window.special_log.add_message(case_message_false, timestamp = True)

            # self.application.log_window.special_log.add_message(case_message_false, timestamp = True)

            for i in range(num):
                start_index = i * 12
                end_index = start_index + 12

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

                hw_count = int(hw_count)  # 转换为整数

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
            case_message_True = f"测例{case_name}运行结果正确"
            self.application.log_window.log(f"测例{case_name}运行结果正确", 1)
            self.application.log_window.special_log.add_message(case_message_True, timestamp = True)


        