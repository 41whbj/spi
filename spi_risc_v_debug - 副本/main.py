#!/usr/bin/env python3.13
"""
filename: main.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-22
description: Qt SPI tool 
"""

import sys
from PySide6.QtWidgets import QApplication
from core.applicaton import Applicaton
from PySide6.QtCore import Qt

if __name__ == '__main__':

    # 控制缩放比例
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    window = Applicaton()
    window.show()
    sys.exit(app.exec())