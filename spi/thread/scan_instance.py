
from PySide6.QtCore import QThread, Signal, QElapsedTimer
from controller.crc import CRC
from controller.frame import Frame,CMD

class ScanInstanceThread(QThread):
    log_signal = Signal(str,int)

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
        timer = QElapsedTimer()
        timer.start()

        target_ms = int(seconds * 1000)

        while self.running and timer.elapsed() < target_ms:
            remaining = target_ms - timer.elapsed()

            if remaining > 10:
                self.msleep(10)
            elif remaining > 1:
                self.msleep(1)

    def stop(self):
        self.running = False

    def run(self):
        global case_list

        if not self.parent.spi_device:
            self.log_signal.emit("SPI设备未连接", 2)
            return
        
        send_data = Frame.generate_frame(CMD["GetCaseList"])

        if self.current_crc_mode == 0:
            crc_value = CRC.crc_16_user(send_data)
            send_data += crc_value.to_bytes(2, byteorder='big')

        self.spi_device.spi_send(
            send_data,
            self.spi_clk_mode,
            self.spi_bit_order
        )
        self.log_signal.emit(f"send_data: {send_data.hex()}", 0)

        self.precise_delay(self.delay)

        received_data = self.spi_device.spi_receive(
            self.spi_clk_mode,
            self.spi_bit_order,
            64
        )
        
        self.log_signal.emit(f"测试接收64字节数据：received_data: {received_data.hex()}", 0)

        if self.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        success, _, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        if success is False:
            self.log_signal.emit(f"获取实例失败：{result}", 2)
            return
        
        if cmd != CMD["CaseList"]:
            self.log_signal.emit("命令字错误", 2)
            return
        
        self.log_signal.emit(f"原始负载: {payload.hex()}", 1)
        print(payload)

        case_list = Frame.parse_case(payload)

        print(case_list)

        case_list_str = ';'.join(case_list)
        self.log_signal.emit(f"负载提取: {case_list_str}", 1)