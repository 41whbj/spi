#!/usr/bin/env python3.13
"""
filename: data_widget.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-26
description: 用户定义主窗口的SPI数据控件。
"""
from PySide6.QtWidgets import (
        QWidget, QHBoxLayout, QCheckBox, QLabel, 
        QPushButton, QLineEdit
    )
from PySide6.QtCore import Signal, Qt

class Data_Widget(QWidget):
    """
        自定义列表项小部件，包含复选框、文本标签和发送按钮。
        
        Signals:
            send_clicked_signal: 点击发送按钮时触发，包含用户数据。
            check_changed_signal: 复选框状态改变时触发，包含用户数据和新状态。
            data_changed_signal: 文本编辑框内容改变时触发，包含用户数据和新文本。
    """

    send_clicked_signal = Signal(object)
    add_clicked_signal = Signal(object)
    check_changed_signal = Signal(object, int)
    data_changed_signal = Signal(object, str)

    def __init__(
            self, 
            parent=None, 
            data_name="", 
            data_text="", 
            show_all=False, 
            checkable=True, 
            sendable=True,
            add_able=True
        ):
        """初始化SPI数据控件.

        Args:
            parent: 父级窗口部件
            data_name (str): 数据名称
            data_text (str): 数据文本
            show_all (bool): 是否显示为可编辑文本框
            checkable (bool): 是否包含复选框
            sendable (bool): 是否包含发送按钮
        """
        super().__init__(parent)

        self.data_name = data_name
        self.data_text = data_text

        self.init_ui(show_all, checkable, sendable, add_able)

    def init_ui(self, show_all, checkable, sendable, add_able=True):
        """初始化用户界面组件.

        Args:
            data_name (str): 数据名称，显示在标签上
            data_text (str): 数据文本内容
            show_all (bool): 是否显示为可编辑文本框
            checkable (bool): 是否包含复选框
            sendable (bool): 是否包含发送按钮
        """

        # 创建水平布局并设置边距
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(5, 2, 10, 2)
        
         # 根据checkable参数决定是否添加复选框
        if checkable:
            self.check_box = QCheckBox(self)
            self.check_box.setChecked(False)
            self.h_layout.addWidget(self.check_box)
            self.check_box.stateChanged.connect(self.check_state_changed)
        elif add_able:
            self.add_button = QPushButton("添加", self)
            self.add_button.setFixedSize(50, 25)
            self.add_button.setStyleSheet("""
                font-size: 11px;
            """)
            self.h_layout.addWidget(self.add_button)
            self.add_button.clicked.connect(self.add_clicked)
        else:
            self.check_box = None

        # 创建名称标签并设置样式
        self.name_text = QLabel(f"{self.data_name}")
        self.name_text.setMaximumWidth(300)
        self.name_text.setMinimumWidth(200)
        self.name_text.setMaximumHeight(50)
        self.name_text.setStyleSheet("color: #696969; font-weight: normal; font-size: 16px;")
        self.name_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 设置文本标签属性：禁用自动换行、纯文本格式、禁止文本交互
        self.name_text.setWordWrap(False)
        self.name_text.setTextFormat(Qt.PlainText)
        self.name_text.setTextInteractionFlags(Qt.NoTextInteraction)

        # 将名称标签添加到布局中
        self.h_layout.addWidget(self.name_text)

         # 根据show_all参数决定显示可编辑文本框还是只读标签
        if show_all:
            self.data_text = QLineEdit(f"{self.data_text}")
            self.data_text.setMinimumWidth(100)
            self.data_text.setStyleSheet("font-size: 16px;")
            self.h_layout.addWidget(self.data_text)
            self.data_text.editingFinished.connect(self.edit_finish)
        else:
            self.data_label = QLabel(f"{self.data_text}")
            self.data_label.setMinimumWidth(100)
            self.data_label.setStyleSheet("font-size: 16px;")
            self.h_layout.addWidget(self.data_label)

        # 添加弹性空间以填充剩余区域
        self.h_layout.addStretch()

        # 根据sendable参数决定是否添加发送按钮
        if sendable:
            self.send_button = QPushButton("发送", self)
            self.send_button.setFixedSize(80, 25)
            self.send_button.setStyleSheet("""
                background-color: #00BFFF;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            """)

            self.send_button.clicked.connect(self.send_clicked)

            self.h_layout.addWidget(self.send_button)

        else:
            self.send_button = None

    def send_clicked(self):
        """处理发送按钮点击事件."""
        self.send_clicked_signal.emit(getattr(self, 'user_data', None))
    
    def check_state_changed(self, state):
        """处理复选框状态改变事件.

        Args:
            state (int): 复选框的新状态
        """
        self.check_changed_signal.emit(getattr(self, 'user_data', None), state)

    def edit_finish(self):
        """处理文本编辑完成事件."""
        text = self.data_text.text().strip()

        # 只保留十六进制字符
        clean_text = ''.join(c for c in text if c in '0123456789ABCDEFabcdef')
        
        if not clean_text:
            return ""
        
        # 如果字符数为奇数，在前面补0
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # 格式化显示，每两个字符之间添加空格
        formatted_text = ' '.join(clean_text[i:i+2] for i in range(0, len(clean_text), 2))

        self.data_text.setText(formatted_text)

        self.data_changed_signal.emit(getattr(self, 'user_data', None), formatted_text)
    
    def set_user_data(self, data):
        """设置用户数据.

        Args:
            data: 要存储的用户数据
        """

        self.user_data = data

    def add_clicked(self):
        """处理添加按钮点击事件."""
        # 获取名称和内容数据
        name_data = self.data_name
        content_data = self.data_text.text().strip()
        
        # 创建包含名称和内容的数据字典
        data = {
            'name': name_data,
            'content': content_data
        }
        
        # 发射信号，传递名称和内容数据
        self.add_clicked_signal.emit(data)