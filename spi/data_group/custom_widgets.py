#!/usr/bin/env python3.13
"""
filename: custom_widgets.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-10-13
description: user_defined widgets.
"""
from PySide6.QtWidgets import (
        QWidget, QHBoxLayout, QCheckBox, QLabel, 
        QPushButton
    )
from PySide6.QtCore import Signal, Qt

class User_ListItemWidget(QWidget):
    """
    Custom list item widget with checkbox, text label and send button.
    
    Signals:
        send_clicked: Emitted when the send button is clicked, contains user data.
        check_state_changed: Emitted when the checkbox state changes, contains user data and new state.
    """

    send_clicked = Signal(object)
    check_state_changed = Signal(object, int)

    def __init__(self, parent=None, data_name="", data_text="", show_all=False, checkable=True, sendable=True):
        super().__init__(parent)

        self.init_ui(data_name, data_text, show_all, checkable, sendable)

    def init_ui(self, data_name, data_text, show_all, checkable, sendable):
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(5, 2, 10, 2)
        
        if checkable:
            self.check_box = QCheckBox(self)
            self.check_box.setChecked(False)
            self.h_layout.addWidget(self.check_box)
            self.check_box.stateChanged.connect(self.on_check_state_changed)
        else:
            self.check_box = None

        # # Text label style
        # if show_all:
        #     self.text_label = QLabel(f"{data_name}:         {data_text}", self)
        # else:
        #     self.text_label = QLabel(f"{data_name}", self)

        self.name_text = QLabel(f"{data_name}")
        self.name_text.setMaximumWidth(200)
        self.name_text.setMinimumWidth(200)
        self.name_text.setMaximumHeight(50)
        self.name_text.setStyleSheet("color: #696969; font-weight: normal; font-size: 16px;")
        self.name_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Ignore long text 
        self.name_text.setWordWrap(False)
        self.name_text.setTextFormat(Qt.PlainText)
        self.name_text.setTextInteractionFlags(Qt.NoTextInteraction)

        self.h_layout.addWidget(self.name_text)

        self.data_text = QLabel(f"{data_text}")
        self.data_text.setMinimumWidth(100)
        self.data_text.setStyleSheet("font-size: 16px;")

        if show_all:
            self.h_layout.addWidget(self.data_text)

        # self.text_label.setMinimumWidth(400)
        # self.text_label.setStyleSheet("font-size: 16px;")
        # self.h_layout.addWidget(self.text_label)

        self.h_layout.addStretch()

        if sendable:
            self.send_button = QPushButton("发送", self)
            self.send_button.setFixedSize(80, 25)
            self.send_button.setStyleSheet("""
                background-color: #abc9de;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            """)

            self.send_button.clicked.connect(self.on_send_clicked)

            self.h_layout.addWidget(self.send_button)
        else:
            self.send_button = None

    def on_send_clicked(self):
        self.send_clicked.emit(getattr(self, 'user_data', None))
    
    def on_check_state_changed(self, state):
        self.check_state_changed.emit(getattr(self, 'user_data', None), state)
    
    def set_user_data(self, data):
        """Set custom user data to associate with the widget.

        This method stores user data within the widget instance, establishing
        connection between the UI component and the application's data model.

        Args:
            data: The data object to be associated with this widget. In the SPI tool
                application, this typically contains the QListWidgetItem that holds
                the actual data name and content.
        """ 

        self.user_data = data