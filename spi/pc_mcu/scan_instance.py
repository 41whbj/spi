
from PySide6.QtCore import QThread, Signal, QElapsedTimer
# from controller.crc import CRC
from .frame import Frame,CMD

class ScanInstanceThread(QThread):
    log_signal = Signal(str,int)
    case_signal = Signal(list)

    def __init__(self, parent=None, delay=1):
        super().__init__(parent)
        self.parent = parent
        self.spi_device = parent.spi_device
        self.current_crc_mode = parent.current_crc_mode
        self.spi_clk_mode = parent.spi_clk_mode
        self.spi_bit_order = parent.spi_bit_order
        self.delay = delay
        self.running = True

    # Precise delay
    def precise_delay(self, seconds):
        # Create timer
        timer = QElapsedTimer()
        timer.start()
        
        # Convert seconds to milliseconds
        target_ms = int(seconds * 1000)

        # timer.elapsed()：check how much time has passed
        while self.running and timer.elapsed() < target_ms:
            # Calculate remaining time, continue check if the goal delay has been achieved
            remaining = target_ms - timer.elapsed()

            if remaining > 10:
                self.msleep(10)
            elif remaining > 1:
                self.msleep(1)

    def run(self):
        global case_list

        if not self.parent.spi_device:
            self.log_signal.emit("SPI设备未连接", 2)
            return
        
        # generate_frame with crc check if selected or not
        if self.current_crc_mode == 0:
            send_data = Frame.generate_frame(CMD["GetCaseList"], use_crc=True)
        else:
            send_data = Frame.generate_frame(CMD["GetCaseList"])

        # Send data
        self.spi_device.spi_send(
            send_data,
            self.spi_clk_mode,
            self.spi_bit_order
        )

        self.log_signal.emit(f"send_data: {send_data.hex()}", 0)

        self.precise_delay(self.delay)

        # Provide a 128-byte receiving area
        received_data = self.spi_device.spi_receive(
            self.spi_clk_mode,
            self.spi_bit_order,
            128
        )
        
        self.log_signal.emit(f"测试接收128字节数据：received_data: {received_data.hex()}", 0)

        if self.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # Parse receive frame
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        if success is False:
            self.log_signal.emit(f"获取实例失败：{result}", 2)
            return
        
        if cmd != CMD["CaseList"]:
            self.log_signal.emit("命令字错误", 2)
            return
        
        self.log_signal.emit(f"原始负载: {payload.hex()}", 1)
        # print(payload)

        case = Frame.parse_case(payload)

        self.case_signal.emit(case)
        
        self.log_signal.emit(f"负载提取: {case}", 1)
