from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget, QMenuBar, QMenu
from PySide6.QtCore import Signal
from ui.Ui_sub_add_data import Ui_SubForm_Data
from PySide6.QtGui import QKeySequence, QShortcut, QAction

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
        # self.ui.button_switch.clicked.connect(self.switch_page)
        # self.ui.button_cal.clicked.connect(self.cal_data)
        # self.ui.button_contrast.clicked.connect(self.cal_data)
        self.command = []

        # 添加键盘快捷键切换页面
        self.setup_shortcuts()
        self.setup_combobox_sync()
        self.create_menu_bar()
        
        self.command = []
        
        # 从主窗口加载保存的数据
        # self.load_data_from_main_window()

    def create_menu_bar(self):
        """创建菜单栏"""
        # 创建菜单栏
        self.menu_bar = QMenuBar(self)

        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                padding: 2px;
                font-size: 12px;
            }
            
            QMenuBar::item {
                background: transparent;
                padding: 4px 8px;
                margin: 2px;
            }
            
            QMenuBar::item:selected {
                background: #d0d0d0;
            }
            
            QMenuBar::item:pressed {
                background: #c0c0c0;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #d0d0d0;
                padding: 2px;
                font-size: 10px;
            }
            
            QMenu::item {
                padding: 4px 20px;
            }
            
            QMenu::item:selected {
                background-color: #d0d0d0;
            }
        """)
        
        # 创建页面控制菜单
        window_menu = QMenu("页面控制", self)
        self.menu_bar.addMenu(window_menu)
        
        # 添加一般页面菜单项
        common_action = QAction("一般页面", self)
        common_action.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        window_menu.addAction(common_action)
        
        # 创建快速指令子菜单
        fast_menu = QMenu("快速指令", self)
        window_menu.addMenu(fast_menu)

        # 添加对比度指令到快速指令子菜单
        contrast_action = QAction("对比度指令", self)
        contrast_action.triggered.connect(self.contrast_config)  # 连接现有的对比度计算函数
        fast_menu.addAction(contrast_action)

        # 添加对比度指令到快速指令子菜单
        contrast_action = QAction("饱和度指令", self)
        contrast_action.triggered.connect(self.saturation_config)
        fast_menu.addAction(contrast_action)
        
        # 将菜单栏添加到布局中
        self.layout().setMenuBar(self.menu_bar)
        
        # # 添加菜单项
        # clear_action = QAction("清空", self)
        # clear_action.triggered.connect(self.clear_fields)
        # edit_menu.addAction(clear_action)
        
        # # 创建视图菜单
        # view_menu = QMenu("视图", self)
        # self.menu_bar.addMenu(view_menu)
        
        # # 添加切换页面菜单项
        # switch_page_action = QAction("切换页面", self)
        # switch_page_action.setShortcut(QKeySequence("Ctrl+Tab"))
        # switch_page_action.triggered.connect(self.switch_page)
        # view_menu.addAction(switch_page_action)
        
        # # 创建帮助菜单
        # help_menu = QMenu("帮助", self)
        # self.menu_bar.addMenu(help_menu)
        
        # # 添加菜单项
        # about_action = QAction("关于", self)
        # about_action.triggered.connect(self.show_about)
        # help_menu.addAction(about_action)
        
        # 将菜单栏添加到布局中
        self.layout().setMenuBar(self.menu_bar)

    def setup_shortcuts(self):
        """设置键盘快捷键"""
        # 使用 Ctrl+Tab 切换页面
        shortcut_switch = QShortcut(QKeySequence("Ctrl+Tab"), self)
        shortcut_switch.activated.connect(self.switch_page)

    def setup_combobox_sync(self):
        """设置 ComboBox 同步变化"""
        # 连接宽度和高度 ComboBox 的 currentIndexChanged 信号
        # 注意：为了避免无限循环，我们需要使用一个标志来防止递归调用
        self._updating = False
        
        # 连接信号
        self.ui.comb_box_width.currentIndexChanged.connect(self.on_width_changed)
        self.ui.comb_box_height.currentIndexChanged.connect(self.on_height_changed)

    def on_width_changed(self, index):
        """当宽度 ComboBox 改变时，同步改变高度 ComboBox"""
        if not self._updating:
            self._updating = True
            self.ui.comb_box_height.setCurrentIndex(index)
            self._updating = False

    def on_height_changed(self, index):
        """当高度 ComboBox 改变时，同步改变宽度 ComboBox"""
        if not self._updating:
            self._updating = True
            self.ui.comb_box_width.setCurrentIndex(index)
            self._updating = False
        
    # Send data to main window
    def send_to_main(self):
        name = self.ui.line_name.text()
        text = self.ui.line_text.text()
        if not name or not text:
            QMessageBox.warning(self, 'warning', '请输入名称和文本.')
            return
        self.signal.emit(name, text)
        # 保存数据到主窗口
        # self.save_data_to_main_window()
        self.close()

    def switch_page(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def contrast_config(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.label_6.setText("对比度")
        self.ui.config.setVisible(True)
        self._disconnect_button_signal()
        self.ui.button_add.clicked.connect(self.cal_contrast)

    def saturation_config(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.label_6.setText("饱和度")
        self.ui.config.setVisible(False)
        self._disconnect_button_signal()
        self.ui.button_add.clicked.connect(self.cal_saturation)

    def cal_contrast(self):
        
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return

        lane = self.ui.comb_box_lane.currentText()
    
        color_depth = self.ui.comb_box_color_depth.currentText()

        width = self.ui.comb_box_width.currentText()

        height = self.ui.comb_box_height.currentText()
 
    
    #     input_contrast = self.ui.line_input_contrast.text()
        input_contrast = self.ui.line_input.text()

        if not input_contrast:
            QMessageBox.warning(self, 'warning', '请输入对比度.')
            return
        
        value_contrast = float(input_contrast)

        if not 0 <= value_contrast <= 2:
            QMessageBox.warning(self, 'warning', '对比度输入错误.')
            return
        
        result_contrast = (int(width) * int(height)) / int(lane) / 64 / int(color_depth) * value_contrast

        result_contrast = max(0, min(result_contrast, 0xFFFF))

        result_contrast_int = int(result_contrast)

        self.ui.line_data1.setText(f"{result_contrast_int << 8 & 0xFF:02X}")
        self.ui.line_data2.setText(f"{result_contrast_int & 0xFF:02X}")

        self.command.append(f"对比度{value_contrast}")
        self.command.append(f"{head} {ddr} {result_contrast_int:04X}")

        self.add_window()

    def _disconnect_button_signal(self):
        """断开button_add的现有连接"""
        try:
            self.ui.button_add.clicked.disconnect()
        except RuntimeError:
            # 没有连接时会抛出异常，忽略即可
            pass
        
    #     if not input_contrast or not input_saturation:
    #         QMessageBox.warning(self, 'warning', '输入为空.')
    #         return
    #     value_contrast = float(input_contrast)
    #     value_saturation = float(input_saturation)

    #     if 0 <= value_contrast <= 2 and 1 <= value_saturation <= 2:

    #         result_contrast = (int(width) * int(height)) / int(lane) / 64 / int(color_depth) * value_contrast

    #         result_contrast = max(0, min(result_contrast, 0xFF))

    #         result_contrast_int = int(result_contrast)

    #         result_saturation = 64 * (value_saturation - 1)

    #         result_saturation = max(0, min(result_saturation, 0xFF))

    #         result_saturation_int = int(result_saturation)

    #         self.ui.line_data1.setText(f"{result_saturation_int:02X}")
    #         self.ui.line_data2.setText(f"{result_contrast_int:02X}")

    #         self.command.append(f"饱和度{value_saturation}对比度{value_contrast}")
    #         self.command.append(f"{head} {ddr} {result_saturation_int:02X} {result_contrast_int:02X}")   
    #     else:
    #         QMessageBox.warning(self, 'warning', '输入错误.')

    def cal_saturation(self):
        
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return
        
        input_saturation = self.ui.line_input.text()

        if not input_saturation:
            QMessageBox.warning(self, 'warning', '请输入饱和度.')
            return
        
        value_saturation = float(input_saturation)

        if not 1 <= value_saturation <= 2:
            QMessageBox.warning(self, 'warning', '饱和度输入错误.')
            return
        
        result_saturation = 64 * (value_saturation - 1)

        result_saturation = max(0, min(result_saturation, 0xFFFF))

        result_saturation_int = int(result_saturation)

        self.ui.line_data1.setText(f"{result_saturation_int << 8 & 0xFF:02X}")
        self.ui.line_data2.setText(f"{result_saturation_int & 0xFF:02X}")

        self.command.append(f"饱和度{value_saturation}")
        self.command.append(f"{head} {ddr} {result_saturation_int:04X}")

        self.add_window()



    def add_window(self):
        # if not self.command:
        #     QMessageBox.warning(self, 'warning', '请先计算数据.')
        #     return
        self.signal.emit(self.command[0], self.command[1])
        # 保存数据到主窗口
        # self.save_data_to_main_window()
        self.command.clear()
        # self.close()
        
    # def save_data_to_main_window(self):
    #     """将子窗口的数据保存到主窗口"""
    #     if self.parent:
    #         # 创建一个字典来保存子窗口的数据
    #         sub_window_data = {
    #             'head': self.ui.line_head.text(),
    #             'ddr': self.ui.line_ddr.text(),
    #             'data1': self.ui.line_data1.text(),
    #             'data2': self.ui.line_data2.text(),
    #             'lane': self.ui.line_lane.text(),
    #             'color_depth': self.ui.line_color_depth.text(),
    #             'width': self.ui.line_width.text(),
    #             'height': self.ui.line_height.text(),
    #             'input_contrast': self.ui.line_input_contrast.text(),
    #             'input_saturation': self.ui.line_input_saturation.text(),
    #         }
            
    #         # 将数据保存到主窗口的属性中
    #         self.parent.spi_sub_window_data = sub_window_data

    # def load_data_from_main_window(self):
    #     """从主窗口加载保存的数据"""
    #     if self.parent and hasattr(self.parent, 'spi_sub_window_data'):
    #         sub_window_data = self.parent.spi_sub_window_data
            
    #         # 从主窗口恢复数据
    #         self.ui.line_head.setText(sub_window_data.get('head', ''))
    #         self.ui.line_ddr.setText(sub_window_data.get('ddr', ''))
    #         self.ui.line_data1.setText(sub_window_data.get('data1', ''))
    #         self.ui.line_data2.setText(sub_window_data.get('data2', ''))
    #         self.ui.line_lane.setText(sub_window_data.get('lane', ''))
    #         self.ui.line_color_depth.setText(sub_window_data.get('color_depth', ''))
    #         self.ui.line_width.setText(sub_window_data.get('width', ''))
    #         self.ui.line_height.setText(sub_window_data.get('height', ''))
    #         self.ui.line_input_contrast.setText(sub_window_data.get('input_contrast', ''))
    #         self.ui.line_input_saturation.setText(sub_window_data.get('input_saturation', ''))
