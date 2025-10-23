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
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSplitter, QStackedWidget,
    QTextEdit, QWidget)

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
        self.gridLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
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
        font5.setFamilies([u"Times New Roman"])
        font5.setPointSize(10)
        self.label_lane.setFont(font5)
        self.label_lane.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_lane)

        self.lineEdit_lane = QLineEdit(self.config)
        self.lineEdit_lane.setObjectName(u"lineEdit_lane")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_lane.sizePolicy().hasHeightForWidth())
        self.lineEdit_lane.setSizePolicy(sizePolicy)
        self.lineEdit_lane.setFont(font5)
        self.lineEdit_lane.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_lane)

        self.label_color_depth = QLabel(self.config)
        self.label_color_depth.setObjectName(u"label_color_depth")
        self.label_color_depth.setMinimumSize(QSize(30, 0))
        font6 = QFont()
        font6.setFamilies([u"Times New Roman"])
        font6.setPointSize(9)
        self.label_color_depth.setFont(font6)
        self.label_color_depth.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_color_depth)

        self.lineEdit_color_depth = QLineEdit(self.config)
        self.lineEdit_color_depth.setObjectName(u"lineEdit_color_depth")
        sizePolicy.setHeightForWidth(self.lineEdit_color_depth.sizePolicy().hasHeightForWidth())
        self.lineEdit_color_depth.setSizePolicy(sizePolicy)
        self.lineEdit_color_depth.setFont(font5)
        self.lineEdit_color_depth.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_color_depth)

        self.label_ppl = QLabel(self.config)
        self.label_ppl.setObjectName(u"label_ppl")
        self.label_ppl.setMinimumSize(QSize(50, 0))
        self.label_ppl.setMaximumSize(QSize(16777215, 16777215))
        self.label_ppl.setFont(font6)
        self.label_ppl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_ppl)

        self.lineEdit_width = QLineEdit(self.config)
        self.lineEdit_width.setObjectName(u"lineEdit_width")
        sizePolicy.setHeightForWidth(self.lineEdit_width.sizePolicy().hasHeightForWidth())
        self.lineEdit_width.setSizePolicy(sizePolicy)
        self.lineEdit_width.setFont(font5)
        self.lineEdit_width.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_width)

        self.label_x = QLabel(self.config)
        self.label_x.setObjectName(u"label_x")
        self.label_x.setMinimumSize(QSize(10, 0))
        self.label_x.setMaximumSize(QSize(10, 31))
        font7 = QFont()
        font7.setPointSize(9)
        self.label_x.setFont(font7)

        self.horizontalLayout_3.addWidget(self.label_x)

        self.lineEdit_height = QLineEdit(self.config)
        self.lineEdit_height.setObjectName(u"lineEdit_height")
        sizePolicy.setHeightForWidth(self.lineEdit_height.sizePolicy().hasHeightForWidth())
        self.lineEdit_height.setSizePolicy(sizePolicy)
        self.lineEdit_height.setFont(font5)
        self.lineEdit_height.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_height)


        self.gridLayout_5.addWidget(self.config, 0, 0, 1, 4)

        self.pushButton_add_data = QPushButton(self.page_formula)
        self.pushButton_add_data.setObjectName(u"pushButton_add_data")
        sizePolicy.setHeightForWidth(self.pushButton_add_data.sizePolicy().hasHeightForWidth())
        self.pushButton_add_data.setSizePolicy(sizePolicy)
        self.pushButton_add_data.setMinimumSize(QSize(0, 0))
        self.pushButton_add_data.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_add_data.setFont(font5)

        self.gridLayout_5.addWidget(self.pushButton_add_data, 4, 3, 1, 1)

        self.comboBox_address = QComboBox(self.page_formula)
        self.comboBox_address.setObjectName(u"comboBox_address")
        sizePolicy.setHeightForWidth(self.comboBox_address.sizePolicy().hasHeightForWidth())
        self.comboBox_address.setSizePolicy(sizePolicy)

        self.gridLayout_5.addWidget(self.comboBox_address, 2, 0, 1, 1)

        self.label_5 = QLabel(self.page_formula)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 16777215))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_7 = QLabel(self.page_formula)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 16777215))
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_7, 1, 1, 1, 1)

        self.lineEdit_input = QLineEdit(self.page_formula)
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setEnabled(True)
        sizePolicy.setHeightForWidth(self.lineEdit_input.sizePolicy().hasHeightForWidth())
        self.lineEdit_input.setSizePolicy(sizePolicy)
        self.lineEdit_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_input.setReadOnly(False)

        self.gridLayout_5.addWidget(self.lineEdit_input, 2, 1, 1, 3)

        self.textEdit_formula = QTextEdit(self.page_formula)
        self.textEdit_formula.setObjectName(u"textEdit_formula")
        sizePolicy.setHeightForWidth(self.textEdit_formula.sizePolicy().hasHeightForWidth())
        self.textEdit_formula.setSizePolicy(sizePolicy)
        self.textEdit_formula.setMaximumSize(QSize(16777215, 25))
        self.textEdit_formula.setReadOnly(True)

        self.gridLayout_5.addWidget(self.textEdit_formula, 4, 1, 1, 2)

        self.label_9 = QLabel(self.page_formula)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMaximumSize(QSize(16777215, 16777215))
        self.label_9.setFont(font5)

        self.gridLayout_5.addWidget(self.label_9, 4, 0, 1, 1)

        self.label = QLabel(self.page_formula)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setFont(font5)

        self.gridLayout_5.addWidget(self.label, 3, 0, 1, 1)

        self.label_2 = QLabel(self.page_formula)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font5)

        self.gridLayout_5.addWidget(self.label_2, 3, 1, 1, 3)

        self.gridLayout_5.setColumnStretch(0, 2)
        self.gridLayout_5.setColumnStretch(2, 10)

        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_formula)
        self.page_old = QWidget()
        self.page_old.setObjectName(u"page_old")
        self.gridLayout_11 = QGridLayout(self.page_old)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.lineEdit_addr = QLineEdit(self.page_old)
        self.lineEdit_addr.setObjectName(u"lineEdit_addr")
        self.lineEdit_addr.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_addr, 2, 1, 1, 1)

        self.label_14 = QLabel(self.page_old)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_14, 1, 1, 1, 1)

        self.lineEdit_head_ = QLineEdit(self.page_old)
        self.lineEdit_head_.setObjectName(u"lineEdit_head_")
        self.lineEdit_head_.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_head_.setReadOnly(False)

        self.gridLayout_10.addWidget(self.lineEdit_head_, 2, 0, 1, 1)

        self.label_16 = QLabel(self.page_old)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_16, 1, 2, 1, 1)

        self.lineEdit_input_1 = QLineEdit(self.page_old)
        self.lineEdit_input_1.setObjectName(u"lineEdit_input_1")
        self.lineEdit_input_1.setEnabled(True)
        self.lineEdit_input_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_input_1.setReadOnly(False)

        self.gridLayout_10.addWidget(self.lineEdit_input_1, 2, 2, 1, 1)

        self.pushButton_add_data_ = QPushButton(self.page_old)
        self.pushButton_add_data_.setObjectName(u"pushButton_add_data_")
        self.pushButton_add_data_.setMinimumSize(QSize(0, 0))

        self.gridLayout_10.addWidget(self.pushButton_add_data_, 3, 3, 1, 1)

        self.config_3 = QWidget(self.page_old)
        self.config_3.setObjectName(u"config_3")
        self.horizontalLayout_5 = QHBoxLayout(self.config_3)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_lane_ = QLabel(self.config_3)
        self.label_lane_.setObjectName(u"label_lane_")
        self.label_lane_.setMinimumSize(QSize(35, 0))
        self.label_lane_.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_lane_)

        self.comb_box_lane_ = QComboBox(self.config_3)
        self.comb_box_lane_.addItem("")
        self.comb_box_lane_.addItem("")
        self.comb_box_lane_.addItem("")
        self.comb_box_lane_.addItem("")
        self.comb_box_lane_.setObjectName(u"comb_box_lane_")
        self.comb_box_lane_.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_5.addWidget(self.comb_box_lane_)

        self.label_color_depth_ = QLabel(self.config_3)
        self.label_color_depth_.setObjectName(u"label_color_depth_")
        self.label_color_depth_.setMinimumSize(QSize(30, 0))
        self.label_color_depth_.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_color_depth_)

        self.comb_box_color_depth_ = QComboBox(self.config_3)
        self.comb_box_color_depth_.addItem("")
        self.comb_box_color_depth_.addItem("")
        self.comb_box_color_depth_.setObjectName(u"comb_box_color_depth_")
        self.comb_box_color_depth_.setMinimumSize(QSize(70, 25))

        self.horizontalLayout_5.addWidget(self.comb_box_color_depth_)

        self.label_ppl_ = QLabel(self.config_3)
        self.label_ppl_.setObjectName(u"label_ppl_")
        self.label_ppl_.setMinimumSize(QSize(50, 0))
        self.label_ppl_.setMaximumSize(QSize(16777215, 16777215))
        self.label_ppl_.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_ppl_)

        self.comb_box_width_ = QComboBox(self.config_3)
        self.comb_box_width_.addItem("")
        self.comb_box_width_.addItem("")
        self.comb_box_width_.addItem("")
        self.comb_box_width_.setObjectName(u"comb_box_width_")
        self.comb_box_width_.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_5.addWidget(self.comb_box_width_)

        self.label_x_ = QLabel(self.config_3)
        self.label_x_.setObjectName(u"label_x_")
        self.label_x_.setMinimumSize(QSize(10, 0))
        self.label_x_.setMaximumSize(QSize(10, 31))
        self.label_x_.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_x_)

        self.comb_box_height_ = QComboBox(self.config_3)
        self.comb_box_height_.addItem("")
        self.comb_box_height_.addItem("")
        self.comb_box_height_.addItem("")
        self.comb_box_height_.setObjectName(u"comb_box_height_")
        self.comb_box_height_.setMinimumSize(QSize(70, 0))

        self.horizontalLayout_5.addWidget(self.comb_box_height_)


        self.gridLayout_10.addWidget(self.config_3, 0, 0, 1, 4)

        self.label_13 = QLabel(self.page_old)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_13, 1, 0, 1, 1)

        self.lineEdit_input_2 = QLineEdit(self.page_old)
        self.lineEdit_input_2.setObjectName(u"lineEdit_input_2")
        self.lineEdit_input_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_input_2.setReadOnly(False)

        self.gridLayout_10.addWidget(self.lineEdit_input_2, 2, 3, 1, 1)

        self.label_15 = QLabel(self.page_old)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_15, 1, 3, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_old)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 1, 1, 1)


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
        self.label_lane.setText(QCoreApplication.translate("SubForm_Data", u"\u901a\u9053", None))
        self.lineEdit_lane.setText(QCoreApplication.translate("SubForm_Data", u"2", None))
        self.label_color_depth.setText(QCoreApplication.translate("SubForm_Data", u"\u8272\u6df1", None))
        self.lineEdit_color_depth.setText(QCoreApplication.translate("SubForm_Data", u"1024", None))
        self.label_ppl.setText(QCoreApplication.translate("SubForm_Data", u"\u5206\u8fa8\u7387", None))
        self.lineEdit_width.setText(QCoreApplication.translate("SubForm_Data", u"3840", None))
        self.label_x.setText(QCoreApplication.translate("SubForm_Data", u"x", None))
        self.lineEdit_height.setText(QCoreApplication.translate("SubForm_Data", u"1080", None))
        self.pushButton_add_data.setText(QCoreApplication.translate("SubForm_Data", u"\u6dfb\u52a0", None))
        self.label_5.setText(QCoreApplication.translate("SubForm_Data", u"\u529f\u80fd", None))
        self.label_7.setText(QCoreApplication.translate("SubForm_Data", u"\u8f93\u5165", None))
        self.label_9.setText(QCoreApplication.translate("SubForm_Data", u"\u516c\u5f0f", None))
        self.label.setText(QCoreApplication.translate("SubForm_Data", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("SubForm_Data", u"TextLabel", None))
        self.label_14.setText(QCoreApplication.translate("SubForm_Data", u"\u5730\u5740", None))
        self.lineEdit_head_.setText(QCoreApplication.translate("SubForm_Data", u"40", None))
        self.label_16.setText(QCoreApplication.translate("SubForm_Data", u"\u9971\u548c\u5ea6", None))
        self.pushButton_add_data_.setText(QCoreApplication.translate("SubForm_Data", u"\u6dfb\u52a0", None))
        self.label_lane_.setText(QCoreApplication.translate("SubForm_Data", u"\u901a\u9053", None))
        self.comb_box_lane_.setItemText(0, QCoreApplication.translate("SubForm_Data", u"2", None))
        self.comb_box_lane_.setItemText(1, QCoreApplication.translate("SubForm_Data", u"4", None))
        self.comb_box_lane_.setItemText(2, QCoreApplication.translate("SubForm_Data", u"8", None))
        self.comb_box_lane_.setItemText(3, QCoreApplication.translate("SubForm_Data", u"16", None))

        self.label_color_depth_.setText(QCoreApplication.translate("SubForm_Data", u"\u8272\u6df1", None))
        self.comb_box_color_depth_.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1024", None))
        self.comb_box_color_depth_.setItemText(1, QCoreApplication.translate("SubForm_Data", u"256", None))

        self.label_ppl_.setText(QCoreApplication.translate("SubForm_Data", u"\u5206\u8fa8\u7387", None))
        self.comb_box_width_.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1920", None))
        self.comb_box_width_.setItemText(1, QCoreApplication.translate("SubForm_Data", u"2560", None))
        self.comb_box_width_.setItemText(2, QCoreApplication.translate("SubForm_Data", u"3840", None))

        self.label_x_.setText(QCoreApplication.translate("SubForm_Data", u"x", None))
        self.comb_box_height_.setItemText(0, QCoreApplication.translate("SubForm_Data", u"1080", None))
        self.comb_box_height_.setItemText(1, QCoreApplication.translate("SubForm_Data", u"1440", None))
        self.comb_box_height_.setItemText(2, QCoreApplication.translate("SubForm_Data", u"2160", None))

        self.label_13.setText(QCoreApplication.translate("SubForm_Data", u"\u5e27\u5934", None))
        self.label_15.setText(QCoreApplication.translate("SubForm_Data", u"\u5bf9\u6bd4\u5ea6", None))
    # retranslateUi

