
from PySide6.QtCore import QThread, Signal, QElapsedTimer, Qt
import random
from controller.crc import CRC
# Worker thread for send data with selectable mode
class SendModeThread(QThread):
    log_signal = Signal(str,int)
    finished_signal = Signal()
    progress_signal = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.running = False
        self.delay = 0
        self.items = []
        self.mode = "order"
        self.cycles = 1
        self.times = 1

    def set_params(self, delay, items, mode, cycles = 1, times = 1):
        self.delay = delay
        self.items = items
        self.mode = mode
        self.cycles = cycles
        self.times = times

    #Precise delay, providing high-precision delay control
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

    def send_orderly(self):
        for item in self.items:
            if not self.running:
                break

            op_timer = QElapsedTimer()
            op_timer.start()

            self.send_item_data(item)

            if self.delay > 0:
                op_time = op_timer.elapsed() / 1000.0
                actual_delay = max(0, self.delay - op_time)
                self.precise_delay(actual_delay)

    def send_cyclic(self):
        for i in range(self.cycles):
            if not self.running:
                break
            self.progress_signal.emit(f"循环:{i+1}/{self.cycles}")
            for item in self.items:
                if not self.running:
                    break
            
                op_timer = QElapsedTimer()
                op_timer.start()
                self.send_item_data(item)
            
                if self.delay > 0:
                    op_time = op_timer.elapsed() / 1000.0
                    actual_delay = max(0, self.delay - op_time)
                    self.precise_delay(actual_delay)

    def send_randomly(self):
        for _ in range(self.times):
            if not self.running:
                break
            
            op_timer = QElapsedTimer()
            op_timer.start()
        
            item = random.choice(self.items)
            self.send_item_data(item)
        
            if self.delay > 0:
                op_time = op_timer.elapsed() / 1000.0
                actual_delay = max(0, self.delay - op_time)
                self.precise_delay(actual_delay)

    def run(self):
        self.running = True

        if self.mode == "order":
            self.send_orderly()
        elif self.mode == "circ":
            self.send_cyclic()
        elif self.mode == "random":
            self.send_randomly()
        
        self.running = False
        self.finished_signal.emit()

    def stop(self):
        self.running = False

    def send_item_data(self, item):
        if not self.running:
            return

        data_tuple = item.data(Qt.UserRole)

        if data_tuple and len(data_tuple) >= 2:
            data_name, data_text = data_tuple
        
        if not data_name or data_name not in self.parent.data_map:
            self.log_signal.emit(f"未找到数据 '{data_name}'", 2)
            return

        hex_parts = data_text.strip().split()

        if self.parent.current_crc_mode == 0:# CRC-16
            temp_bytes = []
            for part in hex_parts:
                temp_bytes.append(int(part, 16))
            crc_value = CRC.crc_16_user(temp_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            hex_parts.append(f"{crc_high:02X}")
            hex_parts.append(f"{crc_low:02X}")
        
        if hasattr(self.parent, 'spi_device') and self.parent.spi_device:
            if self.parent.spi_device.jtool is None or self.parent.spi_device.dev_handle is None:
                self.log_signal.emit(f"{data_name} 发送失败: 设备未连接", 2)
                return

        result = self.parent.spi_device.spi_send(
            [int(part, 16) for part in hex_parts], 
            self.parent.spi_clk_mode,
            self.parent.spi_bit_order
        )

        if result is None:
            self.log_signal.emit(f"{data_name} 发送失败", 2)
            return
        
        data = ' '.join(hex_parts)

        self.log_signal.emit(f"{data_name} 发送成功,{data}", 1)

        if self.parent.ui.check_box_receive.isChecked() is False:
            return
        
        received_data = self.parent.spi_device.spi_receive(
            self.parent.spi_clk_mode,
            self.parent.spi_bit_order,
            self.parent.spi_rx_size
        )

        if received_data is not None:
            try:
                data = ' '.join([f"{byte:02X}" for byte in received_data])
                self.log_signal.emit(f"接收数据: {data}", 1)
            except Exception as e:
                self.log_signal.emit(f"错误: {str(e)}", 2)