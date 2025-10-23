from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from ui.Ui_sub_add_data import Ui_SubForm_Data

# Sub window for adding SPI text data
class SubWindowSpiText(QWidget):
    signal = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_SubForm_Data()
        self.ui.setupUi(self)
        self.parent = parent
        self.setWindowTitle('SPI 数据窗口')
        self.ui.line_text.setPlaceholderText("e.g., 00 00 00")
        self.ui.button_data_confirm.clicked.connect(self.send_to_main)
        self.ui.button_data_cancel.clicked.connect(self.close)
        self.ui.button_switch.clicked.connect(self.switch_page)
        self.ui.button_cal.clicked.connect(self.cal_data)
        self.ui.button_add2window.clicked.connect(self.add2window)
        self.command = []
        
        # 从主窗口加载保存的数据
        self.load_data_from_main_window()

    # Send data to main window
    def send_to_main(self):
        name = self.ui.line_name.text()
        text = self.ui.line_text.text()
        if not name or not text:
            QMessageBox.warning(self, 'warning', '请输入名称和文本.')
            return
        self.signal.emit(name, text)
        # 保存数据到主窗口
        self.save_data_to_main_window()
        self.close()

    def switch_page(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def cal_data(self):
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return

        lane = self.ui.line_lane.text()
        if not lane:
            QMessageBox.warning(self, 'warning', '请输入通道.')
            return
    
        color_depth = self.ui.line_color_depth.text()
        if not color_depth:
            QMessageBox.warning(self, 'warning', '请输入颜色深度.')
            return

        if color_depth not in ['256', '1024']:
            QMessageBox.warning(self, 'warning', '颜色深度必须为256或1024.')
            return
        
        width = self.ui.line_width.text()
        if not width:
            QMessageBox.warning(self, 'warning', '请输入宽度.')
            return
        
        height = self.ui.line_height.text()
        if not height:
            QMessageBox.warning(self, 'warning', '请输入高度.')
            return
        
        input_contrast = self.ui.line_input_contrast.text()
        input_saturation = self.ui.line_input_saturation.text()
        
        if not input_contrast or not input_saturation:
            QMessageBox.warning(self, 'warning', '输入为空.')
            return
        value_contrast = float(input_contrast)
        value_saturation = float(input_saturation)

        if 0 <= value_contrast <= 2 and 1 <= value_saturation <= 2:

            result_contrast = (int(width) * int(height)) / int(lane) / 64 / int(color_depth) * value_contrast

            result_contrast = max(0, min(result_contrast, 0xFF))

            result_contrast_int = int(result_contrast)

            result_saturation = 64 * (value_saturation - 1)

            result_saturation = max(0, min(result_saturation, 0xFF))

            result_saturation_int = int(result_saturation)

            self.ui.line_data1.setText(f"{result_saturation_int:02X}")
            self.ui.line_data2.setText(f"{result_contrast_int:02X}")

            self.command.append(f"饱和度{value_saturation}对比度{value_contrast}")
            self.command.append(f"{head} {ddr} {result_saturation_int:02X} {result_contrast_int:02X}")   
        else:
            QMessageBox.warning(self, 'warning', '输入错误.')
    def add2window(self):
        if not self.command:
            QMessageBox.warning(self, 'warning', '请先计算数据.')
            return
        self.signal.emit(self.command[0], self.command[1])
        # 保存数据到主窗口
        self.save_data_to_main_window()
        self.command.clear()
        # self.close()
        
    def save_data_to_main_window(self):
        """将子窗口的数据保存到主窗口"""
        if self.parent:
            # 创建一个字典来保存子窗口的数据
            sub_window_data = {
                'head': self.ui.line_head.text(),
                'ddr': self.ui.line_ddr.text(),
                'data1': self.ui.line_data1.text(),
                'data2': self.ui.line_data2.text(),
                'lane': self.ui.line_lane.text(),
                'color_depth': self.ui.line_color_depth.text(),
                'width': self.ui.line_width.text(),
                'height': self.ui.line_height.text(),
                'input_contrast': self.ui.line_input_contrast.text(),
                'input_saturation': self.ui.line_input_saturation.text(),
            }
            
            # 将数据保存到主窗口的属性中
            self.parent.spi_sub_window_data = sub_window_data

    def load_data_from_main_window(self):
        """从主窗口加载保存的数据"""
        if self.parent and hasattr(self.parent, 'spi_sub_window_data'):
            sub_window_data = self.parent.spi_sub_window_data
            
            # 从主窗口恢复数据
            self.ui.line_head.setText(sub_window_data.get('head', ''))
            self.ui.line_ddr.setText(sub_window_data.get('ddr', ''))
            self.ui.line_data1.setText(sub_window_data.get('data1', ''))
            self.ui.line_data2.setText(sub_window_data.get('data2', ''))
            self.ui.line_lane.setText(sub_window_data.get('lane', ''))
            self.ui.line_color_depth.setText(sub_window_data.get('color_depth', ''))
            self.ui.line_width.setText(sub_window_data.get('width', ''))
            self.ui.line_height.setText(sub_window_data.get('height', ''))
            self.ui.line_input_contrast.setText(sub_window_data.get('input_contrast', ''))
            self.ui.line_input_saturation.setText(sub_window_data.get('input_saturation', ''))
