from PySide6.QtCore import QThread, Signal, QElapsedTimer
# from controller.crc import CRC
from .frame import Frame, CMD
# from .log import LogManager
# from .pc_mcu2window import PC_MCU2Window

class ScanDeviceThread(QThread):
    """设备扫描线程类，用于在后台线程中执行设备连接检测操作"""
    # 定义日志信号，用于发送日志消息和级别
    log_signal = Signal(str, int)

    def __init__(self, application, delay=1):
        """初始化设备扫描线程

        Args:
            application: 应用程序对象，用于访问全局资源
            delay: 扫描延迟时间（秒），默认为1秒
        """
        super().__init__()
        self.application = application 
        self.ui = self.application.ui
        self.delay = delay
        self.running = True 

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

    def precise_delay(self, seconds):
        """精确延迟函数，可以被中断停止

        Args:
            seconds: 延迟时间（秒）
        """
        timer = QElapsedTimer()       # 创建精确计时器
        timer.start()                 # 启动计时器

        target_ms = int(seconds * 1000)  # 将秒转换为毫秒

        # 循环等待直到达到目标时间或线程被停止
        while self.running and timer.elapsed() < target_ms:
            remaining = target_ms - timer.elapsed()  # 计算剩余时间

            # 根据剩余时间选择适当的睡眠时间
            if remaining > 10:
                self.msleep(10)       # 剩余时间大于10ms时，休眠10ms
            elif remaining > 1:
                self.msleep(1)        # 剩余时间大于1ms时，休眠1ms

    def stop(self):
        """停止线程执行"""
        self.running = False          # 设置运行状态为False以停止线程

    def run(self):
        """线程主执行函数，执行设备扫描和连接检测"""


        # 生成帧
        send_data = Frame.generate_frame(CMD["Ping"])

        # self.LogManager.frame_record(Frame.current_msg_id, "Ping")  # 帧记录（被注释）

        self.application.spi_controller.spi_send(
            send_data.hex(),
            self.clk_mode,
            self.bit_order,
            log = False 
            )

        # self.log_signal.emit(f"send_data: {send_data.hex()}", 0)  # 发送日志（被注释）
        # print(f"send_data: {send_data.hex()}")  # 打印发送数据（调试用）

        self.precise_delay(self.delay)  # 执行精确延迟

        # 根据CRC模式接收响应数据
        if self.application.current_crc_mode == 0:
            # CRC模式下接收数据
            received_data = self.application.spi_controller.spi_receive(
                self.clk_mode,
                self.bit_order,
                20,  # 接收缓冲区大小为20字节
                log = False
            )
            # print(f"received_data: {received_data.hex()}")  # 打印接收数据（调试用）
            use_crc = True  # 设置CRC使用标志
        else:
            # 非CRC模式下接收数据
            received_data = self.application.spi_controller.spi_receive(
                self.clk_mode,
                self.bit_order,
                20  # 接收缓冲区大小为20字节
            )
            # print(f"received_data: {received_data.hex()}")  # 打印接收数据（调试用）
            use_crc = False  # 设置CRC使用标志

        # 解析接收到的帧数据
        success, _, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)
        
        # 根据解析结果处理响应
        if success is True:
            # 解析成功，检查命令类型
            if cmd == CMD["Ack"]:
                # 收到确认响应，连接成功
                self.log_signal.emit("连接成功", 1)
            elif cmd == CMD["Nack"]:
                # 收到否定响应，连接失败
                self.log_signal.emit("RISC-V答应失败", 2)
        else:
            # 解析失败，报告错误原因
            self.log_signal.emit(f"连接失败：{result}", 2)