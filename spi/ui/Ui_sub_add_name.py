# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_add_name.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSplitter, QWidget)

class Ui_SubForm_Name(object):
    def setupUi(self, SubForm_Name):
        if not SubForm_Name.objectName():
            SubForm_Name.setObjectName(u"SubForm_Name")
        SubForm_Name.resize(300, 111)
        self.gridLayout_2 = QGridLayout(SubForm_Name)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(SubForm_Name)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label_name = QLabel(self.splitter)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(11)
        self.label_name.setFont(font)
        self.splitter.addWidget(self.label_name)
        self.line_input = QLineEdit(self.splitter)
        self.line_input.setObjectName(u"line_input")
        self.line_input.setMinimumSize(QSize(0, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.line_input.setFont(font1)
        self.splitter.addWidget(self.line_input)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)

        self.button_name_confirm = QPushButton(SubForm_Name)
        self.button_name_confirm.setObjectName(u"button_name_confirm")
        self.button_name_confirm.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.button_name_confirm, 1, 0, 1, 1)

        self.button_name_cancel = QPushButton(SubForm_Name)
        self.button_name_cancel.setObjectName(u"button_name_cancel")
        self.button_name_cancel.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.button_name_cancel, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(SubForm_Name)

        QMetaObject.connectSlotsByName(SubForm_Name)
    # setupUi

    def retranslateUi(self, SubForm_Name):
        SubForm_Name.setWindowTitle(QCoreApplication.translate("SubForm_Name", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("SubForm_Name", u"\u540d\u79f0", None))
        self.button_name_confirm.setText(QCoreApplication.translate("SubForm_Name", u"\u786e\u5b9a", None))
        self.button_name_cancel.setText(QCoreApplication.translate("SubForm_Name", u"\u53d6\u6d88", None))
    # retranslateUi

