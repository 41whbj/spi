from PySide6.QtCore import QThread, Signal, QElapsedTimer, QTimer, Qt
from .frame import Frame, CMD
from PySide6.QtWidgets import QMessageBox
import random
from .case_manager import CaseID_Manager
from datetime import datetime


class SendThread(QThread):
    """
        循环发送线程，负责从MCU_list_test中获取item并发送
    """
    log_signal = Signal(str, int)
    finished_signal = Signal()
    receive_data_signal = Signal(bytes)
    
    def __init__(self, application, case_result_parser, case_manager):
        super().__init__()
        self.application = application
        self.ui = self.application.ui
        self.case_result_parser = case_result_parser
        self.running = False
        
        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        self.case_manager = case_manager

        # 初始化变量
        self.current_item_index = 0
        self.item_count = 0
        self.round_count = 0
        self.current_round = 0
        self.mode = "循环发送"  # 默认模式
        self.current_case_name = ""
        self.get_case_result_retry_count = 0
        self.get_log_retry_count = 0
        self.log_content = []

    def run(self):
            self.running = True

            # 获取模式选择
            self.mode = self.ui.comboBox_mode_select.currentText()

            # 获取是否无限循环
            self.is_endless = self.ui.radioButton_endless.isChecked()

            # 获取循环次数
            if self.is_endless is False:
                try:
                    round_input_text = self.ui.lineEdit_round_input.text()
                    if round_input_text.strip() == "":
                        # 如果输入为空，默认为1次
                        self.round_count = 1
                        self.log_signal.emit("循环次数为空，使用默认值1", 1)
                    else:
                        self.round_count = int(round_input_text)
                        if self.round_count <= 0:
                            self.round_count = 1
                            self.log_signal.emit("循环次数必须大于0，使用默认值1", 1)
                except ValueError:
                    self.log_signal.emit("循环次数输入无效，使用默认值1", 1)
                    self.round_count = 1
            else:
                self.round_count = 0  # 无限循环用0表示
            
            # 从MCU_list_test中获取所有item
            test_list = self.ui.MCU_list_test
            self.item_count = test_list.count()
            
            if self.item_count == 0:
                self.log_signal.emit("MCU测试列表为空，无法进行测试", 2)
                self.finished_signal.emit()
                return
            
            # 初始化当前轮次
            self.current_round = 0
            
            # 开始执行第一个测例
            self.execute_next_case()

    def execute_next_case(self):
        """执行下一个测例"""
        # 检查是否仍在运行
        if not self.running:
            self.running = False
            self.finished_signal.emit()
            return
        
        # 检查是否达到循环次数限制（如果不是无限循环）
        if not self.is_endless and self.round_count > 0 and self.current_round >= self.round_count:
            self.log_signal.emit("已达到设定的循环次数", 1)
            self.running = False
            self.finished_signal.emit()
            return

        # 获取列表项
        test_list = self.ui.MCU_list_test

        if self.mode == "循环发送":
            # 循环发送模式
            if self.current_item_index >= self.item_count:
                # 一轮完成，开始下一轮
                self.current_item_index = 0
                self.current_round += 1
                if not self.is_endless and self.round_count > 0 and self.current_round >= self.round_count:
                    self.log_signal.emit("已达到设定的循环次数", 1)
                    self.running = False
                    self.finished_signal.emit()
                    return
            list_item = test_list.item(self.current_item_index)
        elif self.mode == "随机发送":
            # 随机发送模式
            if self.item_count > 0:
                random_index = random.randint(0, self.item_count - 1)
                list_item = test_list.item(random_index)
                # 在随机模式下，不增加current_item_index，因为是随机选择
            else:
                list_item = None

        if not list_item:
            # 如果没有找到列表项，继续下一个
            if self.running:  # 检查是否需要继续
                if self.mode == "循环发送":
                    self.current_item_index += 1
                QTimer.singleShot(1000, self.execute_next_case)  # 非阻塞延时1s后继续
            return

        # 获取item对应的widget（这是一个CaseItemWidget）
        widget = test_list.itemWidget(list_item)
        if not widget:
            if self.running:  # 检查是否需要继续
                if self.mode == "循环发送":
                    self.current_item_index += 1
                QTimer.singleShot(1000, self.execute_next_case)  # 非阻塞延时1s后继续
            return

        # 记录当前执行的测例名称
        self.current_case_name = widget.name

        # 临时连接信号以发送数据
        widget.send_frame.connect(self.send_frame_data)
        try:
            # 开始执行测例
            self.log_signal.emit(f"开始执行测例: {widget.name}", 1)
            widget.send_clicked()
        except Exception as e:
            self.log_signal.emit(f"执行测例 {widget.name} 时出错: {str(e)}", 2)
        finally:
            # 断开临时连接
            try:
                widget.send_frame.disconnect(self.send_frame_data)
            except TypeError:
                pass  # 如果没有连接，则忽略错误

    def send_frame_data(self, frame, correct):

        if correct is False:
            self.log_signal.emit("请输入正确的数据", 2)
            return
        
        try:
            self.application.spi_controller.spi_send(
                frame.hex(),
                self.clk_mode,
                self.bit_order,
                log = False
            )

            # 启动测例执行流程 - 按照risc_v_case.py的流程
            QTimer.singleShot(1000, self.receive_ack_response)

        except Exception as e:
            self.log_signal.emit(f"发送数据时出错: {str(e)}", 2)
    
    def receive_ack_response(self):
        """接收Ack响应."""
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.application.spi_controller.spi_receive(
            self.clk_mode, 
            self.bit_order, 
            128, 
            log=False
        )

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)
        
        # 检查命令字是否为Ack
        if cmd == CMD["Ack"]:
            # 检查Ack是否有负载
            if len(payload) > 0:
                self.log_signal.emit(f"Ack命令有负载数据：{bytes(payload).hex()}", 2)
                return
            else:
                self.log_signal.emit("收到正确的Ack响应", 1)
                # Ack确认成功，开始流程二：获取CaseResult
                self.get_case_result_retry_count = 0
                QTimer.singleShot(5000, self.send_get_case_result)
        else:
            self.log_signal.emit(f"收到非Ack命令：{hex(int(cmd))}", 2)
            # 延时3秒后执行下一个测例
            QTimer.singleShot(3000, self.execute_next_case)
            return
    
    def send_get_case_result(self):
        """发送GetCaseResult指令."""

        generate_frame = Frame.generate_frame(CMD["GetCaseResult"])

        self.application.spi_controller.spi_send(generate_frame.hex(), self.clk_mode, self.bit_order)

        QTimer.singleShot(1000, self.receive_case_result)

    def receive_case_result(self):
        """接收CaseResult响应."""

        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.application.spi_controller.spi_receive(self.clk_mode, self.bit_order, 1024, log=False)

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
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return
            # 重新尝试获取CaseResult
            QTimer.singleShot(5000, self.send_get_case_result)
            return

        # 检查命令字类型
        if cmd == CMD["CaseResult"]:
            self.application.log_window.log("收到CaseResult响应", 1)
            self.result_parse(received_data)
            self.get_case_result_retry_count = 0
        elif cmd == CMD["CaseRunning"]:
            self.application.log_window.log("测例仍在运行中", 1)
            # 测例仍在运行，重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 10:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
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
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
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
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return
            QTimer.singleShot(5000, self.send_get_case_result)

    def result_parse(self, received_data):
        """解析测例结果."""

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
            # 延时3秒后执行下一个测例
            QTimer.singleShot(3000, self.execute_next_case)
            return
        
        # 检查命令是否为否定应答(Nack)
        if cmd == (CMD["Nack"]):
            self.application.log_window.log("RISC-V答应失败", 2)
            self.application.log_window.log(f"负载: {bytes(payload[:2])}")
            # 延时3秒后执行下一个测例
            QTimer.singleShot(3000, self.execute_next_case)
            return
        
        if cmd == (CMD["CaseResult"]):

            if len(payload) > 3:
                self.application.log_window.log(f"测例结果负载长度过长，负载: {bytes(payload).hex()}", 2)
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return
            
            if len(payload) < 3:
                self.application.log_window.log(f"测例结果负载长度过短，负载: {bytes(payload).hex()}", 2)
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return

            # 格式化结果负载
            payload = bytes(payload)
            case_id = payload[0:2]
            case_result = payload[2]

            # 获取已处理的测例信息
            processed_result = self.case_manager.get_processed_case()

            # 查找对应的测例, 并记录测例名称
            for case_name, case_payload in processed_result.items():
                if bytes(case_id) == case_payload:
                    self.current_case_name = case_name
                    break

            if case_result == 0:
                self.application.log_window.log(f"测例{self.current_case_name}运行成功", 1)
                # 测例成功，延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
            elif case_result == 1:
                self.application.log_window.log(f"测例{self.current_case_name}运行失败", 2)

                # 失败时请求日志
                self.ask_log()
            else:
                self.application.log_window.log(f"测例{self.current_case_name}执行结果未知，负载: {bytes(payload).hex()}", 2)
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
        else:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 延时3秒后执行下一个测例
            QTimer.singleShot(3000, self.execute_next_case)
            return

    def ask_log(self):
        """
        请求获取日志信息.
        """
        self.application.log_window.log("正在请求获取日志信息", 1)
        
        # 发送GetLog命令
        QTimer.singleShot(1000, self.log_request)

    def log_request(self):
        """
        发送GetLog命令，请求获取日志信息.
        """

        self.get_log_retry_count = 0

        generate_frame = Frame.generate_frame(CMD["GetLog"])
        self.application.spi_controller.spi_send(generate_frame.hex(), self.clk_mode, self.bit_order)

        # 准备接收Log响应
        QTimer.singleShot(1000, self.log_response)

    def log_response(self):
        """
        接收Log响应
        """

        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.application.spi_controller.spi_receive(self.clk_mode, self.bit_order, 512, log=False)

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查帧解析是否成功
        if not success:
            self.application.log_window.log(f"接收Log失败：{result}", 2)
            # 增加重试计数
            self.get_log_retry_count += 1
            if self.get_log_retry_count >= 3:
                self.application.log_window.log("无法接收到日志信息", 2)
                # 重置计数器
                self.get_log_retry_count = 0
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return
            # 重新尝试获取Log
            QTimer.singleShot(1000, self.log_request)
            return
        
        if cmd != CMD["LogSending"] and cmd != CMD["LogFinished"]:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 增加重试计数
            self.get_log_retry_count += 1
            if self.get_log_retry_count >= 3:
                self.application.log_window.log("无法接收到日志信息", 2)
                # 重置计数器
                self.get_log_retry_count = 0
                # 延时3秒后执行下一个测例
                QTimer.singleShot(3000, self.execute_next_case)
                return
            # 重新尝试获取Log
            QTimer.singleShot(1000, self.log_request)
            return

        if cmd == CMD["LogSending"]:
            
            # self.log.append(bytes(payload).decode("ascii"))
            # print(f"解码成功: {bytes(payload).decode('ascii')}")

            self.log_content.append(bytes(payload).decode("latin-1"))
            print(f"解码成功: {bytes(payload).decode('latin-1')}") 

            QTimer.singleShot(1000, self.log_request)
                
        elif cmd == CMD["LogFinished"]:

            self.log_content.append(bytes(payload).decode("latin-1"))
            print(f"解码成功: {bytes(payload).decode('latin-1')}") 

            self.application.log_window.log("日志传输完成", 1)

            # 合并所有日志内容
            log = '\n'.join(self.log_content)
            self.application.log_window.log(f"完整日志内容: {log}", 1)

            log = ''.join(self.log_content)

            # 格式化时间戳
            timestamp = datetime.now().strftime("%H:%M:%S")

            # 保存测试用例运行结果
            self.case_result_parser.save_result(timestamp, self.current_case_name, log)

            # 清空日志缓冲区，为下次使用做准备
            self.log_content.clear()
            
            # 延时3秒后执行下一个测例
            QTimer.singleShot(3000, self.execute_next_case)

    def next_case_after_delay(self):
        """在延时后执行下一个测例"""
        if self.mode == "循环发送":
            self.current_item_index += 1
        # 在随机模式下，不增加current_item_index，因为是随机选择
        self.execute_next_case()

    # def next_case_after_delay(self):
    #     """在延时后执行下一个测例"""
    #     self.current_item_index += 1
    #     self.execute_next_case()
    
    def stop(self):
        """
            停止线程运行
        """
        self.running = False