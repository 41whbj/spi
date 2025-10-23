#!/usr/bin/env python3.13
"""
filename: case_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-02
description: Package as "item" and add it to the list_case.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Signal, Qt
from .frame import Frame, CMD

class CaseID_Manager:
    def __init__(self):
        self.processed_case = {}
    
    def assign_id(self, case_list):

        # Assign ID to each case, ID incrementally
        for index, case in enumerate(case_list):
            hex_id = (index + 1).to_bytes(2, byteorder='big')
            self.processed_case[case] = hex_id

    def get_processed_case(self):
        if self.processed_case:
            return self.processed_case
        else:
            return None
    def clear_processed_case(self):
        """
            Clear processed case
        """
        self.processed_case.clear()
        
class CasePackage:
    def __init__(self):
        self.CMD = CMD

    def package_frame(self, case_id, payload, use_crc):
        """
        pack case id and payload into a frame
        
        Args:
            case_id (bytes)
            payload (bytes)
            
        Returns:
            bytearray: packaged frame
        """

        run_case_data = bytearray()
        run_case_data.extend(case_id)
        run_case_data.extend(payload)

        packaged_frame = Frame.generate_frame(
            cmd=self.CMD["RunCase"],
            data=run_case_data,
            use_crc=use_crc
        )

        return packaged_frame


class CaseItemWidget(QWidget):
    # Send signal when click the send button
    send_frame = Signal(bytearray, bool)  # (packaged_frame)
    
    def __init__(self, name="", id=b"", use_crc=True, mode="send", parent=None):
        super().__init__(parent)
        self.name = name
        self.id = id
        self.use_crc = use_crc
        self.mode = mode
        self.init_ui()
        
    def init_ui(self, button = True, delay = False):
        # Create Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # left：name
        self.name_text = QLabel(self.name)
        self.name_text.setMinimumWidth(80)
        self.name_text.setMaximumHeight(35)
        self.name_text.setStyleSheet("color: #696969; font-weight: normal; font-size: 14px;")
        self.name_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.name_text, 2)

        # Ignore long text 
        self.name_text.setWordWrap(False)
        self.name_text.setTextFormat(Qt.PlainText)
        self.name_text.setTextInteractionFlags(Qt.NoTextInteraction)
        
        # middle：input(payload)
        self.input_payload = QLineEdit()
        self.input_payload.setMinimumWidth(60)
        self.input_payload.setPlaceholderText("请输入负载数据...")
        layout.addWidget(self.input_payload, 1)

        if self.mode == "send":
            # right：button
            self.send_button = QPushButton("发送")
            self.send_button.setMinimumSize(60, 25)
            self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
            
            # connect signal
            self.send_button.clicked.connect(self.send_clicked)
            layout.addWidget(self.send_button, 1)

        else: 

            # right: input delay to continue the time between send and receive
            self.delay_input = QLineEdit()
            self.delay_input.setMinimumWidth(50)
            self.delay_input.setPlaceholderText("发送延时(s)")
            layout.addWidget(self.delay_input, 1)

        layout.addStretch()
        self.setLayout(layout)

    # Create a frame and send it when click the send button
    def send_clicked(self):
        # Get the payload from the input
        input_text = self.input_payload.text()
        if input_text.isdigit() is False:
            self.send_frame.emit(b"", False)
            print(f"input_text: {input_text}")
            return

        if input_text == "":
            decimal_value = 0
        else:
            decimal_value = int(input_text)

        hex_string = f"{decimal_value:X}"
        if len(hex_string) % 2 != 0:
            hex_string = "0" + hex_string
        payload = bytes.fromhex(hex_string)
        frame = CasePackage().package_frame(self.id, payload, use_crc=self.use_crc)
        self.send_frame.emit(frame, True)

# if __name__ == "__main__":
#     case_manager = CaseID_Manager()
#     case_manager.assign_id(['Case1', 'Case2', 'Case3'])
#     print(case_manager.get_processed_case())
