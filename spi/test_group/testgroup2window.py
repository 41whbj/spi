from PySide6.QtWidgets import QComboBox, QListWidget, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt
from data_group.custom_widgets import SPI_Data_Widget

class TestGroupManager:
    
    def __init__(self, combo_box_mode_group, list_group, list_data, parent=None):
        self.combo_box_mode_group = combo_box_mode_group
        self.list_group = list_group
        # self.combo_box_data_group = combo_box_data_group
        self.list_data = list_data
        self.parent = parent

        self.group_data = {}
        self.current_group = None

        self.group_count = 0

        self.init_manager()

    def init_manager(self):
        self.combo_box_mode_group.setEditable(True)
        self.combo_box_mode_group.setInsertPolicy(QComboBox.NoInsert)

        self.list_group.model().rowsInserted.connect(self.mode_group_insert)

        self.combo_box_mode_group.lineEdit().setReadOnly(False)
        self.combo_box_mode_group.lineEdit().editingFinished.connect(self.mode_group_name_changed)

        self.list_group.setDragDropMode(QListWidget.DropOnly)
        self.list_group.setDefaultDropAction(Qt.CopyAction)
        self.list_group.setAcceptDrops(True)
        self.list_group.setDropIndicatorShown(True)

        self.add_mode_group()

    def mode_group_name_changed(self):
        # Get new name from line edit
        new_name = self.combo_box_mode_group.lineEdit().text().strip()
        if not new_name:
            return

        # Get current index
        current_index = self.combo_box_mode_group.currentIndex()
        # If index is valid, set blank name
        if current_index < 0:
            self.combo_box_mode_group.lineEdit().setText("" if not self.current_group else self.current_group)
            return
        
        # Compare new name with original name，ensure name is unique
        original_name = self.combo_box_mode_group.itemText(current_index)
        
        if new_name == original_name:
            return

        # Compare new name with existing names
        for i in range(self.combo_box_mode_group.count()):
            if i != current_index and self.combo_box_mode_group.itemText(i) == new_name:
                QMessageBox.warning(self, "警告", "分组名称已存在！")
                # reset change
                self.combo_box_mode_group.lineEdit().setText(original_name)
                return

        if original_name in self.group_data:
            # Get original data
            original_data = self.group_data.pop(original_name)
            # Add the previous data under the new name
            self.group_data[new_name] = original_data

        # Refresh original_name to new_name
        self.combo_box_mode_group.setItemText(current_index, new_name)

        # Refresh current_group to new_name
        if self.current_group == original_name:
            self.current_group = new_name

        # Reset current_index
        self.combo_box_mode_group.setCurrentIndex(current_index)

    def add_mode_group(self):

        self.group_count += 1

        new_group_name = f"新建分组{self.group_count}"

        # print(f"group_count: {self.group_count}")

        self.combo_box_mode_group.addItem(new_group_name)
        self.group_data[new_group_name] = []

        # print(f"self.group_data: {self.group_data}")

        self.current_group = new_group_name
        new_index = self.combo_box_mode_group.count() - 1
        self.combo_box_mode_group.setCurrentIndex(new_index)
        self.combo_box_mode_group.setCurrentText(new_group_name)
        self.load_mode_group_data(new_group_name)

    def delete_mode_group(self):
        current_index = self.combo_box_mode_group.currentIndex()
        if current_index < 0:
            return

        group_name = self.combo_box_mode_group.currentText()

        self.combo_box_mode_group.removeItem(current_index)

        # print(f"current_index: {current_index}")

        if group_name in self.group_data:
            del self.group_data[group_name]
        
        if self.combo_box_mode_group.count() <= 0:
            self.current_group = None
            self.group_count = 0
            self.list_group.clear()

    def load_mode_group_data(self, group_name):
        self.list_group.clear()
        # print(f"group_name: {group_name}")
        # print(f"self.group_data: {self.group_data}")
        
        if group_name not in self.group_data:
            return

        for item_data in self.group_data[group_name]:
            # print(f"item_data: {item_data}")
            clone_item = QListWidgetItem()
            if isinstance(item_data, dict) and 'name' in item_data and 'data' in item_data:
                data_tuple = (item_data['name'], item_data['data'])
                clone_item.setData(Qt.UserRole, data_tuple)
            elif hasattr(item_data, 'data') and callable(item_data.data):
                data_tuple = item_data.data(Qt.UserRole)
                if data_tuple:
                    clone_item.setData(Qt.UserRole, data_tuple)
            else:
                clone_item.setData(Qt.UserRole, item_data)

            self.list_group.addItem(clone_item)

            data_tuple = clone_item.data(Qt.UserRole)

            if data_tuple and len(data_tuple) >= 2:
                data_name, data_text = data_tuple
                list_item_widget = SPI_Data_Widget(
                    self.list_group,
                    data_name,
                    data_text,
                    show_all=False,
                    checkable=False,
                    sendable=False
                )

                list_item_widget.set_user_data(clone_item)
                list_item_widget.send_clicked_signal.connect(self.parent.spi_send_item)
                self.list_group.setItemWidget(clone_item, list_item_widget)

    # handle when insert item
    def mode_group_insert(self, parent, start, end):
        current_index = self.combo_box_mode_group.currentIndex()
        group_name = self.combo_box_mode_group.itemText(current_index)

        # add item to group_data
        if group_name not in self.group_data:
            return
        
        for i in range(start, end + 1):
            item = self.list_group.item(i)
            
            # skip empty item
            if not item or item.data(Qt.UserRole):
                continue
            
            select_item = self.list_data.selectedItems()
            if not select_item:
                self.list_group.takeItem(i)
                continue

            source_item = select_item[0]
            data_tuple = source_item.data(Qt.UserRole)
            if not data_tuple or len(data_tuple) < 2:
                self.list_group.takeItem(i)
                continue

            # create custom widget
            data_name, data_text = data_tuple
            list_item_widget = SPI_Data_Widget(
                self.list_group,
                data_name,
                data_text,
                show_all=False,
                checkable=False,
                sendable=False
            )

            list_item_widget.set_user_data(item)
            list_item_widget.send_clicked_signal.connect(self.parent.spi_send_item)
            self.list_group.setItemWidget(item, list_item_widget)
        
            # add item to group_data
            self.group_data[group_name].append(data_tuple)

    def save_current_mode_group(self):
        if self.current_group is None:
            return
        
        current_data = []
        
        for i in range(self.list_group.count()):
            item = self.list_group.item(i)

            if not item or not item.data(Qt.UserRole):
                continue

            data_tuple = item.data(Qt.UserRole)

            if data_tuple and len(data_tuple) >= 2:
                current_data.append(data_tuple)

        if current_data != self.group_data.get(self.current_group, []):
            self.group_data[self.current_group] = current_data


    def delete_mode_group_item(self):
        selected_items = self.list_group.selectedItems()
        if not selected_items:
            return

        for item in reversed(selected_items):
            row = self.list_group.row(item)
            if row >= 0:
                self.list_group.takeItem(row)
            
    def get_test_group(self):
        """get group data
        
        Returns:
            dict: contain all group data
        """        
        data = {}
        # print(self.group_data)
        # Traverse the data
        for group_name, items in self.group_data.items():
                # Create list
                data[group_name] = []
                for item in items:
                    # add item data to list
                    if isinstance(item, dict) and 'name' in item and 'data' in item:
                        data_tuple = (item['name'], item['data'])
                        data[group_name].append(data_tuple)
                    elif hasattr(item, 'data') and callable(item.data):
                        data_tuple = item.data(Qt.UserRole)
                        if data_tuple and len(data_tuple) >= 2:
                            data[group_name].append(data_tuple)
                    elif isinstance(item, (tuple, list)) and len(item) >= 2:
                        data[group_name].append(tuple(item))
                    else:
                        data[group_name].append(item)
        
        return data
    
    def set_test_group(self, group_data):
        """set group data
        
        Args:
            group_data (dict): contain all group data
        """
        self.group_data = group_data

        group_names = list(self.group_data.keys())
        for group_name in group_names:
            self.combo_box_mode_group.addItem(group_name)

        if group_data:
            first_group = next(iter(group_data.keys()))
            self.current_group = first_group
            self.combo_box_mode_group.setCurrentText(first_group)
            self.load_mode_group_data(first_group)