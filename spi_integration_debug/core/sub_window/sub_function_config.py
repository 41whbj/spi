#!/usr/bin/env python3.13
"""
filename: sub_function_config.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-23
description: 函数配置子窗口，处理函数相关的配置和设置
"""

import re
from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtWidgets import (
    QMessageBox, QTreeWidgetItem, QStyledItemDelegate, QMenu
)
from PySide6.QtGui import QAction

from core.ui.Ui_sub_function_config import Ui_Form

# 只读代理类
class ReadOnlyDelegate(QStyledItemDelegate):
    """
    只读代理类，用于使特定列不可编辑
    """
    def createEditor(self, parent, option, index):
        """
        重写createEditor方法，返回None表示不创建编辑器
        """
        return None

# 编辑代理类
class EditingDelegate(QStyledItemDelegate):
    """
    编辑代理类，用于处理树形控件的编辑完成信号
    """
    editingFinished = Signal(object, int, str)  # 发送项对象、列号和原始值
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_item = None
        self.current_column = None
        self.original_value = None
        
    def createEditor(self, parent, option, index):
        """
        创建编辑器
        """
        editor = QLineEdit(parent)
        self.current_item = self.parent().itemFromIndex(index)
        self.current_column = index.column()
        
        # 保存原始值
        if self.current_item:
            self.original_value = self.current_item.text(self.current_column)

            editor.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #0078D7;
                selection-background-color: #0078D7;
                selection-color: white;
            }
        """)
        
        # 连接编辑完成信号
        editor.editingFinished.connect(self.on_editing_finished)
        return editor
        
    def on_editing_finished(self):
        """
        处理编辑完成事件
        """
        if self.current_item and hasattr(self, 'current_column') and hasattr(self, 'original_value'):
            # 获取编辑器
            editor = self.sender()
            if editor:
                # 发出编辑完成信号，包含原始值
                self.editingFinished.emit(self.current_item, self.current_column, self.original_value)
            
    def setModelData(self, editor, model, index):
        """
        将编辑器数据保存到模型
        """
        model.setData(index, editor.text(), Qt.EditRole)

class SubWindowFunctionConfig(QWidget):
    """
    函数配置子窗口类，负责处理函数相关的配置和设置
    """
    # function_config_updated = Signal(dict)

    def __init__(self, application):
        """
        初始化函数配置子窗口类
        """
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.application = application
        self.yaml = application.yaml_window

        # 创建编辑委托实例
        self.editing_delegate = EditingDelegate(self.ui.tree_config)
        self.editing_delegate.editingFinished.connect(self.editing_finished)

        self.show_widget = False
        self.ui.formula_widget.setVisible(False)

        # 启用右键菜单
        self.ui.tree_config.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tree_config.customContextMenuRequested.connect(self.show_context_menu)

        self.widget_init()
        self.setup_connections()

        self.multi_var = False

    #===============================================================================
    # 初始化UI组件，建立信号槽连接
    #===============================================================================

    def widget_init(self):
        """
        初始化子窗口的UI组件
        """
        self.ui.tree_config.clear()
        self.ui.tree_config.setHeaderLabels([
            "地址", 
            "算法功能", 
            "记录状态", 
            "参数名称", 
            "多参数状态", 
            "计算公式", 
            "输入值范围", 
            "符号位开启"]
        )

        # 添加委托事件
        self.ui.tree_config.setItemDelegateForColumn(0, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(1, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(2, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(3, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(4, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(5, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(6, self.editing_delegate)
        self.ui.tree_config.setItemDelegateForColumn(7, self.editing_delegate)

        self.ui.combo_box_var.addItems([
            "通道", 
            "色深", 
            "水平分辨率", 
            "垂直分辨率", 
        ])

        self.ui.combo_box_var.activated.connect(self.combo_box_var_activated)

    def combo_box_var_activated(self, index):
        """
        处理变量组合框的激活事件
        """
        text = self.ui.combo_box_var.currentText()

        self.ui.line_formula_input.insert(text)
        
    def setup_connections(self):
        """
        设置应用程序的信号与槽函数连接
        """
        self.ui.button_config.clicked.connect(self.update_config)
        self.ui.check_box_formula.stateChanged.connect(self.toggle_formula_widget_state)

        self.ui.check_box_var_mode.stateChanged.connect(self.toggle_multi_var)

        self.ui.label_6.setVisible(False)
        self.ui.combo_box_var.setVisible(False)

    def toggle_multi_var(self):
        """
        切换多变量模式
        """
        
        self.multi_var = not self.multi_var
        if self.ui.check_box_var_mode.isChecked():
            self.ui.label_6.setVisible(True)
            self.ui.combo_box_var.setVisible(True)
        else:
            self.ui.label_6.setVisible(False)
            self.ui.combo_box_var.setVisible(False)

    #===============================================================================
    # 右键菜单功能
    #===============================================================================
    def show_context_menu(self, position):
        """
        显示右键菜单
        """
        # 获取点击的项
        item = self.ui.tree_config.itemAt(position)
        if item is None:
            return

        # 创建菜单
        menu = self.create_context_menu()
        # 在鼠标位置显示菜单
        menu.exec(self.ui.tree_config.viewport().mapToGlobal(position))

    def create_context_menu(self):
        """
        创建右键菜单
        """
        menu = QMenu(self)
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self.delete_selected_item)
        menu.addAction(delete_action)
        return menu

    def delete_selected_item(self):
        """
        删除选中的项
        """
        # 获取当前选中的项
        currentItem = self.ui.tree_config.currentItem()
        if currentItem is None:
            QMessageBox.information(self, "提示", "请先选择要删除的项")
            return

        # 确认删除
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            "确定要删除选中的项吗？", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 获取项的索引并删除
            index = self.ui.tree_config.indexOfTopLevelItem(currentItem)
            if index >= 0:
                self.ui.tree_config.takeTopLevelItem(index)
                # 更新YAML配置
                self.yaml.update_function_config()

    #===============================================================================
    # 更新配置功能
    #===============================================================================

    def update_config(self):
        """
        通过按钮添加配置项
        """
        # 获取输入值
        addr = self.ui.line_addr_input.text().strip()
        func = self.ui.line_function_input.text().strip()
        record = self.ui.check_box_record.isChecked()
        var_name = self.ui.line_var_input.text().strip()
        multi_var = self.ui.check_box_var_mode.isChecked()
        formula = self.ui.line_formula_input.text().strip()
        range_val = self.ui.line_range_val_input.text().strip()
        sign_state = self.ui.check_box_sign.isChecked()

        # 验证并处理输入值
        validation_result = self.check_and_process_inputs(
            addr, 
            func, 
            record, 
            var_name, 
            multi_var, 
            formula, 
            range_val, 
            sign_state
        )
        
        if not validation_result["is_valid"]:
            QMessageBox.warning(self, "警告", validation_result["error_message"])
            return
        
        # 使用处理后的值
        addr = validation_result["addr"]
        func = validation_result["func"]
        record = validation_result["record"]
        var_name = validation_result["var_name"]
        multi_var = validation_result["multi_var"]
        formula = validation_result["formula"]
        range_val = validation_result["range_val"]
        sign_state = validation_result["sign_state"]

        # 创建新的树节点
        item = QTreeWidgetItem(self.ui.tree_config)
        item.setText(0, addr)
        item.setText(1, func)
        item.setText(2, record)
        item.setText(3, var_name)  
        item.setText(4, multi_var)  
        item.setText(5, formula)
        item.setText(6, range_val)
        item.setText(7, sign_state)

        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)  # 默认允许编辑

        # 设置item的高度和字体
        font = item.font(0)  # 获取第一列的字体
        font.setPointSize(10)  # 设置字体大小
        item.setFont(0, font)  # 应用到所有列
        item.setFont(1, font)
        item.setFont(2, font)
        item.setFont(3, font)
        item.setFont(4, font)
        item.setFont(5, font)
        item.setFont(6, font)
        item.setFont(7, font)

        item.setSizeHint(0, QSize(0, 30))  # 设置高度为25像素

        # 清空输入框
        self._clear_input_fields()

        # 更新YAML配置
        self.yaml.update_function_config()
        
    def _clear_input_fields(self):
        """
        清空输入框
        """
        self.ui.line_addr_input.clear()
        self.ui.line_function_input.clear()
        self.ui.line_var_input.clear()
        self.ui.check_box_var_mode.setChecked(False)
        self.ui.line_formula_input.clear()
        self.ui.line_range_val_input.clear()
        self.ui.check_box_sign.setChecked(False)

    #===============================================================================
    # 检查并处理输入值
    #===============================================================================

    def check_and_process_inputs(self, addr, func, record, var_name, multi_var, formula, range_val, sign_state):
        """
        验证并处理所有输入值
        
        Returns:
            dict: 包含验证结果和处理后值的字典
        """
        result = {
            "is_valid": True,
            "error_message": "",
            "addr": "",
            "func": "",
            "record": "",
            "var_name": "",
            "multi_var": "",
            "formula": "",
            "range_val": "",
            "sign_state": ""
        }

        # 验证地址
        addr_validation = self.check_address(addr)
        if not addr_validation["is_valid"]:
            result["is_valid"] = False
            result["error_message"] = addr_validation["error_message"]
            return result

        result["addr"] = addr_validation["value"]

        # 验证算法功能
        func_validation = self.check_function(func)
        if not func_validation["is_valid"]:
            result["is_valid"] = False
            result["error_message"] = func_validation["error_message"]
            return result
        result["func"] = func_validation["value"]

        # 处理记录状态
        result["record"] = "是" if record else "否"

        # 处理多变量开启状态
        result["multi_var"] = "是" if multi_var else "否"

        # 处理变量名称
        var_name_validation = self.check_var_name(var_name)
        if not var_name_validation["is_valid"]:
            result["is_valid"] = False
            result["error_message"] = var_name_validation["error_message"]
            return result
        result["var_name"] = var_name_validation["value"]

        # 处理计算公式
        formula_validation = self.check_formula(formula, result["var_name"], result["multi_var"])
        if not formula_validation["is_valid"]:
            result["is_valid"] = False
            result["error_message"] = formula_validation["error_message"]
            return result
        result["formula"] = formula_validation["value"]

        # 处理输入值范围
        range_validation = self.check_range(range_val)
        if not range_validation["is_valid"]:
            result["is_valid"] = False
            result["error_message"] = range_validation["error_message"]
            return result
        result["range_val"] = range_validation["value"]

        # 处理符号位开启状态
        result["sign_state"] = "是" if sign_state else "否"

        return result

    #===============================================================================
    # 地址验证功能
    #===============================================================================

    def check_address(self, addr):
        """
        验证地址输入
        
        Args:
            addr (str): 地址输入
            
        Returns:
            dict: 验证结果字典
        """
        result = {"is_valid": True, "error_message": "", "value": ""}
        
        if not addr:
            result["is_valid"] = False
            result["error_message"] = "请输入地址！"
            return result
                
        # 验证地址格式（00-FF）
        formatted_addr = self.is_addr_valid(addr)
        if formatted_addr is False:
            result["is_valid"] = False
            result["error_message"] = "请输入正确的地址格式！"
            return result
        
        # 检查地址是否已存在
        if not self.is_addr_exist(addr):
            result["is_valid"] = False
            result["error_message"] = "该地址已存在！"
            return result
        
        result["value"] = formatted_addr
        return result

    def is_addr_valid(self, addr: str) -> bool:
        """
        验证地址是否符合格式（00-FF）, 并返回格式化后的地址
        """
        # 检查长度是否为1或2个字符
        if len(addr) == 0 or len(addr) > 2:
            return False
        
        addr = addr.strip()

        for char in addr:
            if char not in '0123456789ABCDEFabcdef':
                return False
        
        addr = addr.upper()

        # 补齐为两位
        if len(addr) == 1:
            addr = '0' + addr

        return addr

    def is_addr_exist(self, addr: str) -> bool:
        """
        检查地址是否已存在于配置中
        """
        addr = addr.upper()
        if len(addr) == 1:
            addr = '0' + addr
            
        for i in range(self.ui.tree_config.topLevelItemCount()):
            item = self.ui.tree_config.topLevelItem(i)
            item_addr = item.text(0).upper()
            if len(item_addr) == 1:
                item_addr = '0' + item_addr
            if item_addr == addr:
                return False
        return True

    #===============================================================================
    # 算法功能验证功能
    #===============================================================================

    def check_function(self, func):
        """
        验证算法功能输入
        
        Args:
            func (str): 算法功能输入
            
        Returns:
            dict: 验证结果字典
        """
        result = {"is_valid": True, "error_message": "", "value": ""}
        
        if not func:
            result["is_valid"] = False
            result["error_message"] = "请输入算法功能！"
            return result
        
        # 检查算法功能是否已存在
        if not self.is_function_exist(func):
            result["is_valid"] = False
            result["error_message"] = "该算法功能已分配给对应的地址！"
            return result
        
        result["value"] = func
        return result

    def is_function_exist(self, func: str) -> bool:
        """
        检查算法功能是否已存在于配置中
        """
        for i in range(self.ui.tree_config.topLevelItemCount()):
            item = self.ui.tree_config.topLevelItem(i)
            item_func = item.text(1).upper()
            if item_func == func:
                return False
        return True

    #===============================================================================
    # 变量名称验证功能
    #===============================================================================

    def check_var_name(self, var_name):
        """
        验证变量名称输入
        
        Args:
            var_name (str): 变量名称输入
        Returns:
            dict: 验证结果字典
        """
        result = {"is_valid": True, "error_message": "", "value": ""}
        
        # 处理中文字符
        processed_var_name = self.process_chinese_characters(var_name)
        
        # 如果没有输入变量名称，默认使用"无"
        if processed_var_name == "":
            result["value"] = "无"
            return result
        
                # 检查变量名是否只包含数字、字母、汉字和下划线
        if not re.match(r'^[\w\u4e00-\u9fff]+$', processed_var_name):
            # 找出非法字符
            invalid_chars = re.findall(r'[^\w\u4e00-\u9fff]', processed_var_name)
            invalid_chars = list(set(invalid_chars))  # 去重
            result["is_valid"] = False
            result["error_message"] = f"变量名包含非法字符: {', '.join(invalid_chars)}。变量名只能包含数字、字母、汉字和下划线。"
            return result
        
        result["value"] = processed_var_name
            
        return result

    #===============================================================================
    # 计算公式验证功能
    #===============================================================================

    def check_formula(self, formula, var_name="", multi_var="否"):
        """
        验证计算公式输入
        
        Args:
            formula (str): 计算公式输入
            var_name (str): 变量名称
            multi_var (str): 多变量开启状态 ('是' 或 '否')
            
        Returns:
            dict: 验证结果字典
        """
        result = {"is_valid": True, "error_message": "", "value": ""}
        
        # 如果没有输入公式，默认使用"无"
        if formula == "":
            result["value"] = "无"
            return result
        
        # 处理中文字符
        processed_formula = self.process_chinese_characters(formula)
        
        # 检查公式完整性
        if not self.check_formula_completeness(processed_formula):
            result["is_valid"] = False
            result["error_message"] = "公式不完整！"
            return result

        # 检查语法
        syntax_valid, error_msg = self.check_syntax(processed_formula)
        if not syntax_valid:
            result["is_valid"] = False
            result["error_message"] = f"公式语法错误：{error_msg}"
            return result
        
        # 提取公式中的所有变量名
        variables_in_formula = self.extract_variables_from_formula(processed_formula)
        
        # 如果开启了多变量模式，检查公式中的变量是否合法
        if multi_var == "是":
            
            print(f"提取到的变量名: {variables_in_formula}")

            # 定义允许的额外参数
            allowed_extra_params = ["通道", "色深", "水平分辨率", "垂直分辨率"]
            
            # 检查公式中的变量是否都在允许范围内
            invalid_vars = []
            for var in variables_in_formula:
                # 如果变量不是var_name，也不是额外参数，则为非法变量
                if var != var_name and var not in allowed_extra_params:
                    invalid_vars.append(var)
            
            if invalid_vars:
                result["is_valid"] = False
                result["error_message"] = f"公式中包含非法变量: {', '.join(invalid_vars)}。在多变量模式下，公式中只能包含变量名 '{var_name}' 和额外参数({', '.join(allowed_extra_params)})。"
                return result
        else:
            # 单变量模式：只允许 var_name
            invalid_vars = []
            for var in variables_in_formula:
                if var != var_name:
                    invalid_vars.append(var)
            
            if invalid_vars:
                result["is_valid"] = False
                result["error_message"] = f"公式中包含非法变量: {', '.join(invalid_vars)}。在单变量模式下，公式中只能包含变量名 '{var_name}'。"
                return result
            
        result["value"] = processed_formula
            
        result["value"] = processed_formula
        return result
    
    def check_formula_completeness(self, formula):
        """
        检查公式完整性，包括括号匹配和基本语法检查
        
        Args:
            formula (str): 公式字符串
            
        Returns:
            bool: 公式是否完整
        """

        # 检查括号匹配
        stack = []
        for char in formula:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False  # 发现未匹配的右括号
                stack.pop()
        
        # 检查是否有未闭合的左括号
        if stack:
            return False
        
        # 检查是否以运算符结尾
        if re.search(r'[\+\-\*/]$', formula.strip()):
            return False
        
        # 检查是否以运算符开头（除了负号）
        if re.search(r'^[\+\*/]', formula.strip()):
            return False
        
        # 检查连续的运算符
        if re.search(r'[\+\-\*/]{2,}', formula):
            return False
        
        # 检查空括号
        if re.search(r'\(\s*\)', formula):
            return False
        
        # 检查括号内只有运算符
        if re.search(r'\([\+\-\*/\s]*\)', formula):
            return False
        
        return True

    def check_syntax(self, formula):
        """
        验证公式语法的基本正确性
        
        Args:
            formula (str): 公式字符串
            
        Returns:
            tuple: (is_valid, error_message) 是否有效和错误信息
        """
        
        # 检查非法字符（只允许数字、字母、下划线、运算符、括号、点号和空格）
        if not re.match(r'^[a-zA-Z0-9_\+\-\*/\(\)\.\s\u4e00-\u9fff]+$', formula):
            return False, "公式包含非法字符"
        
        return True, ""
    
    def extract_variables_from_formula(self, formula):
        """
        从公式中提取所有变量名
        
        Args:
            formula (str): 公式字符串
            
        Returns:
            list: 变量名列表
        """
        # 使用正则表达式提取所有变量名（字母、数字、下划线、汉字的组合）
        # 匹配由字母、数字、下划线、汉字组成的标识符
        pattern = r'[\w\u4e00-\u9fff]+'
        variables = re.findall(pattern, formula)
        
        # 过滤掉纯数字（常数）和运算符相关的字符
        filtered_vars = []
        for var in variables:
            # 跳过纯数字（包括小数）
            if re.match(r'^\d+\.?\d*$', var):
                continue
            # 跳过单独的运算符片段（如可能匹配到的+、-、*、/等）
            if var in ['+', '-', '*', '/', '(', ')', '.']:
                continue
            # 如果变量不在已有的列表中，则添加
            if var not in filtered_vars:
                filtered_vars.append(var)
        
        return filtered_vars

    #===============================================================================
    # 输入值范围验证功能
    #===============================================================================

    def check_range(self, range_val):
        """
        验证输入值范围
        
        Args:
            range_val (str): 输入值范围
            
        Returns:
            dict: 验证结果字典
        """
        result = {"is_valid": True, "error_message": "", "value": ""}
        
        # 如果没有输入范围，默认使用"无"
        if range_val == "" or range_val == "无":
            result["value"] = "无"
            return result

        # 验证输入范围格式
        is_valid = self.check_input_range(range_val)
        if is_valid is False:
            result["is_valid"] = False
            result["error_message"] = "输入范围格式错误,请输入如 [1,2]"
            return result
        range_val = self.process_chinese_characters(range_val)

        result["value"] = range_val
        return result
    
    def check_input_range(self, input_range):
        """
        验证输入值范围格式，只接受闭区间格式如 [1,2]，返回是否正确和最小值最大值
        
        Args:
            input_range (str): 输入值范围字符串
            
        Returns:
            bool: 格式是否正确
            tuple: min_value, max_value 或 "","" 如果格式不正确
        """
        if not input_range:
            return True  # 空范围认为是有效的
        
        # 首先处理中文字符
        processed_range = self.process_chinese_characters(input_range)
        
        # 只匹配闭区间格式 [数字,数字]，支持负数和小数
        pattern = r'^\[\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*\]$'
        
        match = re.match(pattern, processed_range)
        if not match:
            return False
        
        # 提取最小值和最大值
        min_val = float(match.group(1))
        max_val = float(match.group(3))
        
        # 检查最小值是否小于等于最大值
        if min_val > max_val:
            return False, "", ""
        
        return True, min_val, max_val

    #===============================================================================
    # 编辑完成处理功能
    #===============================================================================

    def editing_finished(self, item, column, original_value):
        """
        处理树项内容改变事件
        """
        # 根据列号调用相应的处理方法
        handlers = {
            0: self.address_edit,
            1: self.function_edit,
            2: self.record_edit,
            3: self.var_name_edit,
            4: self.multi_var_edit,
            5: self.formula_edit,
            6: self.input_range_edit,
            7: self.sign_edit
        }
        
        handler = handlers.get(column)
        if handler:
            handler(item, original_value)
        else:
            # 默认处理：更新YAML配置
            self.yaml.update_function_config()

    def address_edit(self, item, original_value):
        """
        处理地址编辑完成事件
        """
        # 获取输入的地址
        addr = item.text(0).strip()

        # print(f'addr: {addr}')

        # 验证输入地址是否存在
        if addr == '':
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入地址！"
            )
            # 恢复原始值
            item.setText(0, original_value)
            return
        
        # 验证输入地址是否有效，并格式化地址
        formatted_addr = self.is_addr_valid(addr)
        if formatted_addr is False:
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入正确的地址格式（00-FF）！"
            )
            # 恢复原始值
            item.setText(0, original_value)
            return

        # 检查是否存在相同的地址（排除当前项）
        old_configs = self.get_configs()
        # print(f'地址的old_configs: {old_configs}')

        if old_configs is None:
            # 恢复原始值
            item.setText(0, original_value)
            return

        # 找到当前项的索引
        current_index = -1
        for i in range(self.ui.tree_config.topLevelItemCount()):
            if self.ui.tree_config.topLevelItem(i) == item:
                current_index = i
                break

        # 检查是否存在相同的地址（排除当前项）
        is_same = False
        for i, config in enumerate(old_configs):
            # 排除当前项进行比较
            if i != current_index and config['address'].upper() == formatted_addr.upper():
                is_same = True
                break

        if is_same:
            QMessageBox.warning(
                self, 
                "警告", 
                "该地址已存在！"
            )
            # 恢复原始值
            item.setText(0, original_value)
            return
        
        item.setText(0, formatted_addr)
        self.yaml.update_function_config()

    def function_edit(self, item, original_value):
        """
        处理算法功能编辑完成事件
        """
        # 获取输入的功能
        func = item.text(1).strip()

        # 验证输入功能是否存在
        if func == '':
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入功能！"
            )
            # 恢复原始值
            item.setText(1, original_value)
            return
        
        # 检查是否存在相同的功能（排除当前项）
        old_configs = self.get_configs()

        # print(f'算法功能的old_configs: {old_configs}')

        if old_configs is None:
            # 恢复原始值
            item.setText(1, original_value)
            return

        # 找到当前项的索引
        current_index = -1
        for i in range(self.ui.tree_config.topLevelItemCount()):
            if self.ui.tree_config.topLevelItem(i) == item:
                current_index = i
                break

        # 检查是否存在相同的功能（排除当前项）
        is_same = False
        for i, config in enumerate(old_configs):
            # 排除当前项进行比较
            if i != current_index and config['function'] == func:
                is_same = True
                break

        if is_same:
            QMessageBox.warning(
                self, 
                "警告", 
                "该算法功能已分配给对应的地址！"
            )
            # 恢复原始值
            item.setText(1, original_value)
            return
        
        item.setText(1, func)
        self.yaml.update_function_config()

    def record_edit(self, item, original_value):
        """
        处理记录状态编辑完成事件
        """
        # 获取输入的记录状态
        record = item.text(2).strip()

        # 验证输入记录状态是否存在
        if record == '':
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入记录状态！"
            )
            # 恢复原始值
            item.setText(2, original_value)
            return
        
        # 检查输入记录状态是否有效
        if record not in ['是', '否']:
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入有效记录状态（是/否）！"
            )
            # 恢复原始值
            item.setText(2, original_value)
            return
        
        item.setText(2, record)
        self.yaml.update_function_config()

    def var_name_edit(self, item, original_value):
        """
        处理变量名称编辑完成事件
        """
        # 获取输入的变量名称
        var_name = item.text(3).strip()

        # 获取多变量状态
        multi_var = item.text(4).strip()

        # 处理中文字符
        processed_var_name = self.process_chinese_characters(var_name)
        
        # 如果没有输入变量名称，默认使用"无"
        if processed_var_name == '':
            item.setText(3, "无")
            self.yaml.update_function_config()
            return
        
        # 验证变量名称（包括多变量状态验证）
        var_name_validation = self.check_var_name(processed_var_name)
        if not var_name_validation["is_valid"]:
            QMessageBox.warning(
                self, 
                "警告", 
                var_name_validation["error_message"]
            )
            # 恢复原始值
            item.setText(3, original_value)
            return

        item.setText(3, processed_var_name)
        self.yaml.update_function_config()

    def multi_var_edit(self, item, original_value):
        """
        处理多变量开启编辑完成事件
        """
        # 获取输入的变量类型
        multi_var = item.text(4).strip()

        # 验证输入多变量状态是否存在
        if multi_var == '':
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入多变量状态！"
            )
            # 恢复原始值
            item.setText(4, original_value)
            return
        
        # 检查输入多变量状态是否有效
        if multi_var not in ['是', '否']:
            QMessageBox.warning(
                self, 
                "警告", 
                "请输入有效记录状态（是/否）！"
            )
            # 恢复原始值
            item.setText(4, original_value)
            return

        item.setText(4, multi_var)
        self.yaml.update_function_config()

    def formula_edit(self, item, original_value):
        """
        处理计算公式编辑完成事件
        """
        var_name = item.text(3).strip()
        multi_var = item.text(4).strip()
        
        # 获取输入的公式
        formula = item.text(5).strip()

        # print(f'公式: {formula}')
        
        # 如果没有输入公式，默认使用"无"
        if formula == '':
            item.setText(5, "无")
            self.yaml.update_function_config()
            return
        
        # 处理中文字符
        processed_formula = self.process_chinese_characters(formula)

        # 检查公式完整性
        if not self.check_formula_completeness(processed_formula):
            QMessageBox.warning(
                self, 
                "警告", 
                "公式不完整！"
            )
            # 恢复原始值
            item.setText(5, original_value)
            return

        # 检查语法
        syntax_valid, error_msg = self.check_syntax(processed_formula)
        if not syntax_valid:
            QMessageBox.warning(
                self, 
                "警告", 
                f"公式语法错误：{error_msg}"
            )
            # 恢复原始值
            item.setText(5, original_value)
            return
        
        check_formula = self.check_formula(processed_formula, var_name, multi_var)
        if not check_formula["is_valid"]:
            QMessageBox.warning(
                self, 
                "警告", 
                f"出现错误：{check_formula['error_message']}"
            )
            # 恢复原始值
            item.setText(5, original_value)
            return
        
        item.setText(5, processed_formula)
        self.yaml.update_function_config()

    def input_range_edit(self, item, original_value):
        """
        处理输入范围编辑完成事件
        """
        range_val = item.text(6).strip()

        # 如果没有输入范围，默认使用"无"
        if range_val == '' or range_val == '无':
            item.setText(6, "无")
            self.yaml.update_function_config()
            return

        # 验证输入范围格式
        is_valid = self.check_input_range(range_val)

        if is_valid is False:
            QMessageBox.warning(
                self, 
                "警告", 
                "输入范围格式错误,请输入如 [1,2]"
            )
            # 恢复原始值
            item.setText(6, original_value)
            return
        
        # 处理中文字符
        range_val = self.process_chinese_characters(range_val)
        
        item.setText(6, range_val)
        self.yaml.update_function_config()

    def sign_edit(self, item, original_value):
        """
        处理符号位编辑完成事件
        """
        sign = item.text(7).strip()

        # 如果没有输入符号，默认使用"否"
        if sign == '':
            item.setText(7, "否")
            self.yaml.update_function_config()
            return

        item.setText(7, sign)
        self.yaml.update_function_config()

    #===============================================================================
    # 数据加载和获取功能
    #===============================================================================

    def load_function_config(self, config_data):
        """
        从YAML加载功能配置数据
        
        Args:
            config_data: 从YAML文件读取的功能配置数据
        """
        # 清空现有配置
        self.ui.tree_config.clear()
        
        # 添加配置项
        for item in config_data:
            addr = item.get('address')
            func = item.get('function')
            record = item.get('record')
            var_name = item.get('var_name')
            multi_var = item.get('multi_var')
            formula = item.get('formula')
            range_val = item.get('range_val')
            sign = item.get('sign')

            # 处理record字段，确保是字符串类型
            if isinstance(record, bool):
                record = "是" if record else "否"
                # print(record)

            # 处理sign字段，确保是字符串类型
            if isinstance(sign, bool):
                sign = "是" if sign else "否"

            # 创建新的树节点
            tree_item = QTreeWidgetItem(self.ui.tree_config)
            tree_item.setText(0, addr)
            tree_item.setText(1, func)
            tree_item.setText(2, record)
            tree_item.setText(3, var_name)
            tree_item.setText(4, multi_var)
            tree_item.setText(5, formula)
            tree_item.setText(6, range_val)
            tree_item.setText(7, sign)

            # 设置item的高度和字体
            font = tree_item.font(0)
            font.setPointSize(10)
            tree_item.setFont(0, font)
            tree_item.setFont(1, font)
            tree_item.setFont(2, font)
            tree_item.setFont(3, font)
            tree_item.setFont(4, font)
            tree_item.setFont(5, font)
            tree_item.setFont(6, font)
            tree_item.setFont(7, font)

            tree_item.setFlags(tree_item.flags() | Qt.ItemFlag.ItemIsEditable)  # 默认允许编辑

            # 设置行高
            tree_item.setSizeHint(0, QSize(0, 30))
        
    def get_configs(self):
        """
        获取所有配置项的数据
        返回格式：[{'address': 地址, 'function': 功能, 'record': 是否记录}, ...]
        """
        items = []
        for i in range(self.ui.tree_config.topLevelItemCount()):
            item = self.ui.tree_config.topLevelItem(i)

            addr = item.text(0)
            func = item.text(1)
            record = item.text(2)
            var_name = item.text(3)
            multi_var = item.text(4)
            formula = item.text(5)
            range_val = item.text(6)
            sign = item.text(7)

            items.append({
                'address': addr,
                'function': func,
                'record': record, 
                'var_name': var_name, 
                'multi_var': multi_var,
                'formula': formula, 
                'range_val': range_val, 
                'sign': sign
            })

        return items

    #===============================================================================
    # 界面控制功能
    #===============================================================================

    def toggle_record_state(self):
        """
        切换记录状态按钮的文本和状态
        """
        button = self.sender()  # 获取发送信号的按钮
        if button.isChecked():
            button.setText("✔")
            self.yaml.update_function_config()
        else:
            button.setText("")
            self.yaml.update_function_config()

    def toggle_sign_state(self):
        """
        切换符号位状态按钮的文本和状态
        """
        button = self.sender()  # 获取发送信号的按钮
        if button.isChecked():
            button.setText("✔")
            self.yaml.update_function_config()
            # print("符号位已启用")
        else:
            button.setText("")
            self.yaml.update_function_config()
            # print("符号位已禁用")

    def toggle_formula_widget_state(self):
        """
        切换公式输入框的显示状态
        """
        self.show_widget = not self.show_widget
        self.ui.formula_widget.setVisible(self.show_widget)

    #===============================================================================
    # 辅助功能
    #===============================================================================

    def process_chinese_characters(self, text):
        """
        处理文本中的中文字符，将其转换为英文字符
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return ""
        
        # 中文符号到英文符号的映射
        chinese_to_english = {
            '（': '(',
            '）': ')',
            '＋': '+',
            '－': '-',  # 注意这里是中文的减号
            '×': '*',   # 中文乘号
            '÷': '/',   # 中文除号
            '＝': '=',   # 中文等号
            '《': '<',   # 中文小于号
            '》': '>',   # 中文中号
            '【': '[',   # 中文方括号
            '】': ']',   # 中文方括号
            '｛': '{',   # 中文花括号
            '｝': '}',   # 中文花括号
            '，': ',',   # 中文逗号
            '。': '.',   # 中文句号
            '；': ';',   # 中文分号
            '：': ':',   # 中文冒号
            '“': '"',   # 中文双引号
            '”': '"',   # 中文双引号
            '‘': "'",   # 中文单引号
            '’': "'",   # 中文单引号
        }
        
        # 替换中文符号为英文符号
        processed_text = text
        for chinese, english in chinese_to_english.items():
            processed_text = processed_text.replace(chinese, english)

        return processed_text
    