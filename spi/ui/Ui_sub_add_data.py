# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_add_data.ui'
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

class Ui_SubForm_Data(object):
    def setupUi(self, SubForm_Data):
        if not SubForm_Data.objectName():
            SubForm_Data.setObjectName(u"SubForm_Data")
        SubForm_Data.resize(304, 209)
        self.gridLayout = QGridLayout(SubForm_Data)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(SubForm_Data)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label_name = QLabel(self.splitter)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_name.setFont(font)
        self.splitter.addWidget(self.label_name)
        self.line_name = QLineEdit(self.splitter)
        self.line_name.setObjectName(u"line_name")
        self.line_name.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setPointSize(14)
        self.line_name.setFont(font1)
        self.splitter.addWidget(self.line_name)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.splitter_2 = QSplitter(SubForm_Data)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.label_text = QLabel(self.splitter_2)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMinimumSize(QSize(0, 50))
        self.label_text.setFont(font)
        self.splitter_2.addWidget(self.label_text)
        self.line_text = QLineEdit(self.splitter_2)
        self.line_text.setObjectName(u"line_text")
        self.line_text.setMinimumSize(QSize(0, 50))
        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(14)
        self.line_text.setFont(font2)
        self.splitter_2.addWidget(self.line_text)

        self.gridLayout.addWidget(self.splitter_2, 1, 0, 1, 1)

        self.splitter_3 = QSplitter(SubForm_Data)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.button_data_confirm = QPushButton(self.splitter_3)
        self.button_data_confirm.setObjectName(u"button_data_confirm")
        self.button_data_confirm.setMinimumSize(QSize(0, 50))
        font3 = QFont()
        font3.setPointSize(12)
        self.button_data_confirm.setFont(font3)
        self.splitter_3.addWidget(self.button_data_confirm)
        self.button_data_cancel = QPushButton(self.splitter_3)
        self.button_data_cancel.setObjectName(u"button_data_cancel")
        self.button_data_cancel.setMinimumSize(QSize(0, 50))
        self.button_data_cancel.setFont(font3)
        self.splitter_3.addWidget(self.button_data_cancel)

        self.gridLayout.addWidget(self.splitter_3, 2, 0, 1, 1)


        self.retranslateUi(SubForm_Data)

        QMetaObject.connectSlotsByName(SubForm_Data)
    # setupUi

    def retranslateUi(self, SubForm_Data):
        SubForm_Data.setWindowTitle(QCoreApplication.translate("SubForm_Data", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u540d\u79f0", None))
        self.line_name.setText("")
        self.label_text.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u5185\u5bb9", None))
        self.button_data_confirm.setText(QCoreApplication.translate("SubForm_Data", u"\u786e\u8ba4", None))
        self.button_data_cancel.setText(QCoreApplication.translate("SubForm_Data", u"\u53d6\u6d88", None))
    # retranslateUi

