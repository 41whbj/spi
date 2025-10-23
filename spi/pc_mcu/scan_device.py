from PySide6.QtCore import QThread, Signal, QElapsedTimer
# from controller.crc import CRC
from .frame import Frame, CMD
# from .log import LogManager
# from .pc_mcu2window import PC_MCU2Window

class ScanDeviceThread(QThread):
    log_signal = Signal(str,int)

    def __init__(self, parent=None, delay=1):
        super().__init__(parent)
        self.parent = parent
        self.delay = delay
        self.running = True
        # self.LogManager = LogManager()

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

        # Check if SPI device is connected
        if hasattr(self.parent, 'spi_device') and self.parent.spi_device:
            if self.parent.spi_device.jtool is None or self.parent.spi_device.dev_handle is None:
                self.log_signal.emit("设备未连接", 2)
                return
            
        spi_device = self.parent.spi_device
            

        if self.parent.current_crc_mode == 0:
            send_data = Frame.generate_frame(CMD["Ping"], use_crc=True)
        else:
            send_data = Frame.generate_frame(CMD["Ping"])

        # self.LogManager.frame_record(Frame.current_msg_id, "Ping")

        spi_device.spi_send(
            send_data,
            self.parent.spi_clk_mode,
            self.parent.spi_bit_order
        )

        # self.log_signal.emit(f"send_data: {send_data.hex()}", 0)
        print(f"send_data: {send_data.hex()}")

        self.precise_delay(self.delay)

        if self.parent.current_crc_mode == 0:
            received_data = self.parent.spi_device.spi_receive(
                self.parent.spi_clk_mode,
                self.parent.spi_bit_order,
                20
            )
            print(f"received_data: {received_data.hex()}")
            use_crc = True
        else:
            received_data = spi_device.spi_receive(
                self.parent.spi_clk_mode,
                self.parent.spi_bit_order,
                20
            )
            print(f"received_data: {received_data.hex()}")
            use_crc = False

        success, _, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)
        
        if success is True:
            if cmd == CMD["Ack"]:
                self.log_signal.emit("连接成功", 1)
            elif cmd == CMD["Nack"]:
                self.log_signal.emit(f"连接失败: {payload.hex()}", 2)
        else:
            self.log_signal.emit(f"连接失败：{result}", 2)
