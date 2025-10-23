
from PySide6.QtCore import QThread, Signal, QElapsedTimer, Qt
import random
from crc_manager.crc import CRC
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
        # self.cycles = 1
        self.times = 1

    def set_params(self, delay, items, mode, cycles = '', times = 1, data_poll = False):
        self.delay = delay
        self.items = items
        self.mode = mode
        self.cycles = cycles
        self.times = times
        self.data_poll = data_poll

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
        # Send data orderly
        if self.data_poll is False:
            self.send_group(self.items)
        else:
            self.send_poll(self.items)

    def send_cyclic(self):
        # Send data cyclic

        # When not cycles, Keep send data until  self.running is False
        if not self.cycles:
            cycle_count = 0

            while self.running:
                cycle_count += 1
                self.progress_signal.emit(f"持续发送中，循环第{cycle_count}次")

                if self.data_poll is False:
                    self.send_group(self.items)
                else:
                    self.send_poll(self.items, cyclic_mode=True)
                    self.precise_delay(self.delay)
            return
        
        for i in range(self.cycles):
            if not self.running:
                break
            self.progress_signal.emit(f"循环:{i+1}/{self.cycles}")
            
            if self.data_poll is False:
                self.send_group(self.items)
            else:
                self.send_poll(self.items, cyclic_mode=True)
                if i < (self.cycles - 1) and self.delay > 0:
                    self.precise_delay(self.delay)

    def send_randomly(self):
        for _ in range(self.times):
            if not self.running:
                break
            
            op_timer = QElapsedTimer()
            op_timer.start()
        
            # Randomly select an item from self.items
            group = random.choice(self.items)
            if isinstance(group, (list,tuple)) and len(group) > 0:
                if isinstance(group[0], (list,tuple)) and len(group[0]) >= 2:
                    item = random.choice(group)

            else:
                item = group

            self.send_item_data(item)
        
            if self.delay > 0:
                op_time = op_timer.elapsed() / 1000.0
                actual_delay = max(0, self.delay - op_time)
                self.precise_delay(actual_delay)

    def send_poll(self, items, cyclic_mode=False):
        # Send all the data group, user delay control group send interval.
        for i, group in enumerate(items):
            if not self.running:
                break

            for j, item in enumerate(group):
                if not self.running:
                    break

                op_timer = QElapsedTimer()
                op_timer.start()

                self.send_item_data(item)

                if j < (len(group) - 1):
                    op_time = op_timer.elapsed() / 1000.0
                    # Each item in group has 0.1s delay
                    actual_delay = max(0, 0.1 - op_time)
                    self.precise_delay(actual_delay)

            if cyclic_mode is True and i < (len(items) - 1):
                self.progress_signal.emit("发送下一组数据")

            if i < (len(items) - 1) and self.delay > 0:
                # Add user delay when send next group
                self.precise_delay(self.delay)

    def send_group(self, items):
        # Send data group in list show, user delay control data send interval.
        for item in items:
            if not self.running:
                break

            op_timer = QElapsedTimer()
            op_timer.start()

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

        if isinstance(item,(tuple,list)) and len(item) >= 2:
            data_name, data_text = item
        else:
            data_tuple = item.data(Qt.UserRole)
            if data_tuple and len(data_tuple) >= 2:
                data_name, data_text = data_tuple

        hex_parts = data_text.strip().split()

        # CRC-16 user defined
        if self.parent.current_crc_mode == 0:
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