from PySide6.QtCore import QThread, Signal, QElapsedTimer
# from controller.crc import CRC
from .frame import Frame, CMD

class ScanInstanceThread(QThread):
    """实例扫描线程类，用于在后台线程中执行测例扫描操作"""
    # 定义日志信号，用于发送日志消息和级别
    log_signal = Signal(str, int)
    # 定义测例信号，用于发送扫描到的测例列表
    case_signal = Signal(list)

    def __init__(self, application, delay=1):
        """初始化实例扫描线程

        Args:
            application: 应用程序对象
            delay: 扫描延迟时间（秒），默认为1秒
        """
        super().__init__()
        self.application = application
        self.ui = self.application.ui           
        self.delay = delay             # 延迟时间（秒）
        self.running = True            # 线程运行状态标志

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

    def precise_delay(self, seconds):
        """精确延迟函数，可以被中断停止

        Args:
            seconds: 延迟时间（秒）
        """
        # 创建精确计时器
        timer = QElapsedTimer()
        timer.start()
        
        # 将秒转换为毫秒
        target_ms = int(seconds * 1000)

        # timer.elapsed()：检查已经过去的时间
        while self.running and timer.elapsed() < target_ms:
            # 计算剩余时间，继续检查是否达到了目标延迟
            remaining = target_ms - timer.elapsed()

            # 根据剩余时间选择适当的睡眠时间
            if remaining > 10:
                self.msleep(10)        # 剩余时间大于10ms时，休眠10ms
            elif remaining > 1:
                self.msleep(1)         # 剩余时间大于1ms时，休眠1ms

    def stop(self):
        """停止线程执行"""
        self.running = False           # 设置运行状态为False以停止线程

    def run(self):
        """线程主执行函数，执行测例扫描操作"""

        send_data = Frame.generate_frame(CMD["GetCaseList"])

        # print(f"发送的数据：{send_data}，类型：{type(send_data)}")  # 打印发送数据（调试用）
        
        # 发送数据
        self.application.spi_controller.spi_send(
            send_data.hex(),
            self.clk_mode,              # SPI时钟模式
            self.bit_order,
            log = False 
        )

        # self.log_signal.emit(f"send_data: {send_data.hex()}", 0)  # 发送日志（被注释）
        # print(f"send_data: {send_data.hex()}")  # 打印发送数据（调试用）

        # 执行精确延迟
        self.precise_delay(self.delay)
        
        # 提供一个128字节的接收区域来接收数据
        received_data = self.application.spi_controller.spi_receive(
            self.clk_mode,
            self.bit_order,
            128,                        # 接收缓冲区大小为128字节
            log = False
        )
        
        # print(f"测试接收128字节数据：received_data: {received_data.hex()}")  # 打印接收数据（调试用）

        # 根据CRC模式设置解析标志
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # 解析接收到的帧数据
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查解析是否成功
        if success is False:
            self.log_signal.emit(f"获取测例失败：{result}", 2)
            return
        
        # 检查命令是否为否定应答(Nack)
        if cmd == CMD["Nack"]:
            self.log_signal.emit("RISC-V答应失败", 2)
            return
        
        # self.log_signal.emit(f"原始负载: {payload.hex()}", 1)  # 原始负载日志（被注释）
        # print(f"payload: {payload}")  # 打印负载数据（调试用）

        # 解析测例数据
        case = Frame.parse_case(payload)

        # print(f"case: {case}")  # 打印测例数据（调试用）

        # 发送测例列表信号
        self.case_signal.emit(case)

