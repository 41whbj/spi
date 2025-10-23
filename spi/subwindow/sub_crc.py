from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from ui.Ui_sub_crc import Ui_SubForm_CRC

# Sub window for CRC
class SubWindowCRC(QWidget):
    crc_updated = Signal(int)
    user_define = False

    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_SubForm_CRC()
        self.ui.setupUi(self)
        self.setWindowTitle("CRC修改页面")
        self.parent = parent

        self.crc_init()

        if parent and hasattr(parent, 'current_crc_mode') and parent.current_crc_mode != -1:
            self.ui.check_box_crc_enable.setChecked(True)
            self.crc_enable()

        self.ui.check_box_crc_enable.stateChanged.connect(self.crc_enable)
        self.ui.button_crc_confirm.clicked.connect(self.crc_confirm)
        self.ui.button_crc_cancel.clicked.connect(self.crc_close)        

    def crc_init(self):
        setEnable_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]

        for widget in setEnable_widgets:
            widget.setEnabled(False)

    def crc_enable(self):
        is_enabled = self.ui.check_box_crc_enable.isChecked()

        clear_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
        ]

        setEnable_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]
        
        check_boxes = [
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]

        # Manage Widget States
        if not is_enabled:
            for widget in clear_widgets:
                widget.clear()

            for widget in setEnable_widgets:
                widget.setEnabled(False)

            for check_box in check_boxes:
                check_box.setChecked(False)
        else:
            self.crc_range()
            self.crc_type()
            self.crc_16_user_show()


    def crc_range(self):
        self.ui.combo_box_crc_range.addItems(["写校验"])
        self.ui.combo_box_crc_range.setEnabled(True)
    
    def crc_type(self):
        self.ui.combo_box_crc_type.addItems(["CRC-16(自定义)"])
        self.ui.combo_box_crc_type.setEnabled(True)

    def crc_16_user_show(self):
        self.ui.combo_box_crc_width.addItems(["16"])
        self.ui.line_edit_crc_poly.setText("8005")
        self.ui.line_edit_crc_formula.setText("x16 + x15 + x2 + 1")
        self.ui.line_edit_crc_init.setText("FFFF")
        self.ui.line_edit_crc_xorout.setText("0000")
        self.ui.check_box_in_reversal.setChecked(False)
        self.ui.check_box_out_reversal.setChecked(False)
        self.ui.check_box_high_first.setChecked(True)
    
    def crc_confirm(self):
        if not self.ui.check_box_crc_enable.isChecked():
            self.crc_updated.emit(-1)
        else:
            self.crc_updated.emit(self.ui.combo_box_crc_type.currentIndex())
        self.close()

    def crc_close(self):
        self.close()