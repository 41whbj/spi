from PySide6.QtCore import QThread, Signal, QElapsedTimer, QTimer, Qt
# from .case_manager import CaseItemWidget
# from PySide6.QtCore import QElapsedTimer
from .frame import Frame, CMD

class CycleSendThread(QThread):
    """
        循环发送线程，负责从MCU_list_test中获取item并发送
    """
    log_signal = Signal(str, int)
    finished_signal = Signal()
    receive_data_signal = Signal(bytes)  # 新增信号用于传递接收的数据
    
    def __init__(self, parent, delay=1.0):
        super().__init__()
        self.parent = parent
        self.delay = delay
        self.running = False
        self.receive_data_signal.connect(self.receive_frame_data, Qt.QueuedConnection)
        
    def run(self):
        self.running = True
        
        # 从MCU_list_test中获取所有item
        test_list = self.parent.ui.MCU_list_test
        item_count = test_list.count()
        
        if item_count == 0:
            self.log_signal.emit("MCU测试列表为空，无法进行循环发送", 2)
            self.finished_signal.emit()
            return
        
        try:
            while self.running:
                for i in range(item_count):
                    if not self.running:
                        break
                    
                    # 获取列表项
                    list_item = test_list.item(i)
                    if not list_item:
                        continue
                    
                    # 获取item对应的widget（这是一个CaseItemWidget）
                    widget = test_list.itemWidget(list_item)
                    if not widget:
                        continue
                    
                    # 获取延时值（如果widget有delay_input）
                    delay = self.delay  # 默认使用传入的delay值
                    if hasattr(widget, 'delay_input'):
                        delay_text = widget.delay_input.text()
                        try:
                            delay = float(delay_text) if delay_text else self.delay
                            if delay < 0:
                                delay = self.delay
                        except ValueError:
                            delay = self.delay
                            self.log_signal.emit(f"第{i+1}项的延时设置无效，使用默认值{self.delay}秒", 1)
                    
                    # 直接调用widget的send_clicked方法，并连接其send_frame信号到发送函数
                    # 临时连接信号以发送数据
                    widget.send_frame.connect(self.send_frame_data)
                    try:
                        widget.send_clicked()
                        # self.log_signal.emit(f"已发送第{i+1}项: {widget.name}", 0)
                    except Exception as e:
                        self.log_signal.emit(f"发送第{i+1}项时出错: {str(e)}", 2)
                    finally:
                        # 断开临时连接
                        widget.send_frame.disconnect(self.send_frame_data)
                    
                    # 等待指定的延时
                    self.precise_delay(delay)
        except Exception as e:
            self.log_signal.emit(f"循环发送过程中发生错误: {str(e)}", 2)
        finally:
            self.running = False
            self.finished_signal.emit()
    
    def send_frame_data(self, frame, correct):
        """
        处理来自CaseItemWidget的send_frame信号
        这个方法模仿PC_MCU2Window中的send_frame方法
        """
        if not hasattr(self.parent, 'main_window') or not self.parent.main_window:
            self.log_signal.emit("主窗口未初始化", 2)
            return
            
        if not hasattr(self.parent.main_window, 'spi_device') or not self.parent.main_window.spi_device:
            self.log_signal.emit("SPI设备未连接", 2)
            return
        
        if correct is False:
            self.log_signal.emit("请输入正确的数据", 2)
            return
        
        try:
            result = self.parent.main_window.spi_device.spi_send(
                frame,
                self.parent.main_window.spi_clk_mode,
                self.parent.main_window.spi_bit_order
            )

            if result is not True:
                self.log_signal.emit("数据发送失败", 2)
                return

            data = ' '.join([f"{byte:02X}" for byte in frame])
            print(f"发送成功，数据: {data}")

            delay_input = self.parent.main_window.ui.line_test_interval.text()
            delay_value = float(delay_input) if delay_input else 3.0

            if delay_value <= 0:
                delay_input = 3.0
                print("使用默认值3秒", 1)
            else:
                delay_input = delay_value

            # 使用单次定时器，在延迟后触发接收数据信号
            QTimer.singleShot(int(delay_value * 1000), lambda: self.trigger_receive_data())

        except Exception as e:
            self.log_signal.emit(f"发送数据时出错: {str(e)}", 2)
    
    def trigger_receive_data(self):
        """触发接收数据的处理"""
        if not hasattr(self.parent.main_window, 'spi_device') or not self.parent.main_window.spi_device:
            self.log_signal.emit("SPI设备未连接", 2)
            return

        try:
            received_data = self.parent.main_window.spi_device.spi_receive(
                self.parent.main_window.spi_clk_mode,
                self.parent.main_window.spi_bit_order,
                32
            )
            # 通过信号将数据传递回主线程处理
            self.receive_data_signal.emit(received_data)
        except Exception as e:
            self.log_signal.emit(f"接收数据时出错: {str(e)}", 2)
    
    def receive_frame_data(self, received_data):
        """在主线程中处理接收的数据"""
        try:
            # self.main_window.log(f"测试接收32字节数据：received_data: {received_data.hex()}", 0)

            if self.parent.main_window.current_crc_mode == 0:
                use_crc = True
            else:
                use_crc = False

            # Parse receive frame
            success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

            if success is False:
                self.parent.main_window.log(f"接收数据失败：{result}", 2)
                return
            
            if cmd == (CMD["Nack"]):
                self.parent.main_window.log("接收到Nack命令字,发生错误", 2)

            hex_cmd = "{:04X}".format(cmd)

            hex_cmd_spilt = f"{hex_cmd[:2]} {hex_cmd[2:]}"

            # print(f"received cmd: {hex_cmd}")    
            print(f"received cmd_spilt: {hex_cmd_spilt}")
            
            # print(f"原始负载: {payload}")
            # self.main_window.log(f"原始负载_hex: {payload.hex()}", 1)

            # 使用parent的case_manager而不是self.case_manager
            processed_result = self.parent.case_manager.get_processed_case()


            if len(payload) < 2:
                self.parent.main_window.log("负载数据长度不足", 2)
                return
            
            self.found_case_name = None
            for case_name, case_payload in processed_result.items():
                # print(f"case_name: {case_name}, case_payload: {case_payload}")
                # print(f"payload[:2]: {payload[:2]}")
                if payload[:2]== case_payload:
                    print(f"匹配到测例: {case_name}")
                    self.found_case_name = case_name
                    break
            # print(f"self.found_case_name: {self.found_case_name}")

            print(f"运行结果返回: {payload[-1]}")

            # if payload[-1:] == b'\x00':
            #     self.parent.main_window.log(f"{self.found_case_name}的运行结果是：通过")
            if payload[-1:] == b'\x01':
                self.parent.main_window.log(f"{self.found_case_name}的运行结果是：失败")
        except Exception as e:
            self.parent.main_window.log(f"处理接收数据时出错: {str(e)}", 2)
    
    def stop(self):
        """
            停止线程运行
        """
        self.running = False
        
    def precise_delay(self, seconds):
        """
            高精度延时函数
        """

        timer = QElapsedTimer()
        timer.start()
        
        target_ms = int(seconds * 1000)
        
        while self.running and timer.elapsed() < target_ms:
            remaining = target_ms - timer.elapsed()
            if remaining > 10:
                self.msleep(10)
            elif remaining > 1:
                self.msleep(1)