#!/usr/bin/env python3.13
"""
filename: __init__.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-10-22
description: Qt SPI tool 
"""

import sys
from PySide6.QtWidgets import QApplication
from controller.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

