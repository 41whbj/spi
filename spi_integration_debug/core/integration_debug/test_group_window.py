#!/usr/bin/env python3.13
"""
filename: test_group_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-15
description: 测试数据组窗口类，和主程序界面交互
"""

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,QPushButton, QHeaderView,QWidget,QHBoxLayout
)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from .test_group_manager import TestGroupManager

class TestGroupWindow(QObject):
    """
    测试数据组窗口类，和主程序界面交互
    """

    def __init__(self, application, spi_controller):
        """
        初始化测试数据组窗口
        
        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.spi_controller = spi_controller

        self.test_group_manager = TestGroupManager(self.application,spi_controller)

        self.send_mode_thread = self.test_group_manager.send_mode_thread
        self.log = self.application.log_window

        # 使按钮不可见但仍占据空间
        self.ui.button_start.setVisible(True)
        self.ui.button_start.setEnabled(False)
        self.ui.button_start.setStyleSheet("QPushButton { background-color: transparent; color: transparent; border: none; }")

        self.setup_connections()
        self.init_widget()

        self.ui.line_delay.setPlaceholderText("无输入，数据的延时固定为0.5秒")

    # ==================== UI初始化功能 ====================
    
    def init_widget(self):
        """
        初始化界面组件
        """

        # 设置列表控件为2列，分别为组名和数据
        self.ui.tree_group.setColumnCount(2)
        self.ui.tree_group.setHeaderLabels(["测试组", "数据"])
        self.ui.tree_group.setColumnWidth(0, 130)  # 第一列宽度

        # 限制列宽拖拽调整范围，允许拖拽20个像素宽度
        header = self.ui.tree_group.header()
        # 设置第一列的最小和最大宽度
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # 允许交互调整
        header.setMinimumSectionSize(110)# 最小宽度
        header.resizeSection(0, 130)
        # 设置第一列的最大宽度
        header.setMaximumSectionSize(160)# 最大宽度
        
        # 设置第二列不可编辑
        self.ui.tree_group.setColumnEditable(1, False)

        # 设置拖拽模式为内部移动
        self.ui.tree_group.setDragDropMode(QAbstractItemView.InternalMove)

        # 设置选择模式为单选
        self.ui.tree_group.setSelectionMode(QAbstractItemView.SingleSelection)

        # 设置选择行为为选择整行
        self.ui.tree_group.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 禁用拖拽覆盖模式
        self.ui.tree_group.setDragDropOverwriteMode(False)

        # 设置缩进为0，防止放置嵌套
        self.ui.tree_group.setIndentation(0)
        
        # 启用接收拖拽
        self.ui.tree_group.setAcceptDrops(True)
        
        # 连接拖拽事件
        self.ui.tree_group.setDragDropOverwriteMode(False)

        self.ui.tree_group.itemDoubleClicked.connect(self.item_clicked)

        # 连接项编辑完成事件
        self.ui.tree_group.itemChanged.connect(self.test_group_manager.test_group_item_changed)

        self.ui.tree_group.currentItemChanged.connect(lambda current, previous: QTimer.singleShot(0, self.item_moved))

        # 添加调试信息
        # print("已连接rowsMoved信号")

    # ==================== 信号处理功能 ====================

    def setup_connections(self):
        """
        设置信号槽连接
        """

        self.ui.button_del_test_group.clicked.connect(self.test_group_manager.delete_item)
        self.ui.button_add_test_group.clicked.connect(self.test_group_manager.add_test_group)

        # self.ui.combo_box_mode_group.currentIndexChanged.connect(self.group_changed)

        self.ui.button_start.clicked.connect(self.sending_mode)
        self.ui.button_stop.clicked.connect(self.test_group_manager.stop_sending_mode)

        self.ui.check_box_mode_poll.stateChanged.connect(self.tooltip_change)
        self.ui.check_box_mode_poll.stateChanged.connect(self.hide_button_start)

        # 连接全选复选框
        self.ui.check_box_select_all.stateChanged.connect(self.select_all_changed)

    # ==================== 数据组交互功能 ====================

    def item_clicked(self, item):
        """
        处理测试组列表项点击事件，更新当前选中的测试组
        """
        # 确保点击的是父项
        if item.parent() is None:
            self.test_group_manager.current_group = item.text(0)

        if item.childCount() > 0:  # 只有当项有子项时才执行
            # 获取sender
            pos = QCursor.pos()
            # 获取当前鼠标位置
            local_pos = self.ui.tree_group.viewport().mapFromGlobal(pos)
            
            # 如果点击位置在第一列的左侧（勾选框区域），不执行展开/收起
            if local_pos.x() > 20:  # 假设勾选框和空白区域大约占用20像素
                if item.isExpanded():
                    item.setExpanded(False)  # 收起子项
                else:
                    item.setExpanded(True)    # 展开子项

    def item_moved(self):
        """
        处理测试组或者移动事件，更新内部数据结构以反映新的顺序

        移动测试组，更新test_group_manager中的测试组顺序，
        如果测试组有数据项，数据项需要跟着测试组移动，
        
        如果移动的数据项，需要更新测试组中数据项。
        """

        # print('检查是否触发了test_group_moved信号')

        # 重新构建test_group_manager以匹配UI中的新顺序
        new_group_data = {}

        # 遍历UI中的所有顶级项（测试组）
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            group_name = item.text(0)
            
            # 将其添加到新字典中
            new_group_data[group_name] = self.test_group_manager.test_group_manager[group_name]

        self.test_group_manager.test_group_manager = new_group_data

        # print(f"移动后的测试组: {self.test_group_manager.test_group_manager}")

        # 对于数据项的移动，需要检查每个测试组的子项
        for group_name in self.test_group_manager.test_group_manager:
            # 获取对应的UI项
            group_item = self.test_group_manager.find_group_item(group_name)
            
            # 如果找不到group_item，跳过处理
            if group_item is None:
                continue

            # 重新构建该组的数据项列表以匹配UI顺序
            new_item_list = []
            for i in range(group_item.childCount()):
                child_item = group_item.child(i)
                item_data = child_item.data(0, Qt.UserRole)
                
                # 只有当item_data存在时才添加到列表中
                if item_data is not None:
                    new_item_list.append(item_data)

            # 更新该组的数据项列表
            self.test_group_manager.test_group_manager[group_name] = new_item_list

        # 重新为所有顶级项设置按钮widget（解决拖拽后按钮消失的问题）
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            # 检查是否已经设置了widget
            existing_widget = self.ui.tree_group.itemWidget(item, 1)
            if existing_widget is None:
                # 重新创建并设置按钮widget
                self.create_button_widget(item)

        self.application.yaml_window.update_test_group()

    # ==================== 按钮组件功能 ====================

    def create_button_widget(self, item):
        """
        为指定的QTreeWidgetItem创建并设置按钮widget
        
        Args:
            item (QTreeWidgetItem): 覜设置按钮的项目
        """
        # 创建一个widget来容纳按钮，确保更好的显示效果
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(5, 0, 5, 0)  # 设置适当的边距
        button_layout.setSpacing(0)
        
        # 创建按钮
        send_button = QPushButton("发送")
        send_button.setFixedSize(60, 25)
        send_button.setStyleSheet("font-size: 10px;")
        
        # 将按钮添加到布局中
        button_layout.addWidget(send_button)
        button_layout.setAlignment(Qt.AlignLeft)
        
        # 连接按钮点击事件
        send_button.clicked.connect(lambda checked, name=item._original_name: self.test_group_manager.send_button_clicked(name))
        
        # 设置item widget
        self.ui.tree_group.setItemWidget(item, 1, button_widget)
        
        # 确保按钮可见
        button_widget.show()

    # ==================== 发送模式功能 ====================

    def tooltip_change(self):
        """
        根据勾选框状态，改变行号输入框的提示信息
        """
        if self.ui.check_box_mode_poll.isChecked():
            self.ui.line_delay.setPlaceholderText("无输入，组间延迟为0.5秒")
        else:
            self.ui.line_delay.setPlaceholderText("无输入，数据延时为0.5秒")
        
        self.ui.line_number.setPlaceholderText("无输入，一直发送，直到停止")

    def hide_button_start(self):
        """
        正常发送模式下的开始按钮隐藏
        """
        if self.ui.check_box_mode_poll.isChecked():
            self.ui.button_start.setVisible(True)
            self.ui.button_start.setEnabled(True)
            # 恢复按钮的原始样式
            self.ui.button_start.setStyleSheet("")
        else:
            # 使按钮不可见但仍占据空间
            self.ui.button_start.setVisible(True)
            self.ui.button_start.setEnabled(False)
            self.ui.button_start.setStyleSheet("QPushButton { background-color: transparent; color: transparent; border: none; }")

    def sending_mode(self):
        """
        全局发送模式：根据选定的模式发送所有勾选组的数据
        """
        # 调用TestGroupManager中的sending_mode方法
        self.test_group_manager.sending_mode(is_global_mode=True)

    # ==================== 选择控制功能 ====================

    def select_all_changed(self, state):
        """
        处理全选复选框状态变化
        
        Args:
            state: 复选框的状态 (Qt.Checked 或 Qt.Unchecked)
        """
        # 如果正在更新选择状态，避免循环触发
        if self.test_group_manager.updating_selection:
            return

        # 如果tree_group中没有项，直接返回
        if self.ui.tree_group.topLevelItemCount() == 0:
            return
        
        # 遍历所有顶级项（测试组）
        for i in range(self.ui.tree_group.topLevelItemCount()):
            item = self.ui.tree_group.topLevelItem(i)
            # 根据全选复选框的状态设置每个测试组的勾选状态
            if state == 2:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)

    def update_select_all_state(self):
        """
        更新全选复选框的状态
        当某个item的勾选状态改变时调用此方法来更新全选复选框的状态
        """
        # 设置标志以避免循环触发
        self.test_group_manager.updating_selection = True
        
        try:
            # 如果没有项，直接返回并将全选复选框设为未选中
            if self.ui.tree_group.topLevelItemCount() == 0:
                self.ui.check_box_select_all.setChecked(False)
                return
            
            # 检查是否所有项都被选中
            all_checked = True
            for i in range(self.ui.tree_group.topLevelItemCount()):
                item = self.ui.tree_group.topLevelItem(i)
                if item.checkState(0) != Qt.Checked:
                    all_checked = False
                    break
            
            # 更新全选复选框的状态
            self.ui.check_box_select_all.setChecked(all_checked)
        finally:
            # 重置标志
            self.test_group_manager.updating_selection = False