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
    QSizePolicy, QSplitter, QStackedWidget, QTextEdit,
    QWidget)

class Ui_SubForm_Data(object):
    def setupUi(self, SubForm_Data):
        if not SubForm_Data.objectName():
            SubForm_Data.setObjectName(u"SubForm_Data")
        SubForm_Data.resize(411, 136)
        self.gridLayout_4 = QGridLayout(SubForm_Data)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.stackedWidget = QStackedWidget(SubForm_Data)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font = QFont()
        font.setPointSize(10)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.page_normal = QWidget()
        self.page_normal.setObjectName(u"page_normal")
        self.gridLayout_2 = QGridLayout(self.page_normal)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
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
        font4.setFamilies([u"\u5b8b\u4f53"])
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
        self.page_formula = QWidget()
        self.page_formula.setObjectName(u"page_formula")
        self.gridLayout_6 = QGridLayout(self.page_formula)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.lineEdit_function = QLineEdit(self.page_formula)
        self.lineEdit_function.setObjectName(u"lineEdit_function")
        self.lineEdit_function.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_function.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineEdit_function, 2, 3, 1, 1)

        self.label_3 = QLabel(self.page_formula)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_5 = QLabel(self.page_formula)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_5, 1, 1, 1, 1)

        self.config = QWidget(self.page_formula)
        self.config.setObjectName(u"config")
        self.horizontalLayout_3 = QHBoxLayout(self.config)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
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


        self.gridLayout_5.addWidget(self.config, 0, 0, 1, 4)

        self.label_8 = QLabel(self.page_formula)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_8, 1, 3, 1, 1)

        self.label_7 = QLabel(self.page_formula)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_7, 1, 2, 1, 1)

        self.lineEdit_head = QLineEdit(self.page_formula)
        self.lineEdit_head.setObjectName(u"lineEdit_head")
        self.lineEdit_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_head.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineEdit_head, 2, 0, 1, 1)

        self.comboBox_address = QComboBox(self.page_formula)
        self.comboBox_address.setObjectName(u"comboBox_address")

        self.gridLayout_5.addWidget(self.comboBox_address, 2, 1, 1, 1)

        self.lineEdit_input = QLineEdit(self.page_formula)
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setEnabled(True)
        self.lineEdit_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_input.setReadOnly(False)

        self.gridLayout_5.addWidget(self.lineEdit_input, 2, 2, 1, 1)

        self.pushButton_add_data = QPushButton(self.page_formula)
        self.pushButton_add_data.setObjectName(u"pushButton_add_data")
        self.pushButton_add_data.setMinimumSize(QSize(0, 0))

        self.gridLayout_5.addWidget(self.pushButton_add_data, 4, 3, 1, 1)

        self.label_9 = QLabel(self.page_formula)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 3, 0, 1, 2)

        self.textEdit_formula = QTextEdit(self.page_formula)
        self.textEdit_formula.setObjectName(u"textEdit_formula")
        self.textEdit_formula.setMaximumSize(QSize(16777215, 25))
        self.textEdit_formula.setReadOnly(True)

        self.gridLayout_5.addWidget(self.textEdit_formula, 4, 0, 1, 3)


        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_formula)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(SubForm_Data)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SubForm_Data)
    # setupUi

    def retranslateUi(self, SubForm_Data):
        SubForm_Data.setWindowTitle(QCoreApplication.translate("SubForm_Data", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u540d\u79f0", None))
        self.line_name.setText("")
        self.label_text.setText(QCoreApplication.translate("SubForm_Data", u"\u6570\u636e\u5185\u5bb9", None))
        self.button_data_confirm.setText(QCoreApplication.translate("SubForm_Data", u"\u786e\u8ba4", None))
        self.button_data_cancel.setText(QCoreApplication.translate("SubForm_Data", u"\u53d6\u6d88", None))
        self.label_3.setText(QCoreApplication.translate("SubForm_Data", u"\u5e27\u5934", None))
        self.label_5.setText(QCoreApplication.translate("SubForm_Data", u"\u5730\u5740", None))
        self.label_lane.setText(QCoreApplication.translate("SubForm_Data", u"\u901a\u9053", None))
        self.comb_box_lane.setItemText(0, QCoreApplication.translate("SubForm_Data", u"2", None))
        self.comb_box_lane.setItemText(1, QCoreApplication.translate("SubForm_Data", u"4", None))
        self.comb_box_lane.setItemText(2, QCoreApplication.translate("SubForm_Data", u"8", None))
        self.comb_box_lane.setItemText(3, QCoreApplication.translate("SubForm_Data", u"16", None))

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

        self.label_8.setText(QCoreApplication.translate("SubForm_Data", u"\u529f\u80fd", None))
        self.label_7.setText(QCoreApplication.translate("SubForm_Data", u"\u8f93\u5165", None))
        self.lineEdit_head.setText(QCoreApplication.translate("SubForm_Data", u"40", None))
        self.pushButton_add_data.setText(QCoreApplication.translate("SubForm_Data", u"\u6dfb\u52a0", None))
        self.label_9.setText(QCoreApplication.translate("SubForm_Data", u"\u8ba1\u7b97\u516c\u5f0f", None))
    # retranslateUi

