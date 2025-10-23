#!/usr/bin/env python3.13
"""
filename: sub_add_data.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-02
description: SPI数据添加子窗口，处理SPI数据的输入和配置
"""

from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget, QMenuBar, QMenu
from PySide6.QtCore import Signal
from ui.Ui_sub_add_data import Ui_SubForm_Data
from PySide6.QtGui import QAction

class SubWindowSpiText(QWidget):
    """SPI数据子窗口类，负责处理SPI数据输入和配置相关的UI连接和业务逻辑."""
    signal = Signal(str, str)

    def __init__(self, parent=None):
        """初始化SPI数据子窗口.

        Args:
            parent: 父窗口实例
        """
        super().__init__()
        self.ui = Ui_SubForm_Data()
        self.ui.setupUi(self)
        self.parent = parent
        self.setWindowTitle('SPI 数据窗口')
        self.ui.line_text.setPlaceholderText("e.g., 00 00 00")
        self.ui.button_data_confirm.clicked.connect(self.send_to_main)
        self.ui.button_data_cancel.clicked.connect(self.close)
        self.ui.button_add.clicked.connect(self.cal_command)

        self.now_command = None

        self.setup_combobox_sync()
        self.create_menu_bar()
        
        self.command = []

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
        
        self.layout().setMenuBar(self.menu_bar)

    def setup_combobox_sync(self):
        """设置 ComboBox 同步变化"""
        # 连接宽度和高度 ComboBox 的 currentIndexChanged 信号
        # 注意：为了避免无限循环，需要使用一个标志来防止递归调用
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
        
    def send_to_main(self):
        """将输入的数据发送到主窗口.从输入框获取名称和文本，验证后通过信号发送到主窗口"""
        name = self.ui.line_name.text()
        text = self.ui.line_text.text()
        if not name or not text:
            QMessageBox.warning(self, 'warning', '请输入名称和文本.')
            return
        self.signal.emit(name, text)
        self.close()

    def switch_page(self):
        """切换页面"""
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def contrast_config(self):
        """配置对比度指令"""
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.label_6.setText("对比度")
        self.ui.config.setVisible(True)
        self.now_command = '对比度'

    def saturation_config(self):
        """配置饱和度指令"""
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.label_6.setText("饱和度")
        self.ui.config.setVisible(False)
        self.now_command = '饱和度'

    def cal_contrast(self):
        """计算对比度指令"""
        
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

        # self.ui.line_data1.setText(f"{result_contrast_int << 8 & 0xFF:02X}")
        # self.ui.line_data2.setText(f"{result_contrast_int & 0xFF:02X}")

        self.command.append(f"对比度{value_contrast}")
        self.command.append(f"{head} {ddr} {result_contrast_int:04X}")

        self.add_window()

    def cal_saturation(self):
        """计算饱和度指令"""
        
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

        # self.ui.line_data1.setText(f"{result_saturation_int << 8 & 0xFF:02X}")
        # self.ui.line_data2.setText(f"{result_saturation_int & 0xFF:02X}")

        self.command.append(f"饱和度{value_saturation}")
        self.command.append(f"{head} {ddr} {result_saturation_int:04X}")

        self.add_window()



    def add_window(self):

        self.signal.emit(self.command[0], self.command[1])
        self.command.clear()

    def cal_command(self):
        """计算指令"""
        if self.now_command == '对比度':
            self.cal_contrast()
        elif self.now_command == '饱和度':
            self.cal_saturation()

