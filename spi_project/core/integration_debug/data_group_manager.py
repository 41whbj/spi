#!/usr/bin/env python3.13
"""
filename: data_data_group_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-07
description: 数据组管理器，用于处理数据组操作
"""

from PySide6.QtWidgets import QListWidget, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt, QObject
from .data_widget import Data_Widget

class DataGroupManager(QObject):
    """
    数据组管理器类，负责管理多个数据组，包括添加、删除、重命名、保存和加载数据组等功能
    """

    data_group_manager = {}
    combo_box_data_group = []
    list_data = []
    
    def __init__(self, application,sub_window):
        """
        初始化数据组管理器
        
        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.sub_window = sub_window

        # 当前选中的数据组名称
        self.current_group = None

        """
            统一的数据组管理结构（使用列表）
            - 每个元素是一个字典，包含：
              {
                'name': 数据组名称,
                'data': []  # 存储该组的数据列表
              }
        """

        # 处理首次运行时的默认数据组
        if self.ui.combo_box_data_group.count() > 0:

            # 获取默认数据组名称
            default_group_name = self.ui.combo_box_data_group.itemText(0)

            # 将默认数据组添加到管理器中（作为列表中的字典元素）
            self.data_group_manager.append({
                'name': default_group_name,
                'data': [], # 初始化空的数据列表
            })

            # 设置当前数据组为默认组
            self.current_group = default_group_name

    def add_new_name(self,new_name):
        """
        添加数据组名称的内部函数
        
        Args:
            name: 要添加的数据组名称
        """

        # 避免名称冲突
        if new_name in self.data_group_manager:
            QMessageBox.warning(
                self.application,
                '警告',
                f'{new_name} 已存在，请选择其他名称。'
            )
            return
        
            # 将新名称添加到下拉框中
        self.ui.combo_box_data_group.addItem(new_name)

        # 设置为当前选中项
        self.ui.combo_box_data_group.setCurrentIndex(self.ui.combo_box_data_group.count() - 1)

        # 添加到数据组管理器中
        self.data_group_manager[new_name] = {
            'data': [],
        }

        # 设置为当前选中项
        self.ui.combo_box_data_group.setCurrentIndex(self.ui.combo_box_data_group.count() - 1)
        
        # 手动触发数据组切换事件，确保界面正确更新
        self.group_changed(self.ui.combo_box_data_group.count() - 1)


        # print(f"当前数据组管理器: {self.data_group_manager}")

    def add_data_group(self):
        """
        添加新的数据组
        """

        self.sub_window.name_window(self.add_new_name, "添加数据组")

    def handle_rename_button(self):
        """
        处理重命名按钮点击事件
        """

        # 获取当前选中的索引
        current_index = self.ui.combo_box_data_group.currentIndex()

        if current_index == -1:
            QMessageBox.warning(
                self.application,
                '警告',
                '当前无数据组，无法重命名。'
            )
            return

        if current_index >= 0:

            # 获取当前的文本
            current_text = self.ui.combo_box_data_group.currentText().strip()

            self.sub_window.name_window(
                lambda new_name: self.name_updated(new_name, current_text, current_index)
            )
            
    def name_updated(self,new_name, old_name, index=None):
        """
        处理名称更新事件
        
        Args:
            new_name: 新的名称
            index: 数据组索引
        """
         # 检查索引是否有效
        if index is not None and 0 <= index < self.ui.combo_box_data_group.count():

            # 避免名称冲突
            if new_name in self.data_group_manager:
                QMessageBox.warning(
                    self.application,
                    '警告',
                    f'{new_name} 已存在，请选择其他名称。'
                )
                return

            # 更新下拉框中的文本
            self.ui.combo_box_data_group.setItemText(index, new_name)

            # 更新数据组管理器中的键名
            if old_name in self.data_group_manager:
                self.data_group_manager[new_name] = self.data_group_manager.pop(old_name)

            # print(f"重命名数据组 {old_name} 为 {new_name} 成功")
            # print(f"name_updated当前数据组管理器: {self.data_group_manager}")

    def delete_data_group(self):
        """
        删除当前选中的数据组
        """

        # 获取当前选中的索引和组名
        current_index = self.ui.combo_box_data_group.currentIndex()
        current_group_name = self.ui.combo_box_data_group.currentText()

         # 确认删除操作
        reply = QMessageBox.question(
            self.ui.combo_box_data_group,
            '确认删除',
            f'确定删除分组 "{self.ui.combo_box_data_group.currentText()}" 吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes and current_index >= 0:
            # 保存当前组数据
            # self.save_current_group_data()

            # 从下拉框中移除项
            self.ui.combo_box_data_group.removeItem(current_index)
            if current_group_name in self.data_group_manager:

                # 从管理器中删除对应的数据组
                del self.data_group_manager[current_group_name]

            if self.ui.combo_box_data_group.count() <= 0:

                # 清空数据列表
                self.ui.list_data.clear()

                # 重置当前组引用
                self.current_group = None

            # 更新YAML文件中的数据组
            self.application.yaml_window.update_data_group()

    def get_current_group_name(self):
        """
        获取当前选中的数据组名称
        
        Returns:
            str or None: 当前数据组名称，如果没有选中则返回None
        """
        current_index = self.ui.combo_box_data_group.currentIndex()
        
        if current_index >= 0:

            # 返回当前选中的文本
            return self.ui.combo_box_data_group.currentText()
        
        return None

    def add_data_widget(self, data_name, data_text, show_all=True):
        """
        处理主窗口数据输入，清理非法字符，格式化数据显示，并添加到列表中
        
        Args:
            data_name (str): 数据项的名称
            data_text (str): 原始数据文本
            show_all (bool): 是否显示所有数据项，默认为True
        """

        # 清理data_text中的非法字符，只保留十六进制字符(0-9, A-F, a-f)
        clean_text = ''.join(c for c in data_text if c in '0123456789ABCDEFabcdef')

        # 如果clean_text长度为奇数，在前面补0使其成为偶数长度
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # 将clean_text格式化为每两个字符用空格分隔的形式(XX XX XX ...)
        format_text = ' '.join(clean_text[i:i+2] for i in range(0, len(clean_text), 2))

        # 获取当前组名并检查是否存在同名数据项，避免重复添加
        current_group_name = self.get_current_group_name()

        if current_group_name in self.data_group_manager:
            
            existing_data = self.data_group_manager[current_group_name]['data']

            for item in existing_data:

                existing_name, _ = item
                if existing_name == data_name:
                    QMessageBox.warning(
                        self.application, 
                        '警告', 
                        f"名称 '{data_name}' 已存在，请选择其他名称。"
                    )
                    return

        # 创建一个新的列表项并设置用户数据
        item = QListWidgetItem()
        item.setData(Qt.UserRole, (data_name, format_text))
        self.ui.list_data.addItem(item)

        if current_group_name in self.data_group_manager:
            # 将新的数据项添加到当前组的数据列表中
            self.data_group_manager[current_group_name]['data'].append((data_name, format_text))

        # print(f"添加数据后的data_group_manager：{self.data_group_manager}")

        # 创建自定义的数据控件
        list_item_widget = Data_Widget(
            self.ui.list_data,
            data_name,
            format_text,
            show_all,
            checkable= False
        )

        list_item_widget.set_user_data(item)

        list_item_widget.send_clicked_signal.connect(self.item_send_clicked)
        list_item_widget.data_changed_signal.connect(self.item_data_changed)
        list_item_widget.add_clicked_signal.connect(
            self.application.test_group_window.test_group_manager.send_item
        )

        # 添加项目和控件到列表
        self.ui.list_data.addItem(item)
        self.ui.list_data.setItemWidget(item, list_item_widget)

        self.application.update_all_crc_tooltips()

    def setup_list_data_drag_drop(self):
        """
        设置数据列表的拖拽功能
        """
        # User-defined list widget settings 
        # Realize drag-and-drop function
        self.ui.list_data.setDragDropMode(QListWidget.InternalMove) # 设置拖拽模式为内部移动
        self.ui.list_data.setSelectionMode(QListWidget.SingleSelection) # 设置选择模式为单选
        self.ui.list_data.setDefaultDropAction(Qt.MoveAction) # 设置默认放置动作为移动
        self.ui.list_data.setDragEnabled(True) # 启用拖拽
        self.ui.list_data.setAcceptDrops(True) # 允许放置
        self.ui.list_data.setDropIndicatorShown(True) # 显示放置指示器

        # 连接拖拽完成后的信号，用于同步数据顺序
        self.ui.list_data.model().rowsMoved.connect(self.item_moved)

    def item_moved(self, sourceParent, sourceStart, sourceEnd, destinationParent, destinationRow):
        """
        处理列表行移动事件，同步更新group_manager中的数据顺序
        
        Args:
            sourceParent: 源父项
            sourceStart: 源起始行
            sourceEnd: 源结束行
            destinationParent: 目标父项
            destinationRow: 目标行
        """
        # 获取当前数据组名称
        current_group_name = self.get_current_group_name()
        
        # 检查当前数据组是否存在
        if current_group_name and current_group_name in self.data_group_manager:
            # 重新构建数据列表，按照UI中的顺序
            updated_data = []
            for i in range(self.ui.list_data.count()):
                item = self.ui.list_data.item(i)
                if item and item.data(Qt.UserRole):
                    updated_data.append(item.data(Qt.UserRole))
            
            # 更新group_manager中的数据顺序
            self.data_group_manager[current_group_name]['data'] = updated_data
            
            # 更新YAML文件
            self.application.yaml_window.update_data_group()

    def get_current_list_data(self):
        """
        获取当前列表中的所有数据项
        
        Returns:
            list: 包含所有数据项的列表
        """
        items = []

         # 获取list_data控件中的所有数据
        for i in range(self.list_data.count()):
            
            # 获取当前项
            item = self.ui.list_data.item(i)
            
            # 检查项是否有效
            if item and item.data(Qt.UserRole):
                items.append(item.data(Qt.UserRole))

        return items

    def set_current_list_data(self, items):
        """
        设置当前列表的数据项
        
        Args:
            items: 要设置的数据项列表
        """

        # 清空当前列表
        self.ui.list_data.clear()

        if items == []:
            return  

        # 遍历所有数据项并添加到列表中
        for item_data in items:
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, item_data)


            data_name, data_text = item_data[0], item_data[1]
            # 创建自定义的数据控件
            list_item_widget = Data_Widget(
                self.ui.list_data,
                data_name,
                data_text,
                show_all=True,
                checkable=False
            )
            
            # 设置用户数据并连接信号
            list_item_widget.set_user_data(list_item)
            list_item_widget.send_clicked_signal.connect(self.item_send_clicked)
            list_item_widget.data_changed_signal.connect(self.item_data_changed)
            list_item_widget.add_clicked_signal.connect(
                self.application.test_group_window.test_group_manager.send_item
            )

            # 添加项目和控件到列表
            self.ui.list_data.addItem(list_item)
            self.ui.list_data.setItemWidget(list_item, list_item_widget)

            self.application.update_all_crc_tooltips()


    def item_data_changed(self, item, new_data):
        """
        处理项目数据变化事件,即处理用户在数据列表中修改了数据
        
        Args:
            item: 发生变化的控件
            new_data: 新的数据
        """

        # 获取原始数据
        original_data = item.data(Qt.UserRole)

        # 创建更新后的元组，保持名称不变，只更新数据文本
        updated_data = (original_data[0], new_data)
        item.setData(Qt.UserRole, updated_data)
        
        # 获取当前选中的数据组名称
        current_group_name = self.get_current_group_name()

        # 检查当前选中的数据组是否存在
        if current_group_name and current_group_name in self.data_group_manager:

            # 获取当前选中的数据组中的数据
            group_data = self.data_group_manager[current_group_name]['data']

            # 遍历数据组中的每个数据项
            for i, data_item in enumerate(group_data):
                
                # 匹配名称
                if data_item[0] == original_data[0]:

                    # 更新data_group_manager中的数据
                    self.data_group_manager[current_group_name]['data'][i] = updated_data
                    
                    # print(f"更新后的data_group_manager数据: {self.data_group_manager}")

                    self.application.yaml_window.update_data_group()

                    break

    def group_changed(self, index):
        """
        处理数据组切换事件
        
        Args:
            index: 新选中的数据组索引
        """

        if index < 0:
            return

        # 获取新的数据组名称
        group_name = self.ui.combo_box_data_group.currentText()

        # 更新当前数据组
        self.current_group = group_name

        # 加载新数据组的数据
        self.load_group_data(group_name)

    def load_group_data(self, group_name):
        """
        加载指定数据组的数据
        
        Args:
            group_name: 要加载的数据组名称
        """

        if group_name in self.data_group_manager:

            # 获取数据组数据
            group_data = self.data_group_manager[group_name]

            # print(f"加载数据组 {group_name} 的数据: {group_data['data']}")

            # 加载'data'数据
            self.set_current_list_data(group_data['data'])

    def get_list_data_items(self):
        """
        获取数据列表中的所有项目
        
        Returns:
            list: 包含所有列表项的列表
        """

        items = []
        
        # 遍历所有列表项
        for i in range(self.ui.list_data.count()):
            item = self.ui.list_data.item(i)
            if item and item.data(Qt.UserRole):
                items.append(item)
        
        return items

    def remove_selected_items(self):
        """
        从数据列表中移除选中的数据控件
        """

        # 获取选中的项目
        selected_items = self.ui.list_data.selectedItems()

        # 获取当前数据组名称
        current_group_name = self.get_current_group_name()

        # 遍历并移除每个选中的项目
        for item in selected_items:

            # 从data_group_manager中删除数据
            if current_group_name and current_group_name in self.data_group_manager:
                item_data = item.data(Qt.UserRole)
                if item_data:

                    # 从当前组的data列表中移除匹配的数据项
                    self.data_group_manager[current_group_name]['data'] = [
                        data for data in self.data_group_manager[current_group_name]['data'] 
                        if data[0] != item_data[0]  # 根据名称匹配删除
                    ]

        # 遍历并移除每个选中的项目
        for item in selected_items:
            row = self.ui.list_data.row(item)
            self.ui.list_data.takeItem(row)

        self.application.yaml_window.update_data_group()

    def clear_list(self):
        """
        清空数据列表
        """
        self.ui.list_data.clear()

    def item_send_clicked(self, item):
        """
        处理项目发送按钮点击事件
        
        Args:
            item: 被点击的列表项
        """

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 从item中提取实际的数据
        item_data = item.data(Qt.UserRole)
        
        # item_data是一个元组，第二个元素是实际的数据文本
        data = item_data[1]
        self.application.spi_controller.spi_send(data,self.clk_mode,self.bit_order)

    def set_data_group(self, group_data):
        """
        设置数据组数据
        
        Args:
            group_data (dict): 包含所有数据组数据的字典
        """

        
        self.data_group_manager = group_data

        # 获取所有数据组的名称
        group_names = list(self.data_group_manager.keys())

        # 遍历这些组名，添加到下拉列表中
        for group_name in group_names:
            # print(f"添加数据组的类型 ：{type(group_name)}")
            self.ui.combo_box_data_group.addItem(group_name)

        # 获取第一个数据组的名称
        first_group = next(iter(group_data.keys()))

        # 设置当前数据组为第一个数据组
        self.current_group = first_group

        # 设置下拉列表的当前文本为第一个数据组
        self.ui.combo_box_data_group.setCurrentText(first_group)
        self.load_group_data(first_group)

    def get_data_group_manager(self):
        """
        获取data_group_manager的内容
        
        Returns:
            dict: data_group_manager的内容
        """
        return self.data_group_manager
