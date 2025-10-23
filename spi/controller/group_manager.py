from PySide6.QtWidgets import QComboBox, QListWidget, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt, QTimer
from .custom_widgets import User_ListItemWidget

class GroupManager:
    
    def __init__(self, combo_box_group, list_group, list_data, parent=None):
        self.combo_box_group = combo_box_group
        self.list_group = list_group
        self.list_data = list_data
        self.parent = parent

        self.group_data = {}
        self.current_group = None

        self.init_manager()

    def init_manager(self):
        self.combo_box_group.setEditable(True)
        self.combo_box_group.setInsertPolicy(QComboBox.NoInsert)

        self.list_group.model().rowsInserted.connect(self.list_group_insert)

        self.combo_box_group.lineEdit().setReadOnly(False)
        self.combo_box_group.lineEdit().editingFinished.connect(self.group_name_changed)

        self.list_group.setDragDropMode(QListWidget.DropOnly)
        self.list_group.setDefaultDropAction(Qt.CopyAction)
        self.list_group.setAcceptDrops(True)
        self.list_group.setDropIndicatorShown(True)

        self.add_group()

    def add_group(self):
        group_count = len(self.group_data)
        new_group_name = f"新建分组{group_count + 1}"

        if self.current_group is not None:
            self.save_current_group_data()

        self.combo_box_group.addItem(new_group_name)
        self.group_data[new_group_name] = []

        self.current_group = new_group_name
        new_index = self.combo_box_group.count() - 1
        self.combo_box_group.setCurrentIndex(new_index)
        self.combo_box_group.setCurrentText(new_group_name)
        self.load_group_data(new_group_name)

        if self.current_group is not None:
            self.save_current_group_data()

        # add delay to avoid auto_save error
        QTimer.singleShot(200, self.delayed_auto_save)

    def delete_group(self):
        current_index = self.combo_box_group.currentIndex()
        if current_index < 0:
            return

        group_name = self.combo_box_group.currentText()

        self.combo_box_group.removeItem(current_index)
        if group_name in self.group_data:
            del self.group_data[group_name]
        
        if self.combo_box_group.count() <= 0:
            self.current_group = None
            self.list_group.clear()

        if self.current_group is not None:
            self.save_current_group_data()

        QTimer.singleShot(200, self.delayed_auto_save)

    def group_name_changed(self):
        new_name = self.combo_box_group.lineEdit().text().strip()
        if not new_name:
            return

        current_index = self.combo_box_group.currentIndex()
        if current_index < 0:
            self.combo_box_group.lineEdit().setText("" if not self.current_group else self.current_group)
            return
        
        original_name = self.combo_box_group.itemText(current_index)
        
        if new_name == original_name:
            return

        for i in range(self.combo_box_group.count()):
            if i != current_index and self.combo_box_group.itemText(i) == new_name:
                QMessageBox.warning(self, "警告", "分组名称已存在！")
                self.combo_box_group.lineEdit().setText(original_name)
                return

        if original_name in self.group_data:
            original_data = self.group_data.pop(original_name)
            self.group_data[new_name] = original_data

        self.combo_box_group.setItemText(current_index, new_name)

        if self.current_group == original_name:
            self.current_group = new_name

        self.combo_box_group.setCurrentIndex(current_index)
        self.combo_box_group.currentIndexChanged.connect(self.group_changed)

        if self.current_group is not None:
            self.save_current_group_data()

        QTimer.singleShot(200, self.delayed_auto_save)

    def group_changed(self, index):
        if index < 0:
            self.current_group = None
            self.list_group.clear()
            return

        new_group = self.combo_box_group.currentText()

        if new_group == self.current_group:
            return

        if self.current_group is not None:
            self.save_current_group_data()

        self.current_group = new_group

        self.load_group_data(new_group)

        if self.current_group is not None:
            self.save_current_group_data()

        QTimer.singleShot(200, self.delayed_auto_save)

    def save_current_group_data(self):
        if self.current_group is None:
            return
        
        self.group_data[self.current_group] = []
        
        for i in range(self.list_group.count()):
            item = self.list_group.item(i)

            if not item or not item.data(Qt.UserRole):
                continue

            data_tuple = item.data(Qt.UserRole)
            if data_tuple and len(data_tuple) >= 2:
                self.group_data[self.current_group].append(data_tuple)

    def load_group_data(self, group_name):
        self.list_group.clear()
        
        if group_name not in self.group_data:
            return

        for item_data in self.group_data[group_name]:
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
                list_item_widget = User_ListItemWidget(
                    self.list_group,
                    data_name,
                    data_text,
                    show_all=False,
                    checkable=False,
                    sendable=False
                )

                list_item_widget.set_user_data(clone_item)
                list_item_widget.send_clicked.connect(self.parent.spi_send_item)
                self.list_group.setItemWidget(clone_item, list_item_widget)

        self.list_group.model().rowsInserted.connect(self.list_group_insert)

    def list_group_insert(self, parent, start, end):
        
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
                list_item_widget = User_ListItemWidget(
                    self.list_group,
                    data_name,
                    data_text,
                    show_all=False,
                    checkable=False,
                    sendable=False
                )

                list_item_widget.set_user_data(item)
                list_item_widget.send_clicked.connect(self.parent.spi_send_item)
                self.list_group.setItemWidget(item, list_item_widget)
            if self.current_group is not None:
                self.save_current_group_data()

            QTimer.singleShot(200, self.delayed_auto_save)

    def delayed_auto_save(self):
        if hasattr(self.parent, 'yaml_config'):
            self.parent.yaml_config.auto_save_config()

    def delete_group_item(self):
        selected_items = self.list_group.selectedItems()
        if not selected_items:
            return

        for item in reversed(selected_items):
            row = self.list_group.row(item)
            if row >= 0:
                self.list_group.takeItem(row)

    def get_group_data(self):
        """get group data
        
        Returns:
            dict: contain all group data
        """        
        data = {}
        for i in range(self.combo_box_group.count()):
            group_name = self.combo_box_group.itemText(i)
            if group_name in self.group_data:
                data[group_name] = []
                for item in self.group_data[group_name]:
                    if hasattr(item, 'data') and callable(item.data):
                        data_tuple = item.data(Qt.UserRole)
                        if data_tuple and len(data_tuple) >= 2:
                            data[group_name].append(data_tuple)
                    else:
                        data[group_name].append(item)
        
        return data
        
    def set_group_data(self, group_data):
        """set group data
        
        Args:
            group_data (dict): contain all group data
        """
        self.group_data = group_data
        self.combo_box_group.clear()

        group_names = list(self.group_data.keys())
        for group_name in group_names:
            self.combo_box_group.addItem(group_name)

        if group_data:
            first_group = next(iter(group_data.keys()))
            self.current_group = first_group
            self.combo_box_group.setCurrentText(first_group)
            self.load_group_data(first_group)