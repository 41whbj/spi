#!/usr/bin/env python3.13
"""
filename: data_group_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-01
description: Data group manager for handling data group operations
"""

from PySide6.QtWidgets import QListWidget, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt, QObject, QTimer
from sub_window.sub_name import SubWindowName
from .custom_widgets import User_ListItemWidget

class DataGroupManager(QObject):
    
    def __init__(self, combo_box_data_group, list_data, parent=None):
        super().__init__()
        self.parent = parent
        self.combo_box_data_group = combo_box_data_group
        self.list_data = list_data
        self.current_group = None

        """
            Unified group management
            - key: group name
            - value: {
                'data': []
            }
        """
        self.group_manager = {}

        # Handle default group when run first time
        if self.combo_box_data_group.count() > 0:
            default_group_name = self.combo_box_data_group.itemText(0)
            self.group_manager[default_group_name] = {
                'data': [],
            }
            self.current_group = default_group_name

        self.combo_box_data_group.currentIndexChanged.connect(self.group_changed)

        # Setup auto save timer
        self.setup_auto_save_timer()

    def add_data_group(self, parent_window):

        def add_name(name):
            # Advoid name conflict
            if name in self.group_manager:
                QMessageBox.warning(
                    parent_window,
                    '警告',
                    f'{name} 已存在，请选择其他名称。'
                )
                return

            self.combo_box_data_group.addItem(name)
            self.combo_box_data_group.setCurrentIndex(self.combo_box_data_group.count() - 1)

            # Add to group manager
            self.group_manager[name] = {
                'data': [],
            }

        parent_window.name_window = SubWindowName(parent_window)
        parent_window.name_window.show()
        parent_window.name_window.name_updated.connect(add_name)

    def handle_rename_button(self, parent_window):

        # Get current index
        current_index = self.combo_box_data_group.currentIndex()

        if current_index >= 0:
            current_text = self.combo_box_data_group.currentText().strip()
            # Get subwindow input
            parent_window.name_window = SubWindowName(parent_window, current_text)
            parent_window.name_window.name_updated.connect(
                lambda new_name: self.on_name_updated(parent_window, new_name, current_index)
            )
            parent_window.name_window.show()

    def on_name_updated(self, parent_window, new_name, index=None):
        # Check the index is valid
        if index is not None and 0 <= index < self.combo_box_data_group.count():
            old_name = self.combo_box_data_group.currentText()

            # Advoid name conflict
            if new_name in self.group_manager:
                QMessageBox.warning(
                    parent_window,
                    '警告',
                    f'{new_name} 已存在，请选择其他名称。'
                )
                return

            print(self.group_manager)
            self.combo_box_data_group.setItemText(index, new_name)

            if old_name in self.group_manager:
                self.group_manager[new_name] = self.group_manager.pop(old_name)

    def delete_data_group(self):
        # Get current index
        current_index = self.combo_box_data_group.currentIndex()
        current_group_name = self.combo_box_data_group.currentText()

        # Confirm delete
        reply = QMessageBox.question(
            self.combo_box_data_group,
            '确认删除',
            f'确定删除分组 "{self.combo_box_data_group.currentText()}" 吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes and current_index >= 0:
            # Save current group data
            self.save_current_group_data()

            # Remove item from combo box
            self.combo_box_data_group.removeItem(current_index)
            if current_group_name in self.group_manager:
                del self.group_manager[current_group_name]
            
            # Update last saved data next group
            if hasattr(self, 'last_saved_data'):
                # If there are other groups, update last saved data for next group
                if self.combo_box_data_group.count() > 0:
                    next_group_name = self.combo_box_data_group.currentText()
                    if next_group_name in self.group_manager:
                        self.last_saved_data = self.group_manager[next_group_name]['data']
                else:
                    # No more groups, clear last saved data
                    self.last_saved_data = []
    
    def get_current_group_name(self):
        current_index = self.combo_box_data_group.currentIndex()
        
        if current_index >= 0:
            return self.combo_box_data_group.currentText()
        
        return None

    def setup_list_data_drag_drop(self):
        # User-defined list widget settings 
        # Realize drag-and-drop function
        self.list_data.setDragDropMode(QListWidget.InternalMove)
        self.list_data.setSelectionMode(QListWidget.SingleSelection)
        self.list_data.setDefaultDropAction(Qt.MoveAction)
        self.list_data.setDragEnabled(True)
        self.list_data.setAcceptDrops(True)
        self.list_data.setDropIndicatorShown(True)

    def get_current_list_data(self):
        items = []

        # Get all items in the list_data widget
        for i in range(self.list_data.count()):
            item = self.list_data.item(i)
            if item and item.data(Qt.UserRole):
                items.append(item.data(Qt.UserRole))

        return items

    def set_current_list_data(self, items):
        self.list_data.clear()
        for item_data in items:
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, item_data)

            if isinstance(item_data, tuple) and len(item_data) >= 2:
                data_name, data_text = item_data[0], item_data[1]
                list_item_widget = User_ListItemWidget(
                    self.list_data,
                    data_name,
                    data_text,
                    show_all=True,
                    checkable=False
                )
                
                list_item_widget.set_user_data(list_item)
                list_item_widget.send_clicked.connect(self.item_send_clicked)

                self.list_data.addItem(list_item)
                self.list_data.setItemWidget(list_item, list_item_widget)
            elif isinstance(item_data, dict) and 'name' in item_data:
                list_item.setText(str(item_data['name']))
                self.list_data.addItem(list_item)

    def group_changed(self, index):
        if index < 0:
            return

        group_name = self.combo_box_data_group.currentText()

        # Update current group
        self.current_group = group_name

        # Load new group data
        self.load_group_data(group_name)

    def save_current_group_data(self):
        current_group = self.get_current_group_name()

        if current_group and current_group in self.group_manager:
            # Update group_manager
            self.group_manager[current_group]['data'] = self.get_current_list_data()
            # 更新上次保存的数据状态
            if hasattr(self, 'last_saved_data'):
                self.last_saved_data = self.group_manager[current_group]['data']

    def load_group_data(self, group_name):
        if group_name in self.group_manager:
            group_data = self.group_manager[group_name]
            # Load 'data' and 'spi_config'
            self.set_current_list_data(group_data['data'])
            # 更新上次保存的数据状态
            if hasattr(self, 'last_saved_data'):
                self.last_saved_data = group_data['data']

        else:
            self.list_data.clear()
            # 更新上次保存的数据状态
            if hasattr(self, 'last_saved_data'):
                self.last_saved_data = []

    # Get all items in the list_data widget
    def get_list_data_items(self):
        items = []

        for i in range(self.list_data.count()):
            item = self.list_data.item(i)
            if item and item.data(Qt.UserRole):
                items.append(item)
        
        return items

    def remove_selected_items_from_list_data(self):
        # Get selected items
        selected_items = self.list_data.selectedItems()

        for item in selected_items:
            row = self.list_data.row(item)
            self.list_data.takeItem(row)
    
    def clear_list_data(self):
        self.list_data.clear()

    def item_send_clicked(self, item):
            if self.parent and hasattr(self.parent, 'spi_send_item'):
                self.parent.spi_send_item(item)

    def setup_auto_save_timer(self):

        # Create timer for check data change
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.check_and_save_data)
        print('test0')
        
        # Check data change every 2s
        self.auto_save_timer.start(2000)
        
        # Track last saved data for each group
        self.last_saved_data = {}

    def check_and_save_data(self):
        current_group = self.get_current_group_name()
        
        if current_group and current_group in self.group_manager:
            # Get current list data and spi config
            current_data = self.get_current_list_data()
            # current_spi_config = self.get_current_spi_config()
            
            # Check if data or spi config has changed
            if (self.last_saved_data != current_data):

                # Data has changed, save current group data
                self.save_current_group_data()
                self.last_saved_data = current_data

        # print(f"Group manager: {self.group_manager}")

    def set_data_group(self, group_data):
        """set group data
        
        Args:
            group_data (dict): contain all group data
        """
        self.group_manager = group_data

        group_names = list(self.group_manager.keys())
        for group_name in group_names:
            self.combo_box_data_group.addItem(group_name)

        if group_data:
            first_group = next(iter(group_data.keys()))
            self.current_group = first_group
            self.combo_box_data_group.setCurrentText(first_group)
            self.load_group_data(first_group)
