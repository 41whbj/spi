import traceback
import time
import os
import re
from ctypes import (c_int, POINTER, c_void_p, 
        c_uint32, c_ubyte, byref, windll, c_char_p
    )

class SPI:

    dev_spi = 2
    err_none = 0

    low_1edg = 0

    msb = 0

    ERROR_CODES = {
        1: "参数错误",
        2: "USB 断开",
        4: "USB发送忙",
        8: "正在等待回复",
        16: "通信超时",
        32: "通信数据错误",
        64: "返回失败参数"
    }

    dev_handle = None
    
    def __init__(self, usb_dev=-1, log_callback=None):
        self.usb_id = usb_dev
        self.log_callback = log_callback
        self.jtool = None
        self.device_name = ""

        try:
            dll_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "jtool.dll"
            )
            self.jtool = windll.LoadLibrary(dll_path)

            self.jtool.DevicesScan.argtypes = [c_int, POINTER(c_int)]
            self.jtool.DevicesScan.restype = c_char_p
            self.jtool.DevOpen.argtypes = [c_int, c_void_p, c_int]
            self.jtool.DevOpen.restype = c_void_p

            self.jtool.JSPISetVcc.argtypes = [c_void_p, c_int]
            self.jtool.JSPISetVcc.restype = c_int
            self.jtool.JSPISetVio.argtypes = [c_void_p, c_int]
            self.jtool.JSPISetVio.restype = c_int
            self.jtool.JSPISetSpeed.argtypes = [c_void_p, c_int]
            self.jtool.JSPISetSpeed.restype = c_int

            self.jtool.SPIWriteOnly.argtypes = [
                c_void_p, c_int, c_int, c_uint32, POINTER(c_ubyte)
            ]
            self.jtool.SPIWriteOnly.restype = c_int

            self.jtool.SPIReadOnly.argtypes = [
                c_void_p, c_int, c_int, c_uint32, POINTER(c_ubyte)
            ]
            self.jtool.SPIReadOnly.restype = c_int

            # 添加全双工模式函数声明
            self.jtool.SPIWriteRead.argtypes = [
                c_void_p, c_int, c_int, c_uint32, POINTER(c_ubyte), POINTER(c_ubyte)
            ]
            self.jtool.SPIWriteRead.restype = c_int

            time.sleep(0.3)

        except Exception as e:
            self.log(f"jtool.dll 加载加载失败: {str(e)}")
            self.log(traceback.format_exc())

    def open_device(self):
        if self.jtool is None:
            self.log("jtool.dll 未加载")
            return False
        
        try:
            # Close existing device handle if exists
            if self.dev_handle is not None:
                self.dev_handle = None
            dev_cnt = c_int(0)

            devices_str = self.jtool.DevicesScan(self.dev_spi, byref(dev_cnt))
            if devices_str:
                self.parse_device_info(devices_str)

            if dev_cnt.value <= 0:
                self.log("未检测到SPI设备", 2)
                return False

            self.dev_handle = self.jtool.DevOpen(
                self.dev_spi, None, self.usb_id
            )

            if not self.dev_handle:
                self.log("SPI设备打开失败", 2)
                return False
            
            if self.dev_handle and self.jtool:
                self.jtool.JSPISetVcc(self.dev_handle, c_int(0))
                self.jtool.JSPISetVio(self.dev_handle, c_int(0))
                self.jtool.JSPISetSpeed(self.dev_handle, c_int(0))
                self.log("SPI设备打开成功", 1)
                return True

        except Exception as e:
            self.dev_handle = None
            self.log(f"打开设备异常: {str(e)}")
            return False
        
    def parse_device_info(self, devices_str):
        device_info = devices_str.decode('utf-8')
        sn_start = device_info.find('SN:')
        
        if sn_start != -1:
            sn_part = device_info[sn_start+3:]
            sn_match = re.search(r'([A-F0-9]{8})', sn_part)
            
            if sn_match:
                full_sn = sn_match.group(1)
                middle_sn = full_sn[4:8] if len(full_sn) >= 8 else full_sn

                device_type_match = re.search(r'(JTool-[A-Za-z]+)', device_info)
                device_type = device_type_match.group(1) if device_type_match else "SPI设备"
                
                self.device_name = f"{device_type}({middle_sn})"

    def get_device_name(self):
        return self.device_name if self.device_name else "未知设备"

    def spi_send(self, data, clk_mode=None, bit_order=None):
        if self.jtool is None or self.dev_handle is None:
            self.log("jtool.dll 未加载或设备未打开")
            return None

        try:
            if clk_mode is None:
                clk_mode = self.low_1edg
            if bit_order is None:
                bit_order = self.msb
            if isinstance(data, bytearray):
                data_array = (c_ubyte * len(data))(*data)
                size = len(data)
            elif isinstance(data, (list, bytes)):
                data_array = (c_ubyte * len(data))(*data)
                size = len(data)
            elif isinstance(data, str):
                hex_parts = data.strip().split()
                data_list = [int(part, 16) for part in hex_parts]
                data_array = (c_ubyte * len(data_list))(*data_list)
                size = len(data_list)
            else:
                self.log(f"不支持的数据类型: {type(data)}", 2)
                return None
            
            # print(f"[句柄日志] dev_handle为: {self.dev_handle}")

            result = self.jtool.SPIWriteOnly(
                self.dev_handle,
                c_int(clk_mode),
                c_int(bit_order),
                c_uint32(size),
                data_array
            )

            if result == self.err_none:
                return True
            else:
                self.log(f"SPI发送失败, {self.ERROR_CODES.get(result)}", 2)
                return None
        except Exception as e:
            self.log(f"SPI发送异常: {str(e)}", 2)
            self.log(traceback.format_exc())
            return None

    def spi_receive(self,clk_mode=None, bit_order=None,size = None):
        if self.jtool is None or self.dev_handle is None:
            self.log("jtool.dll 未加载或设备未打开")
            return None

        try:
            if clk_mode is None:
                clk_mode = self.low_1edg
            if bit_order is None:
                bit_order = self.msb
            if size is None:
                size = 1
            
            receive_buffer = (c_ubyte * size)()

            data_size = len(receive_buffer)

            result = self.jtool.SPIReadOnly(
                self.dev_handle,
                c_int(clk_mode),
                c_int(bit_order),
                c_uint32(data_size),
                receive_buffer
            )

            if result == self.err_none:
                received_data = bytes(receive_buffer)
                return received_data
            else:
                self.log(f"SPI接收失败, {self.ERROR_CODES.get(result)}", 2)
                return None

        except Exception as e:
            self.log(f"SPI接收异常: {str(e)}", 2)
            self.log(traceback.format_exc())
            return None

    # Log message via callback or print
    def log(self, message, state=0):
        if self.log_callback:
            self.log_callback(message, state)

    def spi_transfer(self, data, clk_mode=None, bit_order=None):
        """全双工SPI传输模式
        
        Args:
            data: 要发送的数据，可以是bytes、bytearray、list或hex字符串
            clk_mode: 时钟模式，默认为low_1edg
            bit_order: 位序，默认为msb
            
        Returns:
            bytes: 接收到的数据，如果失败则返回None
        """
        if self.jtool is None or self.dev_handle is None:
            self.log("jtool.dll 未加载或设备未打开")
            return None

        try:
            if clk_mode is None:
                clk_mode = self.low_1edg
            if bit_order is None:
                bit_order = self.msb
                
            # 处理发送数据
            if isinstance(data, bytearray):
                send_data_array = (c_ubyte * len(data))(*data)
                size = len(data)
            elif isinstance(data, (list, bytes)):
                send_data_array = (c_ubyte * len(data))(*data)
                size = len(data)
            elif isinstance(data, str):
                hex_parts = data.strip().split()
                data_list = [int(part, 16) for part in hex_parts]
                send_data_array = (c_ubyte * len(data_list))(*data_list)
                size = len(data_list)
            else:
                self.log(f"不支持的数据类型: {type(data)}", 2)
                return None
            
            # 创建接收缓冲区
            receive_buffer = (c_ubyte * size)()
            
            # 执行全双工传输
            result = self.jtool.SPIWriteRead(
                self.dev_handle,
                c_int(clk_mode),
                c_int(bit_order),
                c_uint32(size),
                send_data_array,
                receive_buffer
            )

            if result == self.err_none:
                received_data = bytes(receive_buffer)
                return received_data
            else:
                self.log(f"SPI全双工传输失败, {self.ERROR_CODES.get(result)}", 2)
                return None
                
        except Exception as e:
            self.log(f"SPI全双工传输异常: {str(e)}", 2)
            self.log(traceback.format_exc())
            return None

