from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from ui.Ui_sub_add_name import Ui_SubForm_Name

# Sub window for project name
class SubWindowName(QWidget):
    name_updated = Signal(str)

    def __init__(self, parent=None, current_name=""):
        super().__init__()
        self.current_name = current_name
        self.parent = parent

        self.ui = Ui_SubForm_Name()
        self.ui.setupUi(self)
        self.setWindowTitle("修改名称")

        self.ui.button_name_confirm.clicked.connect(self.on_confirm)
        self.ui.button_name_cancel.clicked.connect(self.close)

    def on_confirm(self):
        new_name = self.ui.line_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "警告", "名称不能为空！")
            return
        
        self.name_updated.emit(new_name)
        self.close()