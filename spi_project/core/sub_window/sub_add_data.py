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
from core.ui.Ui_sub_add_data import Ui_SubForm_Data
from PySide6.QtGui import QAction

class SubWindowAddData(QWidget):
    """
    SPI数据子窗口类，负责处理SPI数据输入和配置相关的UI连接和业务逻辑
    """
    # 定义信号，用于向主窗口发送数据
    data_added = Signal(str, str)

    def __init__(self, application):
        """
        初始化SPI数据子窗口
        
        Args:
            application: 应用实例
        """
        super().__init__()
        # 初始化UI界面
        self.ui = Ui_SubForm_Data()
        self.ui.setupUi(self)
        self.application = application
        
        # 设置窗口标题
        self.setWindowTitle('SPI 数据窗口')
        
        # 设置文本输入框的占位符提示
        self.ui.line_text.setPlaceholderText("e.g., 00 00 00")
        
        # 连接按钮信号与槽函数
        self.ui.button_data_confirm.clicked.connect(self.send_to_main)
        self.ui.button_data_cancel.clicked.connect(self.close)
        self.ui.button_add.clicked.connect(self.cal_command)

        # 当前指令类型标识
        self.now_command = None

        # 设置ComboBox同步变化
        self.setup_combobox_sync()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 存储指令数据的列表
        self.command = []

    def create_menu_bar(self):
        """
        创建菜单栏
        
        创建包含页面控制和快速指令功能的菜单栏，
        用于方便用户切换界面和快速生成常用指令
        """
        # 创建菜单栏对象
        self.menu_bar = QMenuBar(self)

        # 设置菜单栏样式
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
        
        # 添加一般页面菜单项，点击后切换到第一页
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

        # 添加饱和度指令到快速指令子菜单
        saturation_action = QAction("饱和度指令", self)
        saturation_action.triggered.connect(self.saturation_config)
        fast_menu.addAction(saturation_action)

        # 添加饱和度+对比度指令到快速指令子菜单
        saturation_contrast_action = QAction("饱和度+对比度指令", self)
        saturation_contrast_action.triggered.connect(self.saturation_contrast_config)
        fast_menu.addAction(saturation_contrast_action)

        # 添加自然饱和度令到快速指令子菜单
        natural_saturation_action = QAction("自然饱和度令", self)
        natural_saturation_action.triggered.connect(self.natural_saturation_config)
        fast_menu.addAction(natural_saturation_action)
        
        # 将菜单栏添加到布局中
        self.layout().setMenuBar(self.menu_bar)

    def setup_combobox_sync(self):
        """
        设置 ComboBox 同步变化
        
        连接宽度和高度 ComboBox 的 currentIndexChanged 信号，
        实现两个ComboBox选项的同步变化
        注意：为了避免无限循环，需要使用一个标志来防止递归调用
        """
        # 标志位，用于防止ComboBox变化时的递归调用
        self._updating = False
        
        # 连接信号
        self.ui.comb_box_width.currentIndexChanged.connect(self.on_width_changed)
        self.ui.comb_box_height.currentIndexChanged.connect(self.on_height_changed)

    def on_width_changed(self, index):
        """
        当宽度 ComboBox 改变时，同步改变高度 ComboBox
        
        Args:
            index: ComboBox选中项的索引
        """
        if not self._updating:
            self._updating = True
            self.ui.comb_box_height.setCurrentIndex(index)
            self._updating = False

    def on_height_changed(self, index):
        """
        当高度 ComboBox 改变时，同步改变宽度 ComboBox
        
        Args:
            index: ComboBox选中项的索引
        """
        if not self._updating:
            self._updating = True
            self.ui.comb_box_width.setCurrentIndex(index)
            self._updating = False
        
    def send_to_main(self):
        """
        将输入的数据发送到主窗口
        
        从输入框获取名称和文本，验证后通过信号发送到主窗口
        """
        # 获取输入的名称和文本
        name = self.ui.line_name.text()
        text = self.ui.line_text.text()
        
        # 验证输入是否为空
        if not name or not text:
            QMessageBox.warning(self, 'warning', '请输入名称和文本.')
            return
            
        # 发送信号到主窗口
        self.data_added.emit(name, text)

        # 更新数据组列表
        self.application.yaml_window.update_data_group()
        
        # 关闭当前窗口
        self.close()

    def switch_page(self):
        """
        切换页面
        
        在堆叠窗口的两个页面之间进行切换
        """
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def contrast_config(self):
        """
        配置对比度指令
        
        切换到对比度配置页面，并设置相关UI元素
        """
        # 切换到第二页
        self.ui.stackedWidget.setCurrentIndex(1)

        # 显示配置区域
        self.ui.config.setVisible(True)

        self.ui.label_4.setVisible(False)
        self.ui.line_input_saturation.setVisible(False)

        self.ui.label_6.setVisible(True)
        self.ui.line_input_contrast.setVisible(True)

        self.ui.line_input_contrast.clear()
        self.ui.line_input_saturation.clear()
        
        # 设置当前指令类型为对比度
        self.now_command = '对比度'

    def saturation_config(self):
        """
        配置饱和度指令
        
        切换到饱和度配置页面，并设置相关UI元素
        """
        # 切换到第二页
        self.ui.stackedWidget.setCurrentIndex(1)
        
        self.ui.label_4.setText("饱和度")

        # 隐藏配置区域
        self.ui.config.setVisible(False)

        self.ui.label_6.setVisible(False)
        self.ui.line_input_contrast.setVisible(False)

        self.ui.label_4.setVisible(True)
        self.ui.line_input_saturation.setVisible(True)

        self.ui.line_input_contrast.clear()
        self.ui.line_input_saturation.clear()

        # 设置当前指令类型为饱和度
        self.now_command = '饱和度'

    def saturation_contrast_config(self):
        """
        配置饱和度+对比度指令
        
        切换到饱和度+对比度配置页面，并设置相关UI元素
        """
        # 切换到第二页
        self.ui.stackedWidget.setCurrentIndex(1)

        # 显示配置区域
        self.ui.config.setVisible(True)

        self.ui.label_6.setVisible(True)
        self.ui.line_input_contrast.setVisible(True)

        self.ui.label_4.setText("饱和度")
        self.ui.label_4.setVisible(True)
        self.ui.line_input_saturation.setVisible(True)

        self.ui.line_input_contrast.clear()
        self.ui.line_input_saturation.clear()
        
        # 设置当前指令类型为饱和度+对比度
        self.now_command = '饱和度+对比度'

    def natural_saturation_config(self):
        """
        配置自然饱和度指令
        
        切换到自然饱和度配置页面，并设置相关UI元素
        """
        # 切换到第二页
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # 设置标签文本为"饱和度"
        self.ui.label_4.setText("自然饱和度")
        
        # 隐藏配置区域
        self.ui.config.setVisible(False)

        self.ui.label_6.setVisible(False)
        self.ui.line_input_contrast.setVisible(False)

        self.ui.label_4.setVisible(True)
        self.ui.line_input_saturation.setVisible(True)

        self.ui.line_input_contrast.clear()
        self.ui.line_input_saturation.clear()
        
        # 设置当前指令类型为自然饱和度
        self.now_command = '自然饱和度'

    def cal_contrast(self):
        """
        计算对比度指令
        
        根据用户输入的参数计算对比度指令值，并添加到指令列表中
        """
        # 获取头字节输入
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
            
        # 获取地址输入
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return

        # 获取Lane参数
        lane = self.ui.comb_box_lane.currentText()
    
        # 获取颜色深度参数
        color_depth = self.ui.comb_box_color_depth.currentText()

        # 获取宽度参数
        width = self.ui.comb_box_width.currentText()

        # 获取高度参数
        height = self.ui.comb_box_height.currentText()
 
        # 获取对比度输入值
        input_contrast = self.ui.line_input_contrast.text()

        if not input_contrast:
            QMessageBox.warning(self, 'warning', '请输入对比度.')
            return

        # 转换对比度值为浮点数
        value_contrast = float(input_contrast)

        # 验证对比度值范围
        if not 0 <= value_contrast <= 2:
            QMessageBox.warning(self, 'warning', '对比度输入错误.')
            return
        
        # 计算对比度结果
        result_contrast = (int(width) * int(height)) / int(lane) / 64 / int(color_depth) * value_contrast

        # 限制结果在0-0xFFFF范围内
        result_contrast = max(0, min(result_contrast, 0xFFFF))

        # 转换为整数
        result_contrast_int = int(result_contrast)

        # 将指令添加到命令列表
        self.command.append(f"对比度{value_contrast}")
        self.command.append(f"{head} {ddr} {result_contrast_int:04X}")

        # 调用添加窗口函数
        self.add_window()

    def cal_saturation(self):
        """
        计算饱和度指令
        
        根据用户输入的参数计算饱和度指令值，并添加到指令列表中
        """
        # 获取头字节输入
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
            
        # 获取地址输入
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return
        
        # 获取饱和度输入值
        input_saturation = self.ui.line_input_saturation.text()

        if not input_saturation:
            QMessageBox.warning(self, 'warning', '请输入饱和度.')
            return
        
        # 转换饱和度值为浮点数
        value_saturation = float(input_saturation)

        # 验证饱和度值范围
        if not 1 <= value_saturation <= 2:
            QMessageBox.warning(self, 'warning', '饱和度输入错误.')
            return
        
        # 计算饱和度结果
        result_saturation = 64 * (value_saturation - 1)

        # 限制结果在0-0xFFFF范围内
        result_saturation = max(0, min(result_saturation, 0xFFFF))

        # 转换为整数
        result_saturation_int = int(result_saturation)

        # 将指令添加到命令列表
        self.command.append(f"饱和度{value_saturation}")
        self.command.append(f"{head} {ddr} {result_saturation_int:04X}")

        # 调用添加窗口函数
        self.add_window()

    def cal_saturation_contrast(self):
        """
        计算饱和度+对比度指令
        
        根据用户输入的参数计算饱和度+对比度指令值，并添加到指令列表中
        """
        # 获取头字节输入
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
            
        # 获取地址输入
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return
        
        # 获取Lane参数
        lane = self.ui.comb_box_lane.currentText()
    
        # 获取颜色深度参数
        color_depth = self.ui.comb_box_color_depth.currentText()

        # 获取宽度参数
        width = self.ui.comb_box_width.currentText()

        # 获取高度参数
        height = self.ui.comb_box_height.currentText()

        # 获取对比度输入值
        input_contrast = self.ui.line_input_contrast.text()

        if not input_contrast:
            QMessageBox.warning(self, 'warning', '请输入对比度.')
            return
        
        # 转换对比度值为浮点数
        value_contrast = float(input_contrast)

        # 验证对比度值范围
        if not 0 <= value_contrast <= 2:
            QMessageBox.warning(self, 'warning', '对比度输入错误.')
            return
        
        # 获取饱和度输入值
        input_saturation = self.ui.line_input_saturation.text()

        if not input_saturation:
            QMessageBox.warning(self, 'warning', '请输入饱和度.')
            return
        
        # 转换饱和度值为浮点数
        value_saturation = float(input_saturation)

        # 验证饱和度值范围
        if not 1 <= value_saturation <= 2:
            QMessageBox.warning(self, 'warning', '饱和度输入错误.')
            return
        
        # 计算对比度结果
        result_contrast = (int(width) * int(height)) / int(lane) / 64 / int(color_depth) * value_contrast

        # 限制结果在0-0xFF范围内
        result_contrast = max(0, min(result_contrast, 0xFF))

        # 转换为整数
        result_contrast_int = int(result_contrast)

        # 计算饱和度结果
        result_saturation = 64 * (value_saturation - 1)

        # 限制结果在0-0xFF范围内
        result_saturation = max(0, min(result_saturation, 0xFF))

        # 转换为整数
        result_saturation_int = int(result_saturation)

        # 将指令添加到命令列表
        self.command.append(f"饱和度{input_saturation}对比度{input_contrast}")
        self.command.append(f"{head} {ddr} {result_saturation_int:02X} {result_contrast_int:02X}")

        # 调用添加窗口函数
        self.add_window()

    def cal_natural_saturation(self):
        """
        自然饱和度配置
        
        计算并添加自然饱和度令指到指令列表
        """
        # 获取头字节输入
        head = self.ui.line_head.text()
        if not head:
            QMessageBox.warning(self, 'warning', '请输入头字节.')
            return
            
        # 获取地址输入
        ddr = self.ui.line_ddr.text()
        if not ddr:
            QMessageBox.warning(self, 'warning', '请输入地址.')
            return
        
        # 获取饱和度输入值
        input_natural_saturation = self.ui.line_input_saturation.text()

        if not input_natural_saturation:
            QMessageBox.warning(self, 'warning', '请输入自然饱和度.')
            return
        
        # 转换饱和度值为浮点数
        value_natural_saturation = float(input_natural_saturation)

        # 验证饱和度值范围
        if not 0 <= value_natural_saturation <= 2:
            QMessageBox.warning(self, 'warning', '自然饱和度输入错误.')
            return
        
        result_natural_saturation = 100 * (value_natural_saturation - 1)

        # 限制结果在0-0xFFFF范围内
        result_natural_saturation = max(-100, min(result_natural_saturation, 100))

         # 转换为16位有符号整数，然后转换为无符号表示用于显示
        if result_natural_saturation < 0:
            # 负数转换为补码形式 (16位)
            result_natural_saturation_int = int(result_natural_saturation) & 0x00FF
        else:
            # 正数直接转换
            result_natural_saturation_int = int(result_natural_saturation)

        # 将指令添加到命令列表
        self.command.append(f"自然饱和度{value_natural_saturation}")
        self.command.append(f"{head} {ddr} {result_natural_saturation_int:04X}")

        # 调用添加窗口函数
        self.add_window()

    def add_window(self):
        """
        添加窗口
        
        发送指令信号到主窗口，并清空指令列表
        """
        # 发送信号到主窗口
        self.data_added.emit(self.command[0], self.command[1])

        # 更新数据组列表
        self.application.yaml_window.update_data_group()
        
        # 清空指令列表
        self.command.clear()

    def cal_command(self):
        """
        计算指令
        
        根据当前指令类型调用相应的计算函数
        """
        if self.now_command == '对比度':
            self.cal_contrast()
        elif self.now_command == '饱和度':
            self.cal_saturation()
        elif self.now_command == '饱和度+对比度':
            self.cal_saturation_contrast()
        elif self.now_command == '自然饱和度':
            self.cal_natural_saturation()
