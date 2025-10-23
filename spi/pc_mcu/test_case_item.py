#!/usr/bin/env python3.13
"""
filename: test_case_item.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-4
description: 测试CaseItemWidget的简单应用程序
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from .case_manager import CaseItemWidget, CaseID_Manager

class TestCaseItemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CaseItemWidget 测试")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建QListWidget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # 添加测试项
        self.add_test_items()
        
    def add_test_items(self):
        """添加一些测试项到列表中"""
        # 创建几个测试用的CaseItemWidget

        case_list = "Case1;Case2;Case3;"
    
        Case_Manager = CaseID_Manager()

        Case_Manager.assign_id(case_list)
        processed_case = Case_Manager.get_processed_case()

        if processed_case is None:
            print("没有处理任何case")
            return

        print(processed_case)
        
        for name, id_bytes in processed_case.items():
            # 创建自定义控件
            case_item = CaseItemWidget(name, id_bytes)
            
            # 连接发送信号
            case_item.send_frame.connect(self.handle_send_clicked)
            
            # 创建QListWidgetItem并设置自定义控件
            list_item = QListWidgetItem()
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, case_item)
            
            # 设置项的高度
            list_item.setSizeHint(case_item.sizeHint())
            
    def handle_send_clicked(self, frame_data, correct):
        """处理发送按钮点击事件"""
        if correct is True:
            print("发送请求:")
            print(f"  数据帧: {frame_data.hex()}")
        else:
            QMessageBox.warning(self, "输入错误", "请输入有效的负载。")
        
        # 在实际应用中，这里会添加发送数据到SPI设备的代码

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestCaseItemWindow()
    window.show()
    sys.exit(app.exec())