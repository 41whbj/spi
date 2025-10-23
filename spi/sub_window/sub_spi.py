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

    # Send data to main window
    def send_to_main(self):
        name = self.ui.line_name.text()
        text = self.ui.line_text.text()
        if not name or not text:
            QMessageBox.warning(self, 'warning', '请输入名称和文本.')
            return
        self.signal.emit(name, text)
        self.close()