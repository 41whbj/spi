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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(1024, 830)
        MainForm.setMinimumSize(QSize(1024, 830))
        MainForm.setMaximumSize(QSize(2048, 1000))
        self.gridLayout_4 = QGridLayout(MainForm)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_message = QPushButton(MainForm)
        self.button_message.setObjectName(u"button_message")
        self.button_message.setMaximumSize(QSize(100, 25))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(10)
        self.button_message.setFont(font)

        self.horizontalLayout_5.addWidget(self.button_message)

        self.button_pc_fpga = QPushButton(MainForm)
        self.button_pc_fpga.setObjectName(u"button_pc_fpga")
        self.button_pc_fpga.setMaximumSize(QSize(100, 25))
        self.button_pc_fpga.setFont(font)

        self.horizontalLayout_5.addWidget(self.button_pc_fpga)

        self.button_pc_mcu = QPushButton(MainForm)
        self.button_pc_mcu.setObjectName(u"button_pc_mcu")
        self.button_pc_mcu.setMaximumSize(QSize(100, 25))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        self.button_pc_mcu.setFont(font1)

        self.horizontalLayout_5.addWidget(self.button_pc_mcu)

        self.button_hard = QPushButton(MainForm)
        self.button_hard.setObjectName(u"button_hard")
        self.button_hard.setMaximumSize(QSize(100, 25))
        self.button_hard.setFont(font)

        self.horizontalLayout_5.addWidget(self.button_hard)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.gridLayout_4.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.stacked_widget = QStackedWidget(MainForm)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.stacked_widget.setMinimumSize(QSize(990, 0))
        self.stacked_widget.setSizeIncrement(QSize(0, 0))
        self.stacked_widget.setLineWidth(1)
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.gridLayout = QGridLayout(self.Main)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(-1, -1, -1, 2)
        self.button_fold_log = QPushButton(self.Main)
        self.button_fold_log.setObjectName(u"button_fold_log")
        self.button_fold_log.setMinimumSize(QSize(40, 25))
        self.button_fold_log.setMaximumSize(QSize(40, 25))

        self.gridLayout.addWidget(self.button_fold_log, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter_9 = QSplitter(self.Main)
        self.splitter_9.setObjectName(u"splitter_9")
        self.splitter_9.setToolTipDuration(0)
        self.splitter_9.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter_9)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.line_prj_name = QLineEdit(self.layoutWidget)
        self.line_prj_name.setObjectName(u"line_prj_name")

        self.horizontalLayout_6.addWidget(self.line_prj_name)

        self.button_new_prj = QPushButton(self.layoutWidget)
        self.button_new_prj.setObjectName(u"button_new_prj")
        self.button_new_prj.setMinimumSize(QSize(79, 25))
        self.button_new_prj.setMaximumSize(QSize(16777215, 16777215))
        self.button_new_prj.setFont(font)

        self.horizontalLayout_6.addWidget(self.button_new_prj)

        self.button_import_prj = QPushButton(self.layoutWidget)
        self.button_import_prj.setObjectName(u"button_import_prj")
        self.button_import_prj.setMinimumSize(QSize(79, 25))
        self.button_import_prj.setMaximumSize(QSize(16777215, 16777215))
        self.button_import_prj.setFont(font)

        self.horizontalLayout_6.addWidget(self.button_import_prj)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16, 19))

        self.horizontalLayout_6.addWidget(self.label_3)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(45, 25))
        self.label.setFont(font)

        self.horizontalLayout_6.addWidget(self.label)

        self.combo_box_data_group = QComboBox(self.layoutWidget)
        self.combo_box_data_group.setObjectName(u"combo_box_data_group")
        self.combo_box_data_group.setMinimumSize(QSize(80, 25))

        self.horizontalLayout_6.addWidget(self.combo_box_data_group)

        self.button_rename = QPushButton(self.layoutWidget)
        self.button_rename.setObjectName(u"button_rename")
        self.button_rename.setMinimumSize(QSize(79, 25))
        self.button_rename.setMaximumSize(QSize(16777215, 16777215))
        self.button_rename.setFont(font)

        self.horizontalLayout_6.addWidget(self.button_rename)

        self.button_add_data_group = QPushButton(self.layoutWidget)
        self.button_add_data_group.setObjectName(u"button_add_data_group")
        self.button_add_data_group.setMinimumSize(QSize(79, 25))
        self.button_add_data_group.setFont(font1)

        self.horizontalLayout_6.addWidget(self.button_add_data_group)

        self.button_del_data_group = QPushButton(self.layoutWidget)
        self.button_del_data_group.setObjectName(u"button_del_data_group")
        self.button_del_data_group.setMinimumSize(QSize(79, 25))
        self.button_del_data_group.setFont(font1)

        self.horizontalLayout_6.addWidget(self.button_del_data_group)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.list_data = QListWidget(self.layoutWidget)
        self.list_data.setObjectName(u"list_data")
        self.list_data.setMinimumSize(QSize(636, 500))
        font2 = QFont()
        font2.setPointSize(22)
        self.list_data.setFont(font2)

        self.horizontalLayout_4.addWidget(self.list_data)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_add = QPushButton(self.layoutWidget)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(25, 25))
        self.button_add.setMaximumSize(QSize(25, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        self.button_add.setFont(font3)

        self.verticalLayout_2.addWidget(self.button_add)

        self.button_det = QPushButton(self.layoutWidget)
        self.button_det.setObjectName(u"button_det")
        self.button_det.setMinimumSize(QSize(25, 25))
        self.button_det.setMaximumSize(QSize(25, 16777215))
        self.button_det.setFont(font3)

        self.verticalLayout_2.addWidget(self.button_det)

        self.button_crc = QPushButton(self.layoutWidget)
        self.button_crc.setObjectName(u"button_crc")
        self.button_crc.setMinimumSize(QSize(25, 25))
        self.button_crc.setMaximumSize(QSize(25, 16777215))

        self.verticalLayout_2.addWidget(self.button_crc)

        self.verticalSpacer = QSpacerItem(22, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.line_edit_data = QLineEdit(self.layoutWidget)
        self.line_edit_data.setObjectName(u"line_edit_data")
        self.line_edit_data.setMinimumSize(QSize(0, 50))
        self.line_edit_data.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setPointSize(14)
        self.line_edit_data.setFont(font4)

        self.horizontalLayout_11.addWidget(self.line_edit_data)

        self.button_send = QPushButton(self.layoutWidget)
        self.button_send.setObjectName(u"button_send")
        self.button_send.setMinimumSize(QSize(185, 50))
        self.button_send.setMaximumSize(QSize(185, 16777215))
        self.button_send.setFont(font)

        self.horizontalLayout_11.addWidget(self.button_send)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.splitter_9.addWidget(self.layoutWidget)

        self.horizontalLayout.addWidget(self.splitter_9)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.list_group = QListWidget(self.Main)
        self.list_group.setObjectName(u"list_group")
        self.list_group.setMinimumSize(QSize(306, 395))
        self.list_group.setMaximumSize(QSize(314, 16777215))
        font5 = QFont()
        font5.setPointSize(16)
        self.list_group.setFont(font5)

        self.gridLayout_2.addWidget(self.list_group, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.Main)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(99, 25))
        font6 = QFont()
        font6.setFamilies([u"\u5b8b\u4f53"])
        font6.setPointSize(12)
        self.label_5.setFont(font6)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.line_delay = QLineEdit(self.Main)
        self.line_delay.setObjectName(u"line_delay")
        self.line_delay.setMinimumSize(QSize(150, 0))
        self.line_delay.setMaximumSize(QSize(210, 25))
        font7 = QFont()
        font7.setPointSize(12)
        self.line_delay.setFont(font7)

        self.horizontalLayout_7.addWidget(self.line_delay)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.button_add_mode_group = QPushButton(self.Main)
        self.button_add_mode_group.setObjectName(u"button_add_mode_group")
        self.button_add_mode_group.setMaximumSize(QSize(50, 25))
        self.button_add_mode_group.setFont(font1)

        self.horizontalLayout_8.addWidget(self.button_add_mode_group)

        self.button_del_mode_group = QPushButton(self.Main)
        self.button_del_mode_group.setObjectName(u"button_del_mode_group")
        self.button_del_mode_group.setMaximumSize(QSize(50, 25))
        self.button_del_mode_group.setFont(font1)

        self.horizontalLayout_8.addWidget(self.button_del_mode_group)

        self.combo_box_mode_group = QComboBox(self.Main)
        self.combo_box_mode_group.setObjectName(u"combo_box_mode_group")
        self.combo_box_mode_group.setMaximumSize(QSize(150, 25))

        self.horizontalLayout_8.addWidget(self.combo_box_mode_group)

        self.button_del_select = QPushButton(self.Main)
        self.button_del_select.setObjectName(u"button_del_select")
        self.button_del_select.setMaximumSize(QSize(31, 21))

        self.horizontalLayout_8.addWidget(self.button_del_select)


        self.gridLayout_2.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.Main)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(99, 25))
        self.label_2.setFont(font6)

        self.horizontalLayout_9.addWidget(self.label_2)

        self.line_number = QLineEdit(self.Main)
        self.line_number.setObjectName(u"line_number")
        self.line_number.setMinimumSize(QSize(150, 0))
        self.line_number.setMaximumSize(QSize(210, 25))
        self.line_number.setFont(font7)

        self.horizontalLayout_9.addWidget(self.line_number)


        self.gridLayout_2.addLayout(self.horizontalLayout_9, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.radio_button_order = QRadioButton(self.Main)
        self.radio_button_order.setObjectName(u"radio_button_order")
        self.radio_button_order.setMinimumSize(QSize(0, 0))
        self.radio_button_order.setMaximumSize(QSize(300, 25))
        self.radio_button_order.setFont(font6)

        self.verticalLayout_5.addWidget(self.radio_button_order)

        self.radio_button_circ = QRadioButton(self.Main)
        self.radio_button_circ.setObjectName(u"radio_button_circ")
        self.radio_button_circ.setMinimumSize(QSize(0, 0))
        self.radio_button_circ.setMaximumSize(QSize(300, 25))
        self.radio_button_circ.setFont(font6)

        self.verticalLayout_5.addWidget(self.radio_button_circ)

        self.radio_button_random = QRadioButton(self.Main)
        self.radio_button_random.setObjectName(u"radio_button_random")
        self.radio_button_random.setMinimumSize(QSize(0, 0))
        self.radio_button_random.setMaximumSize(QSize(300, 25))
        self.radio_button_random.setFont(font6)

        self.verticalLayout_5.addWidget(self.radio_button_random)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 10, -1, -1)
        self.check_box_mode_poll = QCheckBox(self.Main)
        self.check_box_mode_poll.setObjectName(u"check_box_mode_poll")
        self.check_box_mode_poll.setMaximumSize(QSize(140, 16777215))
        self.check_box_mode_poll.setFont(font)

        self.verticalLayout_3.addWidget(self.check_box_mode_poll)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.button_start = QPushButton(self.Main)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setMinimumSize(QSize(0, 0))
        self.button_start.setMaximumSize(QSize(155, 25))
        self.button_start.setFont(font)

        self.horizontalLayout_10.addWidget(self.button_start)

        self.button_stop = QPushButton(self.Main)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setMinimumSize(QSize(0, 0))
        self.button_stop.setMaximumSize(QSize(155, 25))
        self.button_stop.setFont(font)

        self.horizontalLayout_10.addWidget(self.button_stop)


        self.gridLayout_2.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.stacked_widget.addWidget(self.Main)
        self.Hard = QWidget()
        self.Hard.setObjectName(u"Hard")
        self.spi_widget = QWidget(self.Hard)
        self.spi_widget.setObjectName(u"spi_widget")
        self.spi_widget.setGeometry(QRect(60, 30, 271, 441))
        self.spi_widget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_7 = QGridLayout(self.spi_widget)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.splitter_19 = QSplitter(self.spi_widget)
        self.splitter_19.setObjectName(u"splitter_19")
        self.splitter_19.setOrientation(Qt.Orientation.Horizontal)
        self.label_s_or_q = QLabel(self.splitter_19)
        self.label_s_or_q.setObjectName(u"label_s_or_q")
        self.label_s_or_q.setMinimumSize(QSize(113, 30))
        self.label_s_or_q.setFont(font7)
        self.splitter_19.addWidget(self.label_s_or_q)
        self.combo_box_s_or_q = QComboBox(self.splitter_19)
        self.combo_box_s_or_q.setObjectName(u"combo_box_s_or_q")
        self.combo_box_s_or_q.setMinimumSize(QSize(150, 30))
        self.combo_box_s_or_q.setMaximumSize(QSize(150, 16777215))
        self.combo_box_s_or_q.setFont(font7)
        self.splitter_19.addWidget(self.combo_box_s_or_q)

        self.gridLayout_7.addWidget(self.splitter_19, 7, 0, 1, 1)

        self.button_receive = QPushButton(self.spi_widget)
        self.button_receive.setObjectName(u"button_receive")
        self.button_receive.setMinimumSize(QSize(268, 40))

        self.gridLayout_7.addWidget(self.button_receive, 10, 0, 1, 1)

        self.splitter_15 = QSplitter(self.spi_widget)
        self.splitter_15.setObjectName(u"splitter_15")
        self.splitter_15.setOrientation(Qt.Orientation.Horizontal)
        self.label_io = QLabel(self.splitter_15)
        self.label_io.setObjectName(u"label_io")
        self.label_io.setMinimumSize(QSize(113, 30))
        self.label_io.setFont(font7)
        self.splitter_15.addWidget(self.label_io)
        self.combo_box_io = QComboBox(self.splitter_15)
        self.combo_box_io.setObjectName(u"combo_box_io")
        self.combo_box_io.setMinimumSize(QSize(150, 30))
        self.combo_box_io.setMaximumSize(QSize(150, 16777215))
        self.combo_box_io.setFont(font7)
        self.splitter_15.addWidget(self.combo_box_io)

        self.gridLayout_7.addWidget(self.splitter_15, 3, 0, 1, 1)

        self.splitter_18 = QSplitter(self.spi_widget)
        self.splitter_18.setObjectName(u"splitter_18")
        self.splitter_18.setOrientation(Qt.Orientation.Horizontal)
        self.label_bit = QLabel(self.splitter_18)
        self.label_bit.setObjectName(u"label_bit")
        self.label_bit.setMinimumSize(QSize(113, 30))
        self.label_bit.setFont(font7)
        self.splitter_18.addWidget(self.label_bit)
        self.combo_box_bit = QComboBox(self.splitter_18)
        self.combo_box_bit.setObjectName(u"combo_box_bit")
        self.combo_box_bit.setMinimumSize(QSize(150, 30))
        self.combo_box_bit.setMaximumSize(QSize(150, 16777215))
        self.combo_box_bit.setFont(font7)
        self.splitter_18.addWidget(self.combo_box_bit)

        self.gridLayout_7.addWidget(self.splitter_18, 6, 0, 1, 1)

        self.splitter_17 = QSplitter(self.spi_widget)
        self.splitter_17.setObjectName(u"splitter_17")
        self.splitter_17.setOrientation(Qt.Orientation.Horizontal)
        self.label_clk = QLabel(self.splitter_17)
        self.label_clk.setObjectName(u"label_clk")
        self.label_clk.setMinimumSize(QSize(113, 30))
        self.label_clk.setFont(font7)
        self.splitter_17.addWidget(self.label_clk)
        self.combo_box_clk = QComboBox(self.splitter_17)
        self.combo_box_clk.setObjectName(u"combo_box_clk")
        self.combo_box_clk.setMinimumSize(QSize(150, 30))
        self.combo_box_clk.setMaximumSize(QSize(150, 16777215))
        self.combo_box_clk.setFont(font7)
        self.splitter_17.addWidget(self.combo_box_clk)

        self.gridLayout_7.addWidget(self.splitter_17, 5, 0, 1, 1)

        self.splitter_16 = QSplitter(self.spi_widget)
        self.splitter_16.setObjectName(u"splitter_16")
        self.splitter_16.setOrientation(Qt.Orientation.Horizontal)
        self.label_speed = QLabel(self.splitter_16)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setMinimumSize(QSize(113, 30))
        self.label_speed.setFont(font7)
        self.splitter_16.addWidget(self.label_speed)
        self.combo_box_speed = QComboBox(self.splitter_16)
        self.combo_box_speed.setObjectName(u"combo_box_speed")
        self.combo_box_speed.setMinimumSize(QSize(150, 30))
        self.combo_box_speed.setMaximumSize(QSize(150, 16777215))
        self.combo_box_speed.setFont(font7)
        self.splitter_16.addWidget(self.combo_box_speed)

        self.gridLayout_7.addWidget(self.splitter_16, 4, 0, 1, 1)

        self.splitter_14 = QSplitter(self.spi_widget)
        self.splitter_14.setObjectName(u"splitter_14")
        self.splitter_14.setOrientation(Qt.Orientation.Horizontal)
        self.label_vcc = QLabel(self.splitter_14)
        self.label_vcc.setObjectName(u"label_vcc")
        self.label_vcc.setMinimumSize(QSize(113, 30))
        self.label_vcc.setFont(font7)
        self.splitter_14.addWidget(self.label_vcc)
        self.combo_box_vcc = QComboBox(self.splitter_14)
        self.combo_box_vcc.setObjectName(u"combo_box_vcc")
        self.combo_box_vcc.setMinimumSize(QSize(150, 30))
        self.combo_box_vcc.setMaximumSize(QSize(150, 16777215))
        self.combo_box_vcc.setFont(font7)
        self.splitter_14.addWidget(self.combo_box_vcc)

        self.gridLayout_7.addWidget(self.splitter_14, 2, 0, 1, 1)

        self.splitter_20 = QSplitter(self.spi_widget)
        self.splitter_20.setObjectName(u"splitter_20")
        self.splitter_20.setOrientation(Qt.Orientation.Horizontal)
        self.label_receive_size = QLabel(self.splitter_20)
        self.label_receive_size.setObjectName(u"label_receive_size")
        self.label_receive_size.setMinimumSize(QSize(113, 30))
        font8 = QFont()
        font8.setPointSize(12)
        font8.setBold(False)
        self.label_receive_size.setFont(font8)
        self.splitter_20.addWidget(self.label_receive_size)
        self.combo_box_size = QComboBox(self.splitter_20)
        self.combo_box_size.setObjectName(u"combo_box_size")
        self.combo_box_size.setMinimumSize(QSize(150, 30))
        self.combo_box_size.setMaximumSize(QSize(150, 16777215))
        self.combo_box_size.setFont(font7)
        self.splitter_20.addWidget(self.combo_box_size)

        self.gridLayout_7.addWidget(self.splitter_20, 8, 0, 1, 1)

        self.check_box_receive = QCheckBox(self.spi_widget)
        self.check_box_receive.setObjectName(u"check_box_receive")
        self.check_box_receive.setMinimumSize(QSize(268, 30))
        self.check_box_receive.setFont(font7)

        self.gridLayout_7.addWidget(self.check_box_receive, 9, 0, 1, 1)

        self.splitter_13 = QSplitter(self.spi_widget)
        self.splitter_13.setObjectName(u"splitter_13")
        self.splitter_13.setOrientation(Qt.Orientation.Horizontal)
        self.label_decive = QLabel(self.splitter_13)
        self.label_decive.setObjectName(u"label_decive")
        self.label_decive.setMinimumSize(QSize(100, 30))
        self.label_decive.setMaximumSize(QSize(16777215, 16777215))
        self.label_decive.setFont(font7)
        self.splitter_13.addWidget(self.label_decive)
        self.line_device = QLineEdit(self.splitter_13)
        self.line_device.setObjectName(u"line_device")
        self.line_device.setMinimumSize(QSize(150, 30))
        self.line_device.setMaximumSize(QSize(150, 16777215))
        self.line_device.setFont(font7)
        self.line_device.setReadOnly(True)
        self.splitter_13.addWidget(self.line_device)

        self.gridLayout_7.addWidget(self.splitter_13, 1, 0, 1, 1)

        self.stacked_widget.addWidget(self.Hard)
        self.Prj = QWidget()
        self.Prj.setObjectName(u"Prj")
        self.gridLayout_8 = QGridLayout(self.Prj)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.splitter_2 = QSplitter(self.Prj)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_4 = QSplitter(self.splitter_2)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Horizontal)
        self.button_import_markdown = QPushButton(self.splitter_4)
        self.button_import_markdown.setObjectName(u"button_import_markdown")
        self.button_import_markdown.setMaximumSize(QSize(79, 24))
        self.splitter_4.addWidget(self.button_import_markdown)
        self.splitter_2.addWidget(self.splitter_4)

        self.gridLayout_8.addWidget(self.splitter_2, 1, 0, 1, 1)

        self.text_prj = QTextBrowser(self.Prj)
        self.text_prj.setObjectName(u"text_prj")
        self.text_prj.setMinimumSize(QSize(700, 0))
        self.text_prj.setMaximumSize(QSize(16777215, 16777215))
        font9 = QFont()
        font9.setFamilies([u"\u5b8b\u4f53"])
        font9.setPointSize(20)
        self.text_prj.setFont(font9)
        self.text_prj.setReadOnly(False)

        self.gridLayout_8.addWidget(self.text_prj, 2, 0, 1, 1)

        self.stacked_widget.addWidget(self.Prj)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_5 = QGridLayout(self.page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.splitter_5 = QSplitter(self.page)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Orientation.Horizontal)
        self.button_mcu_connect = QPushButton(self.splitter_5)
        self.button_mcu_connect.setObjectName(u"button_mcu_connect")
        self.button_mcu_connect.setMaximumSize(QSize(76, 24))
        self.splitter_5.addWidget(self.button_mcu_connect)
        self.button_mcu_scan = QPushButton(self.splitter_5)
        self.button_mcu_scan.setObjectName(u"button_mcu_scan")
        self.button_mcu_scan.setMaximumSize(QSize(79, 24))
        self.splitter_5.addWidget(self.button_mcu_scan)
        self.button_mcu_log = QPushButton(self.splitter_5)
        self.button_mcu_log.setObjectName(u"button_mcu_log")
        self.button_mcu_log.setMaximumSize(QSize(76, 24))
        self.splitter_5.addWidget(self.button_mcu_log)
        self.button_mcu_rx = QPushButton(self.splitter_5)
        self.button_mcu_rx.setObjectName(u"button_mcu_rx")
        self.button_mcu_rx.setMaximumSize(QSize(76, 24))
        self.splitter_5.addWidget(self.button_mcu_rx)
        self.line_test_interval = QLineEdit(self.splitter_5)
        self.line_test_interval.setObjectName(u"line_test_interval")
        self.line_test_interval.setMaximumSize(QSize(100, 16777215))
        self.splitter_5.addWidget(self.line_test_interval)
        self.label_4 = QLabel(self.splitter_5)
        self.label_4.setObjectName(u"label_4")
        self.splitter_5.addWidget(self.label_4)

        self.gridLayout_5.addWidget(self.splitter_5, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listView = QListView(self.page)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(314, 570))

        self.horizontalLayout_3.addWidget(self.listView)

        self.MCU_list_case = QListWidget(self.page)
        self.MCU_list_case.setObjectName(u"MCU_list_case")

        self.horizontalLayout_3.addWidget(self.MCU_list_case)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.stacked_widget.addWidget(self.page)

        self.gridLayout_4.addWidget(self.stacked_widget, 1, 0, 1, 1)

        self.log_widget = QWidget(MainForm)
        self.log_widget.setObjectName(u"log_widget")
        self.log_widget.setMinimumSize(QSize(980, 125))
        self.gridLayout_3 = QGridLayout(self.log_widget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter_3 = QSplitter(self.log_widget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.button_save = QPushButton(self.splitter_3)
        self.button_save.setObjectName(u"button_save")
        self.button_save.setMinimumSize(QSize(50, 25))
        self.button_save.setMaximumSize(QSize(100, 100))
        self.button_save.setFont(font)
        self.splitter_3.addWidget(self.button_save)
        self.button_clear = QPushButton(self.splitter_3)
        self.button_clear.setObjectName(u"button_clear")
        self.button_clear.setMinimumSize(QSize(50, 25))
        self.button_clear.setMaximumSize(QSize(100, 100))
        self.button_clear.setFont(font)
        self.splitter_3.addWidget(self.button_clear)

        self.gridLayout_3.addWidget(self.splitter_3, 5, 0, 1, 1)

        self.text_log = QPlainTextEdit(self.log_widget)
        self.text_log.setObjectName(u"text_log")
        self.text_log.setMinimumSize(QSize(0, 0))
        self.text_log.setFont(font6)
        self.text_log.setFrameShadow(QFrame.Shadow.Raised)
        self.text_log.setReadOnly(True)

        self.gridLayout_3.addWidget(self.text_log, 4, 0, 1, 1)


        self.gridLayout_4.addWidget(self.log_widget, 2, 0, 1, 1)


        self.retranslateUi(MainForm)

        self.stacked_widget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"SPI\u4e0a\u4f4d\u673a", None))
#if QT_CONFIG(tooltip)
        MainForm.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.button_message.setText(QCoreApplication.translate("MainForm", u"\u4fe1\u606f", None))
        self.button_pc_fpga.setText(QCoreApplication.translate("MainForm", u"PC-FPGA", None))
        self.button_pc_mcu.setText(QCoreApplication.translate("MainForm", u"PC-MCU", None))
        self.button_hard.setText(QCoreApplication.translate("MainForm", u"\u786c\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.stacked_widget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.Main.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.button_fold_log.setText(QCoreApplication.translate("MainForm", u">", None))
        self.button_new_prj.setText(QCoreApplication.translate("MainForm", u"\u65b0\u5efa", None))
        self.button_import_prj.setText(QCoreApplication.translate("MainForm", u"\u5bfc\u5165", None))
        self.label_3.setText(QCoreApplication.translate("MainForm", u"|", None))
        self.label.setText(QCoreApplication.translate("MainForm", u"\u6570\u636e\u96c6", None))
        self.button_rename.setText(QCoreApplication.translate("MainForm", u"\u91cd\u547d\u540d", None))
        self.button_add_data_group.setText(QCoreApplication.translate("MainForm", u"\u6dfb\u52a0", None))
        self.button_del_data_group.setText(QCoreApplication.translate("MainForm", u"\u5220\u9664", None))
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
        self.line_edit_data.setText("")
        self.button_send.setText(QCoreApplication.translate("MainForm", u"\u53d1\u9001", None))
        self.label_5.setText(QCoreApplication.translate("MainForm", u"\u5ef6\u65f6(s)", None))
        self.button_add_mode_group.setText(QCoreApplication.translate("MainForm", u"\u6dfb\u52a0", None))
        self.button_del_mode_group.setText(QCoreApplication.translate("MainForm", u"\u5220\u9664", None))
        self.button_del_select.setText(QCoreApplication.translate("MainForm", u"-", None))
        self.label_2.setText(QCoreApplication.translate("MainForm", u"\u6b21\u6570", None))
        self.radio_button_order.setText(QCoreApplication.translate("MainForm", u"\u987a\u5e8f\u6267\u884c", None))
        self.radio_button_circ.setText(QCoreApplication.translate("MainForm", u"\u5faa\u73af\u6267\u884c", None))
        self.radio_button_random.setText(QCoreApplication.translate("MainForm", u"\u968f\u673a\u6267\u884c", None))
#if QT_CONFIG(tooltip)
        self.check_box_mode_poll.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p>\u52fe\u9009\u540e\uff0c\u5faa\u73af\u548c\u987a\u5e8f\u6267\u884c\u7684\u76ee\u6807\u8f6c\u53d8\u4e3a\u5217\u8868\u4e2d\u6240\u6709\u7684\u6570\u636e\uff0c</p><p>\u6b64\u65f6\u7684\u8f93\u5165\u5ef6\u65f6\u4e3a\u7ec4\u95f4\u7684\u53d1\u9001\u95f4\u9694\uff0c\u7ec4\u5185\u6570\u636e\u53d1\u9001\u95f4\u9694\u56fa\u5b9a\u4e3a0.5s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.check_box_mode_poll.setText(QCoreApplication.translate("MainForm", u"\u7ec4\u95f4\u53d1\u9001", None))
        self.button_start.setText(QCoreApplication.translate("MainForm", u"\u542f\u52a8", None))
        self.button_stop.setText(QCoreApplication.translate("MainForm", u"\u7ec8\u6b62", None))
        self.label_s_or_q.setText(QCoreApplication.translate("MainForm", u"S/QSPI", None))
        self.button_receive.setText(QCoreApplication.translate("MainForm", u"\u53ea\u8bfb", None))
        self.label_io.setText(QCoreApplication.translate("MainForm", u"IO\u7535\u5e73", None))
        self.label_bit.setText(QCoreApplication.translate("MainForm", u"\u4f4d\u987a\u5e8f", None))
        self.label_clk.setText(QCoreApplication.translate("MainForm", u"\u65f6\u949f", None))
        self.label_speed.setText(QCoreApplication.translate("MainForm", u"SPI\u901f\u7387", None))
        self.label_vcc.setText(QCoreApplication.translate("MainForm", u"VCC\u7535\u538b", None))
        self.label_receive_size.setText(QCoreApplication.translate("MainForm", u"\u8bfb\u6570\u636e\u957f\u5ea6", None))
        self.check_box_receive.setText(QCoreApplication.translate("MainForm", u"\u8bfb\u6570\u636e", None))
        self.label_decive.setText(QCoreApplication.translate("MainForm", u"\u8bbe\u5907", None))
        self.button_import_markdown.setText(QCoreApplication.translate("MainForm", u"\u5bfc\u5165", None))
        self.text_prj.setHtml(QCoreApplication.translate("MainForm", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\u5b8b\u4f53'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Microsoft YaHei UI'; font-size:24pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Microsoft YaHei UI'; font-size:24pt;\"><br /></p></body></html>", None))
        self.button_mcu_connect.setText(QCoreApplication.translate("MainForm", u"\u8fde\u63a5", None))
        self.button_mcu_scan.setText(QCoreApplication.translate("MainForm", u"\u626b\u63cf", None))
        self.button_mcu_log.setText(QCoreApplication.translate("MainForm", u"\u8bf7\u6c42\u65e5\u5fd7", None))
        self.button_mcu_rx.setText(QCoreApplication.translate("MainForm", u"\u63a5\u6536\u6d4b\u8bd5", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainForm", u"<html><head/><body><p>\u8f93\u5165\u6846\u7528\u6765\u63a7\u5236\u8fde\u63a5\u548c\u626b\u63cf\u65f6\uff0cSPI\u8bf7\u6c42MCU\u65f6\u7684\u5199\u65f6\u5e8f\u548c\u56de\u8bfbMCU\u7684\u8bfb\u65f6\u5e8f\u95f4\u9694\uff0c\u9632\u6b62\u65f6\u95f4\u8fc7\u77ed\u5bfc\u81f4MCU\u65e0\u6cd5\u53ca\u65f6\u54cd\u5e94</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainForm", u"\uff01", None))
#if QT_CONFIG(tooltip)
        self.button_save.setToolTip(QCoreApplication.translate("MainForm", u"\u4fdd\u5b58", None))
#endif // QT_CONFIG(tooltip)
        self.button_save.setText(QCoreApplication.translate("MainForm", u"\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.button_clear.setToolTip(QCoreApplication.translate("MainForm", u"\u6e05\u9664", None))
#endif // QT_CONFIG(tooltip)
        self.button_clear.setText(QCoreApplication.translate("MainForm", u"\u6e05\u9664", None))
        self.text_log.setPlainText("")
    # retranslateUi

