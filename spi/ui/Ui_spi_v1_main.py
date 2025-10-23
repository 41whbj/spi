# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spi_v1_main.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(1024, 780)
        MainForm.setMinimumSize(QSize(1024, 780))
        MainForm.setMaximumSize(QSize(3000, 1000))
        self.gridLayout_7 = QGridLayout(MainForm)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 0, 2, 0)
        self.button_pc_mcu = QPushButton(MainForm)
        self.button_pc_mcu.setObjectName(u"button_pc_mcu")
        self.button_pc_mcu.setMaximumSize(QSize(100, 25))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        self.button_pc_mcu.setFont(font)

        self.gridLayout_7.addWidget(self.button_pc_mcu, 0, 1, 1, 1)

        self.log_widget = QWidget(MainForm)
        self.log_widget.setObjectName(u"log_widget")
        self.log_widget.setMinimumSize(QSize(500, 125))
        self.gridLayout_3 = QGridLayout(self.log_widget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.text_log = QPlainTextEdit(self.log_widget)
        self.text_log.setObjectName(u"text_log")
        self.text_log.setMinimumSize(QSize(790, 0))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(12)
        self.text_log.setFont(font1)
        self.text_log.setFrameShadow(QFrame.Shadow.Raised)
        self.text_log.setReadOnly(True)

        self.gridLayout_3.addWidget(self.text_log, 0, 0, 1, 3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.log_widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label_receive_size = QLabel(self.splitter)
        self.label_receive_size.setObjectName(u"label_receive_size")
        self.label_receive_size.setMinimumSize(QSize(81, 30))
        self.label_receive_size.setMaximumSize(QSize(81, 30))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_receive_size.setFont(font2)
        self.splitter.addWidget(self.label_receive_size)
        self.combo_box_size = QComboBox(self.splitter)
        self.combo_box_size.setObjectName(u"combo_box_size")
        self.combo_box_size.setMinimumSize(QSize(100, 30))
        self.combo_box_size.setMaximumSize(QSize(100, 30))
        font3 = QFont()
        font3.setPointSize(12)
        self.combo_box_size.setFont(font3)
        self.splitter.addWidget(self.combo_box_size)

        self.verticalLayout.addWidget(self.splitter)

        self.check_box_receive = QCheckBox(self.log_widget)
        self.check_box_receive.setObjectName(u"check_box_receive")
        self.check_box_receive.setMinimumSize(QSize(0, 0))
        self.check_box_receive.setMaximumSize(QSize(271, 30))
        self.check_box_receive.setFont(font3)

        self.verticalLayout.addWidget(self.check_box_receive)

        self.button_receive = QPushButton(self.log_widget)
        self.button_receive.setObjectName(u"button_receive")
        self.button_receive.setMinimumSize(QSize(0, 39))
        self.button_receive.setMaximumSize(QSize(271, 40))

        self.verticalLayout.addWidget(self.button_receive)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 3, 1, 1)

        self.button_save = QPushButton(self.log_widget)
        self.button_save.setObjectName(u"button_save")
        self.button_save.setMinimumSize(QSize(50, 25))
        self.button_save.setMaximumSize(QSize(100, 100))
        font4 = QFont()
        font4.setFamilies([u"\u5b8b\u4f53"])
        font4.setPointSize(10)
        self.button_save.setFont(font4)

        self.gridLayout_3.addWidget(self.button_save, 1, 0, 1, 1)

        self.button_clear = QPushButton(self.log_widget)
        self.button_clear.setObjectName(u"button_clear")
        self.button_clear.setMinimumSize(QSize(50, 25))
        self.button_clear.setMaximumSize(QSize(100, 100))
        self.button_clear.setFont(font4)

        self.gridLayout_3.addWidget(self.button_clear, 1, 1, 1, 1)


        self.gridLayout_7.addWidget(self.log_widget, 4, 0, 1, 4)

        self.button_fold_log = QPushButton(MainForm)
        self.button_fold_log.setObjectName(u"button_fold_log")
        self.button_fold_log.setMinimumSize(QSize(40, 25))
        self.button_fold_log.setMaximumSize(QSize(40, 25))

        self.gridLayout_7.addWidget(self.button_fold_log, 3, 0, 1, 1)

        self.button_pc_fpga = QPushButton(MainForm)
        self.button_pc_fpga.setObjectName(u"button_pc_fpga")
        self.button_pc_fpga.setMaximumSize(QSize(100, 25))
        self.button_pc_fpga.setFont(font4)

        self.gridLayout_7.addWidget(self.button_pc_fpga, 0, 0, 1, 1)

        self.stacked_widget = QStackedWidget(MainForm)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.stacked_widget.setMinimumSize(QSize(990, 0))
        self.stacked_widget.setSizeIncrement(QSize(0, 0))
        font5 = QFont()
        font5.setPointSize(9)
        self.stacked_widget.setFont(font5)
        self.stacked_widget.setLineWidth(1)
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.gridLayout = QGridLayout(self.Main)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(2)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.Main)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(99, 25))
        self.label_5.setFont(font1)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.line_delay = QLineEdit(self.Main)
        self.line_delay.setObjectName(u"line_delay")
        self.line_delay.setMinimumSize(QSize(140, 0))
        self.line_delay.setMaximumSize(QSize(205, 25))
        self.line_delay.setFont(font3)

        self.horizontalLayout_7.addWidget(self.line_delay)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.button_start = QPushButton(self.Main)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setMinimumSize(QSize(0, 0))
        self.button_start.setMaximumSize(QSize(231, 25))
        self.button_start.setFont(font4)

        self.horizontalLayout_10.addWidget(self.button_start)

        self.button_stop = QPushButton(self.Main)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setMinimumSize(QSize(0, 0))
        self.button_stop.setMaximumSize(QSize(168, 25))
        self.button_stop.setFont(font4)

        self.horizontalLayout_10.addWidget(self.button_stop)


        self.gridLayout_2.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.radio_button_order = QRadioButton(self.Main)
        self.radio_button_order.setObjectName(u"radio_button_order")
        self.radio_button_order.setMinimumSize(QSize(0, 0))
        self.radio_button_order.setMaximumSize(QSize(300, 25))
        self.radio_button_order.setFont(font1)

        self.verticalLayout_5.addWidget(self.radio_button_order)

        self.radio_button_circ = QRadioButton(self.Main)
        self.radio_button_circ.setObjectName(u"radio_button_circ")
        self.radio_button_circ.setMinimumSize(QSize(0, 0))
        self.radio_button_circ.setMaximumSize(QSize(300, 25))
        self.radio_button_circ.setFont(font1)

        self.verticalLayout_5.addWidget(self.radio_button_circ)

        self.radio_button_random = QRadioButton(self.Main)
        self.radio_button_random.setObjectName(u"radio_button_random")
        self.radio_button_random.setMinimumSize(QSize(0, 0))
        self.radio_button_random.setMaximumSize(QSize(300, 25))
        self.radio_button_random.setFont(font1)

        self.verticalLayout_5.addWidget(self.radio_button_random)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.check_box_mode_poll = QCheckBox(self.Main)
        self.check_box_mode_poll.setObjectName(u"check_box_mode_poll")
        self.check_box_mode_poll.setMaximumSize(QSize(80, 16777215))
        self.check_box_mode_poll.setFont(font4)

        self.horizontalLayout_2.addWidget(self.check_box_mode_poll)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.button_del_mode_group = QPushButton(self.Main)
        self.button_del_mode_group.setObjectName(u"button_del_mode_group")
        self.button_del_mode_group.setMaximumSize(QSize(65, 25))
        font6 = QFont()
        font6.setFamilies([u"\u5b8b\u4f53"])
        font6.setPointSize(9)
        self.button_del_mode_group.setFont(font6)

        self.horizontalLayout_5.addWidget(self.button_del_mode_group)

        self.button_add_mode_group = QPushButton(self.Main)
        self.button_add_mode_group.setObjectName(u"button_add_mode_group")
        self.button_add_mode_group.setMaximumSize(QSize(65, 25))
        self.button_add_mode_group.setFont(font6)

        self.horizontalLayout_5.addWidget(self.button_add_mode_group)

        self.combo_box_mode_group = QComboBox(self.Main)
        self.combo_box_mode_group.setObjectName(u"combo_box_mode_group")
        self.combo_box_mode_group.setMaximumSize(QSize(155, 25))

        self.horizontalLayout_5.addWidget(self.combo_box_mode_group)

        self.button_del_select = QPushButton(self.Main)
        self.button_del_select.setObjectName(u"button_del_select")
        self.button_del_select.setMaximumSize(QSize(45, 21))

        self.horizontalLayout_5.addWidget(self.button_del_select)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.list_group = QListWidget(self.Main)
        self.list_group.setObjectName(u"list_group")
        self.list_group.setMinimumSize(QSize(0, 0))
        self.list_group.setMaximumSize(QSize(340, 16777215))
        font7 = QFont()
        font7.setPointSize(16)
        self.list_group.setFont(font7)

        self.gridLayout_2.addWidget(self.list_group, 1, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.Main)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(99, 25))
        self.label_2.setFont(font1)

        self.horizontalLayout_9.addWidget(self.label_2)

        self.line_number = QLineEdit(self.Main)
        self.line_number.setObjectName(u"line_number")
        self.line_number.setMinimumSize(QSize(150, 0))
        self.line_number.setMaximumSize(QSize(205, 25))
        self.line_number.setFont(font3)

        self.horizontalLayout_9.addWidget(self.line_number)


        self.gridLayout_2.addLayout(self.horizontalLayout_9, 4, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_add = QPushButton(self.Main)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(25, 25))
        self.button_add.setMaximumSize(QSize(25, 16777215))
        font8 = QFont()
        font8.setPointSize(10)
        self.button_add.setFont(font8)

        self.verticalLayout_2.addWidget(self.button_add)

        self.button_det = QPushButton(self.Main)
        self.button_det.setObjectName(u"button_det")
        self.button_det.setMinimumSize(QSize(25, 25))
        self.button_det.setMaximumSize(QSize(25, 16777215))
        self.button_det.setFont(font8)

        self.verticalLayout_2.addWidget(self.button_det)

        self.button_crc = QPushButton(self.Main)
        self.button_crc.setObjectName(u"button_crc")
        self.button_crc.setMinimumSize(QSize(25, 25))
        self.button_crc.setMaximumSize(QSize(25, 16777215))

        self.verticalLayout_2.addWidget(self.button_crc)

        self.verticalSpacer = QSpacerItem(22, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.list_data = QListWidget(self.Main)
        self.list_data.setObjectName(u"list_data")
        self.list_data.setMinimumSize(QSize(640, 495))
        font9 = QFont()
        font9.setPointSize(22)
        self.list_data.setFont(font9)

        self.gridLayout_4.addWidget(self.list_data, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.Main)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(48, 25))

        self.horizontalLayout_6.addWidget(self.label_8)

        self.line_prj_name = QLineEdit(self.Main)
        self.line_prj_name.setObjectName(u"line_prj_name")
        self.line_prj_name.setMaximumSize(QSize(132, 16777215))

        self.horizontalLayout_6.addWidget(self.line_prj_name)

        self.button_new_prj = QPushButton(self.Main)
        self.button_new_prj.setObjectName(u"button_new_prj")
        self.button_new_prj.setMinimumSize(QSize(79, 25))
        self.button_new_prj.setMaximumSize(QSize(16777215, 16777215))
        self.button_new_prj.setFont(font6)

        self.horizontalLayout_6.addWidget(self.button_new_prj)

        self.button_import_prj = QPushButton(self.Main)
        self.button_import_prj.setObjectName(u"button_import_prj")
        self.button_import_prj.setMinimumSize(QSize(79, 25))
        self.button_import_prj.setMaximumSize(QSize(16777215, 16777215))
        self.button_import_prj.setFont(font6)

        self.horizontalLayout_6.addWidget(self.button_import_prj)

        self.label_3 = QLabel(self.Main)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16, 19))

        self.horizontalLayout_6.addWidget(self.label_3)

        self.label = QLabel(self.Main)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(45, 25))
        self.label.setMaximumSize(QSize(45, 25))
        self.label.setFont(font4)

        self.horizontalLayout_6.addWidget(self.label)

        self.combo_box_data_group = QComboBox(self.Main)
        self.combo_box_data_group.setObjectName(u"combo_box_data_group")
        self.combo_box_data_group.setMinimumSize(QSize(80, 25))

        self.horizontalLayout_6.addWidget(self.combo_box_data_group)

        self.button_rename = QPushButton(self.Main)
        self.button_rename.setObjectName(u"button_rename")
        self.button_rename.setMinimumSize(QSize(79, 25))
        self.button_rename.setMaximumSize(QSize(16777215, 16777215))
        self.button_rename.setFont(font6)

        self.horizontalLayout_6.addWidget(self.button_rename)

        self.button_add_data_group = QPushButton(self.Main)
        self.button_add_data_group.setObjectName(u"button_add_data_group")
        self.button_add_data_group.setMinimumSize(QSize(79, 25))
        self.button_add_data_group.setFont(font6)

        self.horizontalLayout_6.addWidget(self.button_add_data_group)

        self.button_del_data_group = QPushButton(self.Main)
        self.button_del_data_group.setObjectName(u"button_del_data_group")
        self.button_del_data_group.setMinimumSize(QSize(79, 25))
        self.button_del_data_group.setFont(font6)

        self.horizontalLayout_6.addWidget(self.button_del_data_group)


        self.gridLayout_4.addLayout(self.horizontalLayout_6, 0, 0, 1, 2)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.line_edit_data = QLineEdit(self.Main)
        self.line_edit_data.setObjectName(u"line_edit_data")
        self.line_edit_data.setMinimumSize(QSize(0, 50))
        self.line_edit_data.setMaximumSize(QSize(16777215, 16777215))
        font10 = QFont()
        font10.setPointSize(14)
        self.line_edit_data.setFont(font10)

        self.horizontalLayout_11.addWidget(self.line_edit_data)

        self.button_send = QPushButton(self.Main)
        self.button_send.setObjectName(u"button_send")
        self.button_send.setMinimumSize(QSize(185, 50))
        self.button_send.setMaximumSize(QSize(185, 16777215))
        self.button_send.setFont(font4)

        self.horizontalLayout_11.addWidget(self.button_send)


        self.gridLayout_4.addLayout(self.horizontalLayout_11, 2, 0, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout_4)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.stacked_widget.addWidget(self.Main)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setFont(font5)
        self.gridLayout_5 = QGridLayout(self.page)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(0)
        self.MCU_button_send = QPushButton(self.page)
        self.MCU_button_send.setObjectName(u"MCU_button_send")
        self.MCU_button_send.setMinimumSize(QSize(0, 53))

        self.gridLayout_9.addWidget(self.MCU_button_send, 1, 0, 1, 1)

        self.MCU_button_stop = QPushButton(self.page)
        self.MCU_button_stop.setObjectName(u"MCU_button_stop")
        self.MCU_button_stop.setMinimumSize(QSize(0, 53))

        self.gridLayout_9.addWidget(self.MCU_button_stop, 1, 1, 1, 1)

        self.MCU_list_test = QListWidget(self.page)
        self.MCU_list_test.setObjectName(u"MCU_list_test")
        self.MCU_list_test.setMinimumSize(QSize(420, 0))
        self.MCU_list_test.setMaximumSize(QSize(480, 16777215))

        self.gridLayout_9.addWidget(self.MCU_list_test, 0, 0, 1, 2)


        self.gridLayout_6.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_mcu_connect = QPushButton(self.page)
        self.button_mcu_connect.setObjectName(u"button_mcu_connect")
        self.button_mcu_connect.setMaximumSize(QSize(76, 24))

        self.horizontalLayout_3.addWidget(self.button_mcu_connect)

        self.button_mcu_scan = QPushButton(self.page)
        self.button_mcu_scan.setObjectName(u"button_mcu_scan")
        self.button_mcu_scan.setMaximumSize(QSize(79, 24))

        self.horizontalLayout_3.addWidget(self.button_mcu_scan)

        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.line_test_interval = QLineEdit(self.page)
        self.line_test_interval.setObjectName(u"line_test_interval")
        self.line_test_interval.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.line_test_interval)

        self.button_mcu_export_pdf = QPushButton(self.page)
        self.button_mcu_export_pdf.setObjectName(u"button_mcu_export_pdf")

        self.horizontalLayout_3.addWidget(self.button_mcu_export_pdf)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.MCU_list_case = QListWidget(self.page)
        self.MCU_list_case.setObjectName(u"MCU_list_case")
        self.MCU_list_case.setMinimumSize(QSize(560, 0))

        self.verticalLayout_7.addWidget(self.MCU_list_case)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(2)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.MCU_line_test = QLineEdit(self.page)
        self.MCU_line_test.setObjectName(u"MCU_line_test")
        self.MCU_line_test.setMinimumSize(QSize(0, 48))
        self.MCU_line_test.setFont(font10)

        self.horizontalLayout_14.addWidget(self.MCU_line_test)

        self.MCU_button_test = QPushButton(self.page)
        self.MCU_button_test.setObjectName(u"MCU_button_test")
        self.MCU_button_test.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_14.addWidget(self.MCU_button_test)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)


        self.gridLayout_6.addLayout(self.verticalLayout_7, 0, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.stacked_widget.addWidget(self.page)

        self.gridLayout_7.addWidget(self.stacked_widget, 2, 0, 1, 4)

        self.horizontalSpacer_2 = QSpacerItem(774, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.button_spi_config = QPushButton(MainForm)
        self.button_spi_config.setObjectName(u"button_spi_config")

        self.gridLayout_7.addWidget(self.button_spi_config, 0, 2, 1, 1)

        self.spi_config_widget = QWidget(MainForm)
        self.spi_config_widget.setObjectName(u"spi_config_widget")
        self.layout_spi_config = QGridLayout(self.spi_config_widget)
        self.layout_spi_config.setSpacing(0)
        self.layout_spi_config.setObjectName(u"layout_spi_config")
        self.layout_spi_config.setContentsMargins(0, 0, 0, 0)
        self.combo_box_clk = QComboBox(self.spi_config_widget)
        self.combo_box_clk.setObjectName(u"combo_box_clk")
        self.combo_box_clk.setMinimumSize(QSize(110, 29))
        self.combo_box_clk.setMaximumSize(QSize(110, 16777215))
        self.combo_box_clk.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_clk, 0, 9, 1, 1)

        self.label_bit = QLabel(self.spi_config_widget)
        self.label_bit.setObjectName(u"label_bit")
        self.label_bit.setMinimumSize(QSize(0, 0))
        self.label_bit.setMaximumSize(QSize(45, 25))
        self.label_bit.setFont(font8)

        self.layout_spi_config.addWidget(self.label_bit, 0, 10, 1, 1)

        self.label_clk = QLabel(self.spi_config_widget)
        self.label_clk.setObjectName(u"label_clk")
        self.label_clk.setMinimumSize(QSize(0, 0))
        self.label_clk.setMaximumSize(QSize(30, 25))
        self.label_clk.setFont(font8)

        self.layout_spi_config.addWidget(self.label_clk, 0, 8, 1, 1)

        self.line_device = QLineEdit(self.spi_config_widget)
        self.line_device.setObjectName(u"line_device")
        self.line_device.setMinimumSize(QSize(120, 25))
        self.line_device.setMaximumSize(QSize(110, 25))
        self.line_device.setFont(font8)
        self.line_device.setReadOnly(True)

        self.layout_spi_config.addWidget(self.line_device, 0, 1, 1, 1)

        self.label_speed = QLabel(self.spi_config_widget)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setMinimumSize(QSize(0, 0))
        self.label_speed.setMaximumSize(QSize(50, 25))
        self.label_speed.setFont(font8)

        self.layout_spi_config.addWidget(self.label_speed, 0, 6, 1, 1)

        self.combo_box_vcc = QComboBox(self.spi_config_widget)
        self.combo_box_vcc.setObjectName(u"combo_box_vcc")
        self.combo_box_vcc.setMinimumSize(QSize(70, 29))
        self.combo_box_vcc.setMaximumSize(QSize(70, 16777215))
        self.combo_box_vcc.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_vcc, 0, 3, 1, 1)

        self.label_io = QLabel(self.spi_config_widget)
        self.label_io.setObjectName(u"label_io")
        self.label_io.setMinimumSize(QSize(0, 0))
        self.label_io.setMaximumSize(QSize(45, 25))
        self.label_io.setFont(font8)

        self.layout_spi_config.addWidget(self.label_io, 0, 4, 1, 1)

        self.combo_box_io = QComboBox(self.spi_config_widget)
        self.combo_box_io.setObjectName(u"combo_box_io")
        self.combo_box_io.setMinimumSize(QSize(70, 29))
        self.combo_box_io.setMaximumSize(QSize(70, 16777215))
        self.combo_box_io.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_io, 0, 5, 1, 1)

        self.label_vcc = QLabel(self.spi_config_widget)
        self.label_vcc.setObjectName(u"label_vcc")
        self.label_vcc.setMinimumSize(QSize(0, 0))
        self.label_vcc.setMaximumSize(QSize(60, 25))
        self.label_vcc.setFont(font8)

        self.layout_spi_config.addWidget(self.label_vcc, 0, 2, 1, 1)

        self.label_decive = QLabel(self.spi_config_widget)
        self.label_decive.setObjectName(u"label_decive")
        self.label_decive.setMinimumSize(QSize(0, 0))
        self.label_decive.setMaximumSize(QSize(35, 25))
        self.label_decive.setFont(font8)

        self.layout_spi_config.addWidget(self.label_decive, 0, 0, 1, 1)

        self.combo_box_speed = QComboBox(self.spi_config_widget)
        self.combo_box_speed.setObjectName(u"combo_box_speed")
        self.combo_box_speed.setMinimumSize(QSize(80, 29))
        self.combo_box_speed.setMaximumSize(QSize(80, 16777215))
        self.combo_box_speed.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_speed, 0, 7, 1, 1)

        self.label_s_or_q = QLabel(self.spi_config_widget)
        self.label_s_or_q.setObjectName(u"label_s_or_q")
        self.label_s_or_q.setMinimumSize(QSize(0, 0))
        self.label_s_or_q.setMaximumSize(QSize(50, 25))
        self.label_s_or_q.setFont(font8)

        self.layout_spi_config.addWidget(self.label_s_or_q, 0, 12, 1, 1)

        self.combo_box_s_or_q = QComboBox(self.spi_config_widget)
        self.combo_box_s_or_q.setObjectName(u"combo_box_s_or_q")
        self.combo_box_s_or_q.setMinimumSize(QSize(110, 29))
        self.combo_box_s_or_q.setMaximumSize(QSize(110, 16777215))
        self.combo_box_s_or_q.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_s_or_q, 0, 13, 1, 1)

        self.combo_box_bit = QComboBox(self.spi_config_widget)
        self.combo_box_bit.setObjectName(u"combo_box_bit")
        self.combo_box_bit.setMinimumSize(QSize(80, 29))
        self.combo_box_bit.setMaximumSize(QSize(80, 16777215))
        self.combo_box_bit.setFont(font8)

        self.layout_spi_config.addWidget(self.combo_box_bit, 0, 11, 1, 1)


        self.gridLayout_7.addWidget(self.spi_config_widget, 1, 0, 1, 4)


        self.retranslateUi(MainForm)

        self.stacked_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"SPI\u4e0a\u4f4d\u673a", None))
#if QT_CONFIG(tooltip)
        MainForm.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.button_pc_mcu.setText(QCoreApplication.translate("MainForm", u"PC-MCU", None))
        self.text_log.setPlainText("")
        self.label_receive_size.setText(QCoreApplication.translate("MainForm", u"\u8bfb\u6570\u636e\u957f\u5ea6", None))
        self.check_box_receive.setText(QCoreApplication.translate("MainForm", u"\u8bfb\u6570\u636e", None))
        self.button_receive.setText(QCoreApplication.translate("MainForm", u"\u53ea\u8bfb", None))
#if QT_CONFIG(tooltip)
        self.button_save.setToolTip(QCoreApplication.translate("MainForm", u"\u4fdd\u5b58", None))
#endif // QT_CONFIG(tooltip)
        self.button_save.setText(QCoreApplication.translate("MainForm", u"\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.button_clear.setToolTip(QCoreApplication.translate("MainForm", u"\u6e05\u9664", None))
#endif // QT_CONFIG(tooltip)
        self.button_clear.setText(QCoreApplication.translate("MainForm", u"\u6e05\u9664", None))
        self.button_fold_log.setText(QCoreApplication.translate("MainForm", u">", None))
        self.button_pc_fpga.setText(QCoreApplication.translate("MainForm", u"PC-FPGA", None))
#if QT_CONFIG(tooltip)
        self.stacked_widget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.Main.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainForm", u"\u5ef6\u65f6(s)", None))
        self.button_start.setText(QCoreApplication.translate("MainForm", u"\u542f\u52a8", None))
        self.button_stop.setText(QCoreApplication.translate("MainForm", u"\u7ec8\u6b62", None))
        self.radio_button_order.setText(QCoreApplication.translate("MainForm", u"\u987a\u5e8f\u6267\u884c", None))
        self.radio_button_circ.setText(QCoreApplication.translate("MainForm", u"\u5faa\u73af\u6267\u884c", None))
        self.radio_button_random.setText(QCoreApplication.translate("MainForm", u"\u968f\u673a\u6267\u884c", None))
#if QT_CONFIG(tooltip)
        self.check_box_mode_poll.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p>\u52fe\u9009\u540e\uff0c\u5faa\u73af\u548c\u987a\u5e8f\u6267\u884c\u7684\u76ee\u6807\u8f6c\u53d8\u4e3a\u5217\u8868\u4e2d\u6240\u6709\u7684\u6570\u636e\uff0c</p><p>\u6b64\u65f6\u7684\u8f93\u5165\u5ef6\u65f6\u4e3a\u7ec4\u95f4\u7684\u53d1\u9001\u95f4\u9694\uff0c\u7ec4\u5185\u6570\u636e\u53d1\u9001\u95f4\u9694\u56fa\u5b9a\u4e3a0.5s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.check_box_mode_poll.setText(QCoreApplication.translate("MainForm", u"\u7ec4\u95f4\u53d1\u9001", None))
        self.button_del_mode_group.setText(QCoreApplication.translate("MainForm", u"\u5220\u9664", None))
        self.button_add_mode_group.setText(QCoreApplication.translate("MainForm", u"\u6dfb\u52a0", None))
        self.button_del_select.setText(QCoreApplication.translate("MainForm", u"-", None))
        self.label_2.setText(QCoreApplication.translate("MainForm", u"\u6b21\u6570", None))
#if QT_CONFIG(tooltip)
        self.button_add.setToolTip(QCoreApplication.translate("MainForm", u"\u6dfb\u52a0\u6570\u636e", None))
#endif // QT_CONFIG(tooltip)
        self.button_add.setText(QCoreApplication.translate("MainForm", u"+", None))
#if QT_CONFIG(tooltip)
        self.button_det.setToolTip(QCoreApplication.translate("MainForm", u"\u5220\u9664\u6570\u636e", None))
#endif // QT_CONFIG(tooltip)
        self.button_det.setText(QCoreApplication.translate("MainForm", u"-", None))
#if QT_CONFIG(tooltip)
        self.button_crc.setToolTip(QCoreApplication.translate("MainForm", u"CRC\u68c0\u9a8c", None))
#endif // QT_CONFIG(tooltip)
        self.button_crc.setText(QCoreApplication.translate("MainForm", u"C", None))
        self.label_8.setText(QCoreApplication.translate("MainForm", u"\u9879\u76ee\u540d\u79f0", None))
        self.button_new_prj.setText(QCoreApplication.translate("MainForm", u"\u65b0\u5efa", None))
        self.button_import_prj.setText(QCoreApplication.translate("MainForm", u"\u5bfc\u5165", None))
        self.label_3.setText(QCoreApplication.translate("MainForm", u"|", None))
        self.label.setText(QCoreApplication.translate("MainForm", u"\u6570\u636e\u96c6", None))
        self.button_rename.setText(QCoreApplication.translate("MainForm", u"\u91cd\u547d\u540d", None))
        self.button_add_data_group.setText(QCoreApplication.translate("MainForm", u"\u6dfb\u52a0", None))
        self.button_del_data_group.setText(QCoreApplication.translate("MainForm", u"\u5220\u9664", None))
        self.line_edit_data.setText("")
        self.button_send.setText(QCoreApplication.translate("MainForm", u"\u53d1\u9001", None))
        self.MCU_button_send.setText(QCoreApplication.translate("MainForm", u"\u53d1\u9001", None))
        self.MCU_button_stop.setText(QCoreApplication.translate("MainForm", u"\u7ec8\u6b62", None))
        self.button_mcu_connect.setText(QCoreApplication.translate("MainForm", u"\u8fde\u63a5", None))
        self.button_mcu_scan.setText(QCoreApplication.translate("MainForm", u"\u626b\u63cf", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p>\u8f93\u5165\u6846\u7528\u6765\u63a7\u5236\u8fde\u63a5\u548c\u626b\u63cf\u65f6\uff0cSPI\u8bf7\u6c42MCU\u65f6\u7684\u5199\u65f6\u5e8f\u548c\u56de\u8bfbMCU\u7684\u8bfb\u65f6\u5e8f\u95f4\u9694\uff0c\u9632\u6b62\u65f6\u95f4\u8fc7\u77ed\u5bfc\u81f4MCU\u65e0\u6cd5\u53ca\u65f6\u54cd\u5e94</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainForm", u"\u8c03\u8bd5\u533a\u57df", None))
        self.button_mcu_export_pdf.setText(QCoreApplication.translate("MainForm", u"\u5bfc\u51fa\u6d4b\u8bd5\u6587\u6863", None))
        self.MCU_button_test.setText(QCoreApplication.translate("MainForm", u"\u53d1\u9001", None))
        self.button_spi_config.setText(QCoreApplication.translate("MainForm", u"spi\u914d\u7f6e", None))
        self.label_bit.setText(QCoreApplication.translate("MainForm", u"\u4f4d\u987a\u5e8f", None))
        self.label_clk.setText(QCoreApplication.translate("MainForm", u"\u65f6\u949f", None))
        self.label_speed.setText(QCoreApplication.translate("MainForm", u"SPI\u901f\u7387", None))
        self.label_io.setText(QCoreApplication.translate("MainForm", u"IO\u7535\u5e73", None))
        self.label_vcc.setText(QCoreApplication.translate("MainForm", u"VCC\u7535\u538b", None))
        self.label_decive.setText(QCoreApplication.translate("MainForm", u"\u8bbe\u5907", None))
        self.label_s_or_q.setText(QCoreApplication.translate("MainForm", u"S/QSPI", None))
    # retranslateUi

