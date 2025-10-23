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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSplitter, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_SubForm_Data(object):
    def setupUi(self, SubForm_Data):
        if not SubForm_Data.objectName():
            SubForm_Data.setObjectName(u"SubForm_Data")
        SubForm_Data.resize(425, 153)
        self.gridLayout_4 = QGridLayout(SubForm_Data)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(SubForm_Data)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font = QFont()
        font.setPointSize(10)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.page_normal = QWidget()
        self.page_normal.setObjectName(u"page_normal")
        self.gridLayout_2 = QGridLayout(self.page_normal)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(5)
        self.splitter = QSplitter(self.page_normal)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label_name = QLabel(self.splitter)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_name.setFont(font1)
        self.splitter.addWidget(self.label_name)
        self.line_name = QLineEdit(self.splitter)
        self.line_name.setObjectName(u"line_name")
        self.line_name.setMinimumSize(QSize(0, 40))
        font2 = QFont()
        font2.setPointSize(14)
        self.line_name.setFont(font2)
        self.splitter.addWidget(self.line_name)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.splitter_2 = QSplitter(self.page_normal)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.label_text = QLabel(self.splitter_2)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMinimumSize(QSize(0, 40))
        self.label_text.setFont(font1)
        self.splitter_2.addWidget(self.label_text)
        self.line_text = QLineEdit(self.splitter_2)
        self.line_text.setObjectName(u"line_text")
        self.line_text.setMinimumSize(QSize(0, 40))
        font3 = QFont()
        font3.setFamilies([u"Times New Roman"])
        font3.setPointSize(14)
        self.line_text.setFont(font3)
        self.splitter_2.addWidget(self.line_text)

        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 1)

        self.splitter_3 = QSplitter(self.page_normal)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.button_data_confirm = QPushButton(self.splitter_3)
        self.button_data_confirm.setObjectName(u"button_data_confirm")
        self.button_data_confirm.setMinimumSize(QSize(0, 40))
        font4 = QFont()
        font4.setPointSize(12)
        self.button_data_confirm.setFont(font4)
        self.splitter_3.addWidget(self.button_data_confirm)
        self.button_data_cancel = QPushButton(self.splitter_3)
        self.button_data_cancel.setObjectName(u"button_data_cancel")
        self.button_data_cancel.setMinimumSize(QSize(0, 40))
        self.button_data_cancel.setFont(font4)
        self.splitter_3.addWidget(self.button_data_cancel)

        self.gridLayout.addWidget(self.splitter_3, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_normal)
        self.page_quick_command = QWidget()
        self.page_quick_command.setObjectName(u"page_quick_command")
        self.gridLayout_3 = QGridLayout(self.page_quick_command)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.page_quick_command)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.line_head = QLineEdit(self.page_quick_command)
        self.line_head.setObjectName(u"line_head")
        self.line_head.setMinimumSize(QSize(60, 35))
        self.line_head.setMaximumSize(QSize(16777215, 16777215))
        self.line_head.setFont(font)

        self.verticalLayout.addWidget(self.line_head)


        self.gridLayout_3.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.label_2 = QLabel(self.page_quick_command)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.line_ddr = QLineEdit(self.page_quick_command)
        self.line_ddr.setObjectName(u"line_ddr")
        self.line_ddr.setMinimumSize(QSize(60, 35))
        self.line_ddr.setMaximumSize(QSize(16777215, 16777215))
        self.line_ddr.setFont(font)

        self.verticalLayout_2.addWidget(self.line_ddr)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.page_quick_command)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_3.addWidget(self.label_3)

        self.line_data1 = QLineEdit(self.page_quick_command)
        self.line_data1.setObjectName(u"line_data1")
        self.line_data1.setMinimumSize(QSize(60, 34))
        self.line_data1.setMaximumSize(QSize(16777215, 16777215))
        self.line_data1.setFont(font)

        self.verticalLayout_3.addWidget(self.line_data1)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 1, 2, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.page_quick_command)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(94, 0))
        self.label_4.setFont(font)

        self.verticalLayout_4.addWidget(self.label_4)

        self.line_data2 = QLineEdit(self.page_quick_command)
        self.line_data2.setObjectName(u"line_data2")
        self.line_data2.setMinimumSize(QSize(60, 34))
        self.line_data2.setMaximumSize(QSize(16777215, 16777215))
        self.line_data2.setFont(font)

        self.verticalLayout_4.addWidget(self.line_data2)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 3, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.page_quick_command)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(60, 40))

        self.horizontalLayout_2.addWidget(self.label_6)

        self.line_input = QLineEdit(self.page_quick_command)
        self.line_input.setObjectName(u"line_input")
        self.line_input.setMinimumSize(QSize(50, 40))
        self.line_input.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.line_input)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.button_add = QPushButton(self.page_quick_command)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(69, 40))
        self.button_add.setMaximumSize(QSize(16777215, 16777215))
        self.button_add.setFont(font)

        self.gridLayout_3.addWidget(self.button_add, 2, 2, 1, 2)

        self.config = QWidget(self.page_quick_command)
        self.config.setObjectName(u"config")
        self.horizontalLayout_3 = QHBoxLayout(self.config)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_lane = QLabel(self.config)
        self.label_lane.setObjectName(u"label_lane")
        self.label_lane.setMinimumSize(QSize(35, 0))
        font5 = QFont()
        font5.setPointSize(9)
        self.label_lane.setFont(font5)

        self.horizontalLayout_3.addWidget(self.label_lane)

        self.comb_box_lane = QComboBox(self.config)
        self.comb_box_lane.addItem("")
        self.comb_box_lane.addItem("")
        self.comb_box_lane.setObjectName(u"comb_box_lane")
        self.comb_box_lane.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.comb_box_lane)

        self.label_color_depth = QLabel(self.config)
        self.label_color_depth.setObjectName(u"label_color_depth")
        self.label_color_depth.setMinimumSize(QSize(30, 0))
        self.label_color_depth.setFont(font5)

        self.horizontalLayout_3.addWidget(self.label_color_depth)

        self.comb_box_color_depth = QComboBox(self.config)
        self.comb_box_color_depth.addItem("")
        self.comb_box_color_depth.addItem("")
        self.comb_box_color_depth.setObjectName(u"comb_box_color_depth")
        self.comb_box_color_depth.setMinimumSize(QSize(70, 25))

        self.horizontalLayout_3.addWidget(self.comb_box_color_depth)

        self.label_ppl = QLabel(self.config)
        self.label_ppl.setObjectName(u"label_ppl")
        self.label_ppl.setMinimumSize(QSize(50, 0))
        self.label_ppl.setMaximumSize(QSize(16777215, 16777215))
        self.label_ppl.setFont(font5)

        self.horizontalLayout_3.addWidget(self.label_ppl)

        self.comb_box_width = QComboBox(self.config)
        self.comb_box_width.addItem("")
        self.comb_box_width.addItem("")
        self.comb_box_width.addItem("")
        self.comb_box_width.setObjectName(u"comb_box_width")
        self.comb_box_width.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.comb_box_width)

        self.label_x = QLabel(self.config)
        self.label_x.setObjectName(u"label_x")
        self.label_x.setMinimumSize(QSize(10, 0))
        self.label_x.setMaximumSize(QSize(10, 31))
        self.label_x.setFont(font5)

        self.horizontalLayout_3.addWidget(self.label_x)

        self.comb_box_height = QComboBox(self.config)
        self.comb_box_height.addItem("")
        self.comb_box_height.addItem("")
        self.comb_box_height.addItem("")
        self.comb_box_height.setObjectName(u"comb_box_height")
        self.comb_box_height.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.comb_box_height)


        self.gridLayout_3.addWidget(self.config, 0, 0, 1, 4)

        self.stackedWidget.addWidget(self.page_quick_command)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 2, 1)


        self.retranslateUi(SubForm_Data)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SubForm_Data)
    # setupUi

    def retranslateUi(self, SubForm_Data):
        SubForm_Data.setWindowTitle(QCoreApplication.translate("SubForm_Data", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u540d\u79f0", None))
        self.line_name.setText("")
        self.label_text.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u5185\u5bb9", None))
        self.button_data_confirm.setText(QCoreApplication.translate("SubForm_Data", u"\u786e\u8ba4", None))
        self.button_data_cancel.setText(QCoreApplication.translate("SubForm_Data", u"\u53d6\u6d88", None))
        self.label.setText(QCoreApplication.translate("SubForm_Data", u"\u5e27\u5934", None))
        self.line_head.setText(QCoreApplication.translate("SubForm_Data", u"40", None))
        self.label_2.setText(QCoreApplication.translate("SubForm_Data", u"\u5730\u5740", None))
        self.line_ddr.setText(QCoreApplication.translate("SubForm_Data", u"0A", None))
        self.label_3.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u5e271", None))
        self.label_4.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u5e272", None))
        self.label_6.setText(QCoreApplication.translate("SubForm_Data", u"\u5bf9\u6bd4\u5ea6", None))
        self.button_add.setText(QCoreApplication.translate("SubForm_Data", u"\u6dfb\u52a0", None))
        self.label_lane.setText(QCoreApplication.translate("SubForm_Data", u"\u901a\u9053", None))
        self.comb_box_lane.setItemText(0, QCoreApplication.translate("SubForm_Data", u"8", None))
        self.comb_box_lane.setItemText(1, QCoreApplication.translate("SubForm_Data", u"10", None))

        self.label_color_depth.setText(QCoreApplication.translate("SubForm_Data", u"\u8272\u6df1", None))
        self.comb_box_color_depth.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1024", None))
        self.comb_box_color_depth.setItemText(1, QCoreApplication.translate("SubForm_Data", u"256", None))

        self.label_ppl.setText(QCoreApplication.translate("SubForm_Data", u"\u5206\u8fa8\u7387", None))
        self.comb_box_width.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1920", None))
        self.comb_box_width.setItemText(1, QCoreApplication.translate("SubForm_Data", u"2560", None))
        self.comb_box_width.setItemText(2, QCoreApplication.translate("SubForm_Data", u"3840", None))

        self.label_x.setText(QCoreApplication.translate("SubForm_Data", u"x", None))
        self.comb_box_height.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1080", None))
        self.comb_box_height.setItemText(1, QCoreApplication.translate("SubForm_Data", u"1440", None))
        self.comb_box_height.setItemText(2, QCoreApplication.translate("SubForm_Data", u"2160", None))

    # retranslateUi

