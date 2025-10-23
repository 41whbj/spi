#!/usr/bin/env python3.13
"""
filename: sub_add_data.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-21
description: SPI数据添加子窗口，处理SPI数据的输入和配置
"""

import re
from PySide6.QtWidgets import QMessageBox, QTabWidget
from PySide6.QtWidgets import QWidget, QMenuBar, QMenu, QStatusBar
from PySide6.QtCore import Signal, QTimer
from core.ui.Ui_sub_add_data import Ui_SubForm_Data
from PySide6.QtGui import QAction
from core.sub_window.formula_parser import FormulaParser

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

        self.yaml_window = application.yaml_window

        self.yaml_path = None
        
        # 设置窗口标题
        self.setWindowTitle('SPI 数据窗口')
        
        # 设置文本输入框的占位符提示
        self.ui.line_text.setPlaceholderText("e.g., 00 00 00")
        
        # 当前指令类型标识
        self.now_command = None

        # 设置ComboBox同步变化
        self.setup_combobox_sync()
        
        # 创建菜单栏
        self.create_tab_widget()
        
        # 存储指令数据的列表
        self.command = []

        # 创建状态栏并添加到第二页底部
        self.create_status_bar()

        self.connect_yaml_signals()
        
        # 使用QTimer定期检查YAML文件是否已导入
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_yaml_import_status)
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次

        self.setup_connections()

    # ==================== 信号连接功能 ====================

    def setup_connections(self):
        """
        设置UI组件的信号与槽函数连接
        """
        # 连接按钮信号与槽函数
        self.ui.button_data_confirm.clicked.connect(self.send_to_main)
        self.ui.button_data_cancel.clicked.connect(self.close)
        self.ui.pushButton_add_data.clicked.connect(self.cal_formula_command)
        self.ui.pushButton_add_data_.clicked.connect(self.add_saturation_contrast)

    # ==================== YAML文件处理功能 ====================

    def check_yaml_import_status(self):
        """
        定期检查YAML文件导入状态并更新界面
        """
        # 检查是否有导入的YAML文件路径
        if self.yaml_window.file_path:
            # 如果已经有导入的文件路径但状态栏未更新，则更新状态栏
            if self.yaml_path != self.yaml_window.file_path:
                self.yaml_path = self.yaml_window.file_path
                self.status_bar.showMessage(f"已导入yaml文件: {self.yaml_path}", 0)
                
                # 更新comboBox_address
                self.update_combo_box_address(self.yaml_path)
        else:
            # 如果没有导入的文件，保持就绪状态
            if self.status_bar.currentMessage() == "":
                self.status_bar.showMessage("未导入文件", 0)

    def connect_yaml_signals(self):
            """
            连接YAML窗口的信号到状态栏更新函数
            """
            # 连接导入信号到状态栏更新函数
            self.yaml_window.import_signal.connect(self.update_status_bar_on_import)
            # 连接导入信号到comboBox_address更新函数
            self.yaml_window.import_signal.connect(self.update_combo_box_address)
            # print("连接YAML信号")

    def update_combo_box_address(self, file_path):
        """
        当YAML文件导入时更新comboBox_address
        
        Args:
            file_path: 导入的文件路径
        """
        # print(f"update_combo_box_address被调用，文件路径: {file_path}")
        
        # 从function_config_window_instance获取配置数据
        # try:
        # 获取功能配置数据
        function_config_data = self.application.sub_window.function_config_window_instance.get_configs()
        
        # print(f"从function_config获取的数据: {function_config_data}")
        
        # 检查数据是否为空
        if not function_config_data:
            # print("功能配置数据为空")
            return
        
        # # 断开之前的连接以避免重复连接
        # try:
        #     self.ui.comboBox_address.currentIndexChanged.disconnect(self.display_function_for_address)
        #     print("已断开之前的信号连接")
        # except TypeError:
        #     # 如果之前没有连接，则忽略错误
        #     print("之前没有信号连接")
        #     pass
        
        # 使用blockSignals临时阻止信号发射
        self.ui.comboBox_address.blockSignals(True)
        # print("阻塞信号")
        
        # 清空comboBox_address的现有项
        # print("清空comboBox_address的现有项")
        self.ui.comboBox_address.clear()

        # 从function_config中提取地址并添加到comboBox_address
        for i, item in enumerate(function_config_data):
            address = item.get('address')
            function = item.get('function', '')
            var_name = item.get('var_name', '')
            formula = item.get('formula', '')
            range_val = item.get('range_val', '')
 
            var_name = self.clean_var_name(var_name)
            
            # print(f"处理第{i}项 - 地址: {address}, 功能: {function}, 公式: {formula}")
            
            if address:
                # 存储一个元组作为itemData
                data_tuple = (function, formula, var_name, range_val)
                self.ui.comboBox_address.addItem(address, data_tuple)
                # print(f"添加地址项: {address}, 关联数据: {data_tuple}")
        
        # 恢复信号发射
        self.ui.comboBox_address.blockSignals(False)
        # print("恢复信号")

        # 重新连接信号
        self.ui.comboBox_address.currentIndexChanged.connect(self.display_function_for_address)
        # print("重新连接信号")
        
        # print(f"comboBox_address总项数: {self.ui.comboBox_address.count()}")

        count = self.ui.comboBox_address.count()
        # print(f"comboBox_address总项数: {count}")
        
        # 主动触发一次索引改变来显示第一个地址对应的功能
        if self.ui.comboBox_address.count() > 1:  # 有实际地址项
            # print("设置索引为1，显示第一个实际地址项")
            self.ui.comboBox_address.setCurrentIndex(count - 1)  # 选择最后一个地址项


        # print(f"已更新comboBox_address，共添加{len(function_config_data)}个地址项")
        # except Exception as e:
        #     print(f"更新comboBox_address时出错: {e}")
        #     import traceback
        #     traceback.print_exc()

    def display_function_for_address(self, index):
        """
        根据comboBox_address的选择显示对应的功能和公式
        
        Args:
            index: comboBox_address的当前索引
        """
        # print(f"display_function_for_address被调用，索引: {index}")
        
        # 检查索引是否有效
        if index < 0:
            # print("索引无效，清空显示")
            self.ui.lineEdit_function.clear()
            self.ui.textEdit_formula.clear()
            return
            
        # 获取选中项关联的功能数据和公式
        data = self.ui.comboBox_address.itemData(index)
        
        function, formula, var_name ,range_val = data
        # print(f"解包数据成功 - 功能: {function}, 公式: {formula}, 变量名: {var_name}")

        # 显示功能数据
        if function:
            # print(f"设置lineEdit_function文本: {function}")
            self.ui.lineEdit_function.setText(function)
        else:
            # print("清空lineEdit_function")
            self.ui.lineEdit_function.clear()

        # 显示公式数据
        if formula:
            # print(f"设置textEdit_formula文本: {formula}")
            self.ui.textEdit_formula.setText(formula)
        else:
            # print("清空textEdit_formula")
            self.ui.textEdit_formula.clear()

        self.ui.lineEdit_input.setPlaceholderText(f"输入范围: {range_val}")

    def update_status_bar_on_import(self, file_path):
        """
        当YAML文件导入时更新状态栏
        
        Args:
            file_path: 导入的文件路径
        """
        # 更新状态栏显示导入成功的消息
        self.status_bar.showMessage(f"已导入项目: {file_path}", 0)
        self.yaml_path = file_path

    # ==================== 界面组件功能 ====================

    def create_status_bar(self):
        """
        创建状态栏并添加到第二页底部
        """
        # 创建状态栏
        self.status_bar = QStatusBar(self)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                border-top: 1px solid #d0d0d0;
                font-size: 10px;
                padding: 2px;
            }
        """)
        
        # 将状态栏添加到布局中
        self.ui.page_formula.layout().addWidget(self.status_bar)
        
        # 设置初始状态消息
        self.status_bar.showMessage("无yaml导入", 0)  # 0表示永久显示

    def clean_var_name(self, var_name):
        """
        清理var_name字段，移除其中包含的额外参数
        
        Args:
            var_name (str): 原始变量名称
            
        Returns:
            str: 清理后的变量名称
        """

        # 定义需要移除的额外参数列表
        extra_params = ["通道", "色深", "水平分辨率", "垂直分辨率"]
        
        # 移除这些额外参数
        cleaned_var_name = var_name
        for param in extra_params:
            cleaned_var_name = cleaned_var_name.replace(param, "")
        
        # 移除多余的逗号和空格
        # 处理类似 "对比度,,通道" 的情况
        cleaned_var_name = re.sub(r',+', ',', cleaned_var_name)  # 将多个连续逗号替换为单个逗号
        cleaned_var_name = re.sub(r'^,+|,+$', '', cleaned_var_name)  # 移除开头和结尾的逗号
        cleaned_var_name = cleaned_var_name.strip()  # 移除首尾空格
        
        return cleaned_var_name

    def create_tab_widget(self):
        """
        创建选项卡控件
        
        创建包含页面控制和快速指令功能的选项卡控件，
        用于方便用户切换界面和快速生成常用指令
        """
        # 创建标签页控件
        self.tab_widget = QTabWidget(self)

        # 设置标签页样式
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background-color: #f0f0f0;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #d0d0d0;
                border-bottom-color: #d0d0d0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 12px;
                margin: 0px 2px;
                font-size: 12px;
            }
            
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom-color: #ffffff;
            }
            
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
        """)

                # 添加一般页面标签
        self.tab_widget.addTab(self.ui.page_normal, "一般指令")
        
        # 添加快速指令标签
        self.tab_widget.addTab(self.ui.page_formula, "快速指令")
        
        # 添加饱和度+对比度指令标签
        self.tab_widget.addTab(self.ui.page_old, "饱和度+对比度指令")
        
        # 将菜单栏添加到布局中
        self.layout().addWidget(self.tab_widget)

    # ==================== 数据处理功能 ====================

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

    # ==================== 指令计算功能 ====================

    def cal_formula_command(self):
        """
        通过formula计算指令
        
        根据当前选中的地址和输入的值，使用formula计算数据
        """

        #获取帧头
        head = self.ui.lineEdit_head.text()

        # 获取当前选中的地址
        current_index = self.ui.comboBox_address.currentIndex()
        address = self.ui.comboBox_address.currentText()    

        # 获取选中项关联的数据
        data = self.ui.comboBox_address.itemData(current_index)
        if not data:
            QMessageBox.warning(self, 'warning', '未找到对应的功能配置.')
            return

        function, formula, var_name, range_val = data

        # 获取输入值
        input_value_text = self.ui.lineEdit_input.text()
        if not input_value_text:
            QMessageBox.warning(self, 'warning', f'请输入{var_name}的值.')
            return

        # 获取function_config_window_instance以获取范围和符号位设置
        try:
            function_config_data = self.application.sub_window.function_config_window_instance.get_configs()
            selected_config = None
            for config in function_config_data:
                if config.get('address') == address:
                    selected_config = config
                    break

            if not selected_config:
                QMessageBox.warning(self, 'warning', f'未找到地址 {address} 的配置信息.')
                return

            # 获取范围设置
            if range_val:
                # 解析范围值，例如 '[2,4]' 格式
                try:
                    range_val = range_val.strip('[]')
                    range_parts = range_val.split(',')
                    if len(range_parts) == 2:
                        min_val = float(range_parts[0].strip())
                        max_val = float(range_parts[1].strip())
                        
                        input_value = float(input_value_text)
                        if input_value < min_val or input_value > max_val:
                            QMessageBox.warning(self, 'warning', f'输入值 {input_value} 不在范围 [{min_val}, {max_val}] 内.')
                            return
                    else:
                        input_value = float(input_value_text)
                except ValueError:
                    QMessageBox.warning(self, 'warning', '范围值格式错误或输入值不是有效数字.')
                    return
            else:
                input_value = float(input_value_text)

            # 获取符号位设置
            sign_enabled = selected_config.get('sign', '否') == '是'

            # 获取多变量设置
            multi_var = selected_config.get('multi_var', '否')

            parser = FormulaParser()
            formula_variables = parser.extract_variables(formula)

            # 根据公式中的变量构建变量字典
            var_dict = {}

            if var_name and len(var_name) > 0:
                # 如果var_name中定义了变量，将输入值分配给第一个变量
                var_dict[var_name] = input_value

            if multi_var == '是':
                # 为公式中其他变量分配界面控件的值
                for formula_var in formula_variables:
                    if formula_var not in var_dict:  # 只处理不在var_dict中的变量
                        if formula_var == "通道":
                            var_dict[formula_var] = int(self.ui.comb_box_lane.currentText())
                        elif formula_var == "色深":
                            var_dict[formula_var] = int(self.ui.comb_box_color_depth.currentText())
                        elif formula_var == "水平分辨率":
                            var_dict[formula_var] = int(self.ui.comb_box_width.currentText())
                        elif formula_var == "垂直分辨率":
                            var_dict[formula_var] = int(self.ui.comb_box_height.currentText())
            else:
                pass

            print(var_dict)

            # 计算公式结果
            result = FormulaParser.calculate_formula_result(formula, var_dict)

            # 将结果限制在0-0xFFFF范围内
            result = max(0, min(result, 0xFFFF))

            # 使用16位转换（4位十六进制）
            hex_result = FormulaParser.calculate_and_format_result(formula, var_dict, sign_enabled, 16)

            # 将指令添加到命令列表
            # 数据名称是function和输入值的拼接

            if input_value_text == "0":
                command_name = f"{function}关闭"
            else:
                command_name = f"{function}{input_value_text}"

            self.command.append(command_name)
            self.command.append(f"{head} {address} {hex_result}")

            # print(self.command)

            # 调用添加窗口函数
            self.add_window()

            self.command.clear()

        except Exception as e:
            QMessageBox.warning(self, 'warning', f'计算公式时出错: {str(e)}')
            return

    # ==================== 数据发送功能 ====================

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

    def add_window(self):
        """
        添加窗口
        
        发送指令信号到主窗口，并清空指令列表
        """
        # 发送信号到主窗口
        self.data_added.emit(self.command[0], self.command[1])

        # 更新数据组列表
        self.application.yaml_window.update_data_group()

    def add_saturation_contrast(self):
        """
        计算饱和度+对比度指令
        """
        # 获取帧头
        head = self.ui.lineEdit_head.text()

        # 获取饱和度地址
        saturation_address = self.ui.lineEdit_address_saturation.text()
        if not saturation_address:
            QMessageBox.warning(self, 'warning', '请输入饱和度地址.')
            return

        # 获取对比度地址
        contrast_address = self.ui.lineEdit_address_contrast.text()
        if not contrast_address:
            QMessageBox.warning(self, 'warning', '请输入对比度地址.')
            return

        # 获取饱和度值
        value_saturation_text = self.ui.lineEdit_value_saturation.text()
        if not value_saturation_text:
            QMessageBox.warning(self, 'warning', '请输入饱和度值.')
            return

        # 获取对比度值
        value_contrast_text = self.ui.lineEdit_value_contrast.text()
        if not value_contrast_text:
            QMessageBox.warning(self, 'warning', '请输入对比度值.')
            return

        try:
            value_saturation = float(value_saturation_text)
            value_contrast = float(value_contrast_text)
        except ValueError:
            QMessageBox.warning(self, 'warning', '输入的值不是有效数字.')
            return

        # 将值限制在0-0xFFFF范围内
        value_saturation = max(0, min(value_saturation, 0xFFFF))
        value_contrast = max(0, min(value_contrast, 0xFFFF))

        # 转换为4位十六进制
        hex_saturation = f"{int(value_saturation):04X}"
        hex_contrast = f"{int(value_contrast):04X}"

        # 将指令添加到命令列表
        self.command.append(f"饱和度{value_saturation}对比度{value_contrast}")
        self.command.append(f"{head} {saturation_address} {hex_saturation}")
        self.command.append(f"{head} {contrast_address} {hex_contrast}")

        # 调用添加窗口函数
        self.add_window()

        self.command.clear()