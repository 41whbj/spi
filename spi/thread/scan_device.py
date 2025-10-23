
from PySide6.QtCore import QThread, Signal, QElapsedTimer
# from controller.crc import CRC
from controller.frame import Frame, CMD

class ScanDeviceThread(QThread):
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
        if not self.parent.spi_device:
            self.log_signal.emit("SPI设备未连接", 2)
            return
        
        if self.current_crc_mode == 0:
            send_data = Frame.generate_frame(CMD["Ping"], use_crc=True)
        else:
            send_data = Frame.generate_frame(CMD["Ping"])

        self.spi_device.spi_send(
            send_data,
            self.spi_clk_mode,
            self.spi_bit_order
        )

        self.log_signal.emit(f"send_data: {send_data.hex()}", 0)

        self.precise_delay(self.delay)

        if self.current_crc_mode == 0:
            received_data = self.spi_device.spi_receive(
                self.spi_clk_mode,
                self.spi_bit_order,
                12
            )
            self.log_signal.emit(f"received_data: {received_data.hex()}", 0)
            use_crc = True
        else:
            received_data = self.spi_device.spi_receive(
                self.spi_clk_mode,
                self.spi_bit_order,
                10
            )
            self.log_signal.emit(f"received_data: {received_data.hex()}", 0)
            use_crc = False

        success, _, cmd, _, result = Frame.parse_receive_frame(received_data, use_crc)
        
        if success is True:
            if cmd == CMD["Ack"]:
                self.log_signal.emit("连接成功", 1)
            else:
                self.log_signal.emit("命令字错误", 2)
        else:
            self.log_signal.emit(f"连接失败：{result}", 2)