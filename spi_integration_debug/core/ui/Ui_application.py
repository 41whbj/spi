# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'application.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from .CustomTreeWidget import CustomTreeWidget

class Ui_Application(object):
    def setupUi(self, Application):
        if not Application.objectName():
            Application.setObjectName(u"Application")
        Application.resize(853, 547)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Application.sizePolicy().hasHeightForWidth())
        Application.setSizePolicy(sizePolicy)
        Application.setMinimumSize(QSize(0, 0))
        Application.setMaximumSize(QSize(2000, 1000))
        self.gridLayout = QGridLayout(Application)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, -1, -1, 0)

        self.gridLayout.addLayout(self.horizontalLayout_13, 0, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.spi_config_widget = QWidget(Application)
        self.spi_config_widget.setObjectName(u"spi_config_widget")
        self.spi_config_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_12 = QHBoxLayout(self.spi_config_widget)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_decive = QLabel(self.spi_config_widget)
        self.label_decive.setObjectName(u"label_decive")
        self.label_decive.setMinimumSize(QSize(0, 0))
        self.label_decive.setMaximumSize(QSize(30, 20))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(10)
        self.label_decive.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_decive)

        self.line_device = QLineEdit(self.spi_config_widget)
        self.line_device.setObjectName(u"line_device")
        self.line_device.setMinimumSize(QSize(0, 0))
        self.line_device.setMaximumSize(QSize(95, 20))
        font1 = QFont()
        font1.setPointSize(9)
        self.line_device.setFont(font1)
        self.line_device.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.line_device)

        self.button_refresh = QPushButton(self.spi_config_widget)
        self.button_refresh.setObjectName(u"button_refresh")
        self.button_refresh.setMaximumSize(QSize(20, 16777215))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaylistRepeat))
        self.button_refresh.setIcon(icon)
        self.button_refresh.setIconSize(QSize(13, 13))

        self.horizontalLayout_12.addWidget(self.button_refresh)

        self.label_vcc = QLabel(self.spi_config_widget)
        self.label_vcc.setObjectName(u"label_vcc")
        self.label_vcc.setMinimumSize(QSize(0, 0))
        self.label_vcc.setMaximumSize(QSize(50, 20))
        self.label_vcc.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_vcc)

        self.combo_box_vcc = QComboBox(self.spi_config_widget)
        self.combo_box_vcc.setObjectName(u"combo_box_vcc")
        self.combo_box_vcc.setMinimumSize(QSize(0, 0))
        self.combo_box_vcc.setMaximumSize(QSize(57, 20))
        self.combo_box_vcc.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_vcc)

        self.label_io = QLabel(self.spi_config_widget)
        self.label_io.setObjectName(u"label_io")
        self.label_io.setMinimumSize(QSize(0, 0))
        self.label_io.setMaximumSize(QSize(40, 20))
        self.label_io.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_io)

        self.combo_box_io = QComboBox(self.spi_config_widget)
        self.combo_box_io.setObjectName(u"combo_box_io")
        self.combo_box_io.setMinimumSize(QSize(0, 0))
        self.combo_box_io.setMaximumSize(QSize(60, 20))
        self.combo_box_io.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_io)

        self.label_speed = QLabel(self.spi_config_widget)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setMinimumSize(QSize(0, 0))
        self.label_speed.setMaximumSize(QSize(50, 20))
        self.label_speed.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_speed)

        self.combo_box_speed = QComboBox(self.spi_config_widget)
        self.combo_box_speed.setObjectName(u"combo_box_speed")
        self.combo_box_speed.setMinimumSize(QSize(0, 0))
        self.combo_box_speed.setMaximumSize(QSize(80, 20))
        self.combo_box_speed.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_speed)

        self.label_clk = QLabel(self.spi_config_widget)
        self.label_clk.setObjectName(u"label_clk")
        self.label_clk.setMinimumSize(QSize(0, 0))
        self.label_clk.setMaximumSize(QSize(30, 20))
        self.label_clk.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_clk)

        self.combo_box_clk = QComboBox(self.spi_config_widget)
        self.combo_box_clk.setObjectName(u"combo_box_clk")
        self.combo_box_clk.setMinimumSize(QSize(0, 0))
        self.combo_box_clk.setMaximumSize(QSize(100, 20))
        self.combo_box_clk.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_clk)

        self.label_bit = QLabel(self.spi_config_widget)
        self.label_bit.setObjectName(u"label_bit")
        self.label_bit.setMinimumSize(QSize(0, 0))
        self.label_bit.setMaximumSize(QSize(40, 20))
        self.label_bit.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_bit)

        self.combo_box_bit = QComboBox(self.spi_config_widget)
        self.combo_box_bit.setObjectName(u"combo_box_bit")
        self.combo_box_bit.setMinimumSize(QSize(0, 0))
        self.combo_box_bit.setMaximumSize(QSize(60, 20))
        self.combo_box_bit.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_bit)

        self.label_s_or_q = QLabel(self.spi_config_widget)
        self.label_s_or_q.setObjectName(u"label_s_or_q")
        self.label_s_or_q.setMinimumSize(QSize(0, 0))
        self.label_s_or_q.setMaximumSize(QSize(40, 20))
        self.label_s_or_q.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_s_or_q)

        self.combo_box_s_or_q = QComboBox(self.spi_config_widget)
        self.combo_box_s_or_q.setObjectName(u"combo_box_s_or_q")
        self.combo_box_s_or_q.setMinimumSize(QSize(0, 0))
        self.combo_box_s_or_q.setMaximumSize(QSize(100, 20))
        self.combo_box_s_or_q.setFont(font1)

        self.horizontalLayout_12.addWidget(self.combo_box_s_or_q)

        self.checkBox_self_test = QCheckBox(self.spi_config_widget)
        self.checkBox_self_test.setObjectName(u"checkBox_self_test")
        self.checkBox_self_test.setFont(font)

        self.horizontalLayout_12.addWidget(self.checkBox_self_test)


        self.horizontalLayout_8.addWidget(self.spi_config_widget)


        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.button_start = QPushButton(Application)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setMinimumSize(QSize(0, 0))
        self.button_start.setMaximumSize(QSize(231, 25))
        self.button_start.setFont(font)

        self.horizontalLayout_10.addWidget(self.button_start)

        self.button_stop = QPushButton(Application)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setMinimumSize(QSize(0, 0))
        self.button_stop.setMaximumSize(QSize(168, 25))
        self.button_stop.setFont(font)

        self.horizontalLayout_10.addWidget(self.button_stop)


        self.gridLayout_2.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(Application)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(48, 25))

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.line_prj_name = QLineEdit(Application)
        self.line_prj_name.setObjectName(u"line_prj_name")
        self.line_prj_name.setMinimumSize(QSize(90, 0))
        self.line_prj_name.setMaximumSize(QSize(90, 16777215))

        self.gridLayout_3.addWidget(self.line_prj_name, 0, 1, 1, 1)

        self.button_new_prj = QPushButton(Application)
        self.button_new_prj.setObjectName(u"button_new_prj")
        self.button_new_prj.setMinimumSize(QSize(0, 25))
        self.button_new_prj.setMaximumSize(QSize(60, 16777215))
        font2 = QFont()
        font2.setFamilies([u"\u5b8b\u4f53"])
        font2.setPointSize(9)
        self.button_new_prj.setFont(font2)

        self.gridLayout_3.addWidget(self.button_new_prj, 0, 2, 1, 1)

        self.button_import_prj = QPushButton(Application)
        self.button_import_prj.setObjectName(u"button_import_prj")
        self.button_import_prj.setMinimumSize(QSize(0, 25))
        self.button_import_prj.setMaximumSize(QSize(60, 16777215))
        self.button_import_prj.setFont(font2)

        self.gridLayout_3.addWidget(self.button_import_prj, 0, 3, 1, 1)

        self.label_3 = QLabel(Application)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16, 19))

        self.gridLayout_3.addWidget(self.label_3, 0, 4, 1, 1)

        self.label = QLabel(Application)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 25))
        self.label.setMaximumSize(QSize(45, 25))
        self.label.setFont(font)

        self.gridLayout_3.addWidget(self.label, 0, 5, 1, 1)

        self.combo_box_data_group = QComboBox(Application)
        self.combo_box_data_group.setObjectName(u"combo_box_data_group")
        self.combo_box_data_group.setMinimumSize(QSize(100, 25))

        self.gridLayout_3.addWidget(self.combo_box_data_group, 0, 6, 1, 1)

        self.button_rename = QPushButton(Application)
        self.button_rename.setObjectName(u"button_rename")
        self.button_rename.setMinimumSize(QSize(0, 25))
        self.button_rename.setMaximumSize(QSize(60, 16777215))
        self.button_rename.setFont(font2)

        self.gridLayout_3.addWidget(self.button_rename, 0, 7, 1, 1)

        self.button_add_data_group = QPushButton(Application)
        self.button_add_data_group.setObjectName(u"button_add_data_group")
        self.button_add_data_group.setMinimumSize(QSize(0, 25))
        self.button_add_data_group.setMaximumSize(QSize(60, 16777215))
        self.button_add_data_group.setFont(font2)

        self.gridLayout_3.addWidget(self.button_add_data_group, 0, 8, 1, 1)

        self.button_del_data_group = QPushButton(Application)
        self.button_del_data_group.setObjectName(u"button_del_data_group")
        self.button_del_data_group.setMinimumSize(QSize(0, 25))
        self.button_del_data_group.setMaximumSize(QSize(60, 16777215))
        self.button_del_data_group.setFont(font2)

        self.gridLayout_3.addWidget(self.button_del_data_group, 0, 9, 1, 1)

        self.gridLayout_3.setColumnStretch(5, 1)

        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 2)

        self.list_data = QListWidget(Application)
        self.list_data.setObjectName(u"list_data")
        self.list_data.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"Microsoft YaHei"])
        font3.setPointSize(20)
        self.list_data.setFont(font3)

        self.gridLayout_4.addWidget(self.list_data, 1, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.line_data = QLineEdit(Application)
        self.line_data.setObjectName(u"line_data")
        self.line_data.setMinimumSize(QSize(0, 30))
        self.line_data.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setFamilies([u"Times New Roman"])
        font4.setPointSize(12)
        self.line_data.setFont(font4)

        self.horizontalLayout_11.addWidget(self.line_data)

        self.button_send = QPushButton(Application)
        self.button_send.setObjectName(u"button_send")
        self.button_send.setMinimumSize(QSize(0, 30))
        self.button_send.setMaximumSize(QSize(80, 16777215))
        self.button_send.setFont(font)

        self.horizontalLayout_11.addWidget(self.button_send)

        self.label_6 = QLabel(Application)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setTextFormat(Qt.TextFormat.AutoText)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_6)

        self.button_receive = QPushButton(Application)
        self.button_receive.setObjectName(u"button_receive")
        self.button_receive.setMinimumSize(QSize(0, 0))
        self.button_receive.setMaximumSize(QSize(80, 30))

        self.horizontalLayout_11.addWidget(self.button_receive)

        self.splitter = QSplitter(Application)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label_receive_size = QLabel(self.splitter)
        self.label_receive_size.setObjectName(u"label_receive_size")
        self.label_receive_size.setMinimumSize(QSize(0, 30))
        self.label_receive_size.setMaximumSize(QSize(55, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_receive_size.setFont(font5)
        self.splitter.addWidget(self.label_receive_size)
        self.combo_box_size = QComboBox(self.splitter)
        self.combo_box_size.setObjectName(u"combo_box_size")
        self.combo_box_size.setMinimumSize(QSize(0, 30))
        self.combo_box_size.setMaximumSize(QSize(75, 30))
        font6 = QFont()
        font6.setPointSize(10)
        self.combo_box_size.setFont(font6)
        self.splitter.addWidget(self.combo_box_size)

        self.horizontalLayout_11.addWidget(self.splitter)


        self.gridLayout_4.addLayout(self.horizontalLayout_11, 3, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_add = QPushButton(Application)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(25, 25))
        self.button_add.setMaximumSize(QSize(25, 16777215))
        self.button_add.setFont(font6)

        self.verticalLayout_2.addWidget(self.button_add)

        self.button_det = QPushButton(Application)
        self.button_det.setObjectName(u"button_det")
        self.button_det.setMinimumSize(QSize(25, 25))
        self.button_det.setMaximumSize(QSize(25, 16777215))
        self.button_det.setFont(font6)

        self.verticalLayout_2.addWidget(self.button_det)

        self.button_crc = QPushButton(Application)
        self.button_crc.setObjectName(u"button_crc")
        self.button_crc.setMinimumSize(QSize(25, 25))
        self.button_crc.setMaximumSize(QSize(25, 16777215))

        self.verticalLayout_2.addWidget(self.button_crc)

        self.button_function_config = QPushButton(Application)
        self.button_function_config.setObjectName(u"button_function_config")
        self.button_function_config.setMinimumSize(QSize(25, 25))
        self.button_function_config.setMaximumSize(QSize(25, 25))
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.button_function_config.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.button_function_config)

        self.button_fold_config = QPushButton(Application)
        self.button_fold_config.setObjectName(u"button_fold_config")
        self.button_fold_config.setMaximumSize(QSize(25, 25))
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaFlash))
        self.button_fold_config.setIcon(icon2)

        self.verticalLayout_2.addWidget(self.button_fold_config)

        self.pushButton_log = QPushButton(Application)
        self.pushButton_log.setObjectName(u"pushButton_log")
        self.pushButton_log.setMinimumSize(QSize(25, 25))
        self.pushButton_log.setMaximumSize(QSize(25, 25))
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewFullscreen))
        self.pushButton_log.setIcon(icon3)

        self.verticalLayout_2.addWidget(self.pushButton_log)

        self.verticalSpacer = QSpacerItem(22, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_4)

        self.widget_log = QWidget(Application)
        self.widget_log.setObjectName(u"widget_log")
        self.gridLayout_6 = QGridLayout(self.widget_log)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.listWidget_log_normal = QListWidget(self.widget_log)
        self.listWidget_log_normal.setObjectName(u"listWidget_log_normal")
        self.listWidget_log_normal.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_6.addWidget(self.listWidget_log_normal, 1, 0, 1, 1)

        self.listWidget_log = QListWidget(self.widget_log)
        self.listWidget_log.setObjectName(u"listWidget_log")
        self.listWidget_log.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.listWidget_log, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.widget_log)

        self.verticalLayout_3.setStretch(0, 10)
        self.verticalLayout_3.setStretch(1, 3)

        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 1, 6, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(Application)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(56, 0))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_2)

        self.line_number = QLineEdit(Application)
        self.line_number.setObjectName(u"line_number")
        self.line_number.setMinimumSize(QSize(0, 0))
        self.line_number.setMaximumSize(QSize(205, 25))
        self.line_number.setFont(font6)

        self.horizontalLayout_9.addWidget(self.line_number)


        self.gridLayout_2.addLayout(self.horizontalLayout_9, 4, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(Application)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(56, 0))
        self.label_5.setMaximumSize(QSize(16777215, 16777215))
        self.label_5.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.line_delay = QLineEdit(Application)
        self.line_delay.setObjectName(u"line_delay")
        self.line_delay.setMinimumSize(QSize(0, 0))
        self.line_delay.setMaximumSize(QSize(205, 25))
        self.line_delay.setFont(font6)

        self.horizontalLayout_7.addWidget(self.line_delay)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.button_add_test_group = QPushButton(Application)
        self.button_add_test_group.setObjectName(u"button_add_test_group")
        self.button_add_test_group.setMaximumSize(QSize(65, 25))
        self.button_add_test_group.setFont(font2)

        self.horizontalLayout_5.addWidget(self.button_add_test_group)

        self.button_del_test_group = QPushButton(Application)
        self.button_del_test_group.setObjectName(u"button_del_test_group")
        self.button_del_test_group.setMaximumSize(QSize(65, 25))
        self.button_del_test_group.setFont(font2)

        self.horizontalLayout_5.addWidget(self.button_del_test_group)

        self.check_box_select_all = QCheckBox(Application)
        self.check_box_select_all.setObjectName(u"check_box_select_all")

        self.horizontalLayout_5.addWidget(self.check_box_select_all)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(Application)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.check_box_mode_poll = QCheckBox(Application)
        self.check_box_mode_poll.setObjectName(u"check_box_mode_poll")
        self.check_box_mode_poll.setMaximumSize(QSize(80, 16777215))
        self.check_box_mode_poll.setFont(font)

        self.horizontalLayout_2.addWidget(self.check_box_mode_poll)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.tree_group = CustomTreeWidget(Application)
        self.tree_group.setObjectName(u"tree_group")
        self.tree_group.setMinimumSize(QSize(250, 0))
        self.tree_group.setMaximumSize(QSize(16777215, 16777215))
        font7 = QFont()
        font7.setFamilies([u"Microsoft YaHei"])
        font7.setPointSize(9)
        self.tree_group.setFont(font7)
        self.tree_group.setStyleSheet(u"")
        self.tree_group.setColumnCount(0)

        self.gridLayout_2.addWidget(self.tree_group, 1, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 1)


        self.retranslateUi(Application)

        QMetaObject.connectSlotsByName(Application)
    # setupUi

    def retranslateUi(self, Application):
        Application.setWindowTitle(QCoreApplication.translate("Application", u"SPI\u4e0a\u4f4d\u673a", None))
#if QT_CONFIG(tooltip)
        Application.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_decive.setText(QCoreApplication.translate("Application", u"\u8bbe\u5907", None))
        self.button_refresh.setText("")
        self.label_vcc.setText(QCoreApplication.translate("Application", u"VCC\u7535\u538b", None))
        self.label_io.setText(QCoreApplication.translate("Application", u"IO\u7535\u5e73", None))
        self.label_speed.setText(QCoreApplication.translate("Application", u"SPI\u901f\u7387", None))
        self.label_clk.setText(QCoreApplication.translate("Application", u"\u65f6\u949f", None))
        self.label_bit.setText(QCoreApplication.translate("Application", u"\u4f4d\u987a\u5e8f", None))
        self.label_s_or_q.setText(QCoreApplication.translate("Application", u"S/QSPI", None))
        self.checkBox_self_test.setText(QCoreApplication.translate("Application", u"\u81ea\u6d4b", None))
        self.button_start.setText(QCoreApplication.translate("Application", u"\u542f\u52a8", None))
        self.button_stop.setText(QCoreApplication.translate("Application", u"\u7ec8\u6b62", None))
        self.label_8.setText(QCoreApplication.translate("Application", u"\u9879\u76ee\u540d\u79f0", None))
        self.button_new_prj.setText(QCoreApplication.translate("Application", u"\u65b0\u5efa", None))
        self.button_import_prj.setText(QCoreApplication.translate("Application", u"\u5bfc\u5165", None))
        self.label_3.setText(QCoreApplication.translate("Application", u"|", None))
        self.label.setText(QCoreApplication.translate("Application", u"\u6570\u636e\u96c6", None))
        self.button_rename.setText(QCoreApplication.translate("Application", u"\u91cd\u547d\u540d", None))
        self.button_add_data_group.setText(QCoreApplication.translate("Application", u"\u6dfb\u52a0", None))
        self.button_del_data_group.setText(QCoreApplication.translate("Application", u"\u5220\u9664", None))
        self.line_data.setText("")
        self.button_send.setText(QCoreApplication.translate("Application", u"\u53d1\u9001", None))
        self.label_6.setText(QCoreApplication.translate("Application", u"|", None))
        self.button_receive.setText(QCoreApplication.translate("Application", u"\u53ea\u8bfb", None))
        self.label_receive_size.setText(QCoreApplication.translate("Application", u"\u53ea\u8bfb\u957f\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.button_add.setToolTip(QCoreApplication.translate("Application", u"\u6dfb\u52a0\u6570\u636e", None))
#endif // QT_CONFIG(tooltip)
        self.button_add.setText(QCoreApplication.translate("Application", u"+", None))
#if QT_CONFIG(tooltip)
        self.button_det.setToolTip(QCoreApplication.translate("Application", u"\u5220\u9664\u6570\u636e", None))
#endif // QT_CONFIG(tooltip)
        self.button_det.setText(QCoreApplication.translate("Application", u"-", None))
#if QT_CONFIG(tooltip)
        self.button_crc.setToolTip(QCoreApplication.translate("Application", u"CRC\u68c0\u9a8c", None))
#endif // QT_CONFIG(tooltip)
        self.button_crc.setText(QCoreApplication.translate("Application", u"C", None))
        self.button_function_config.setText("")
        self.button_fold_config.setText("")
        self.pushButton_log.setText("")
        self.label_2.setText(QCoreApplication.translate("Application", u"\u6b21\u6570", None))
#if QT_CONFIG(tooltip)
        self.line_number.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Application", u"\u5ef6\u65f6(s)", None))
        self.button_add_test_group.setText(QCoreApplication.translate("Application", u"\u6dfb\u52a0", None))
        self.button_del_test_group.setText(QCoreApplication.translate("Application", u"\u5220\u9664", None))
        self.check_box_select_all.setText(QCoreApplication.translate("Application", u"\u5168\u9009", None))
        self.label_4.setText(QCoreApplication.translate("Application", u"\u5faa\u73af\u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.check_box_mode_poll.setToolTip(QCoreApplication.translate("Application", u"<html><head/><body><p>\u52fe\u9009\u540e\uff0c\u5faa\u73af\u548c\u987a\u5e8f\u6267\u884c\u7684\u76ee\u6807\u8f6c\u53d8\u4e3a\u5217\u8868\u4e2d\u6240\u6709\u7684\u6570\u636e\uff0c</p><p>\u6b64\u65f6\u7684\u8f93\u5165\u5ef6\u65f6\u4e3a\u7ec4\u95f4\u7684\u53d1\u9001\u95f4\u9694\uff0c\u7ec4\u5185\u6570\u636e\u53d1\u9001\u95f4\u9694\u56fa\u5b9a\u4e3a0.1s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.check_box_mode_poll.setText(QCoreApplication.translate("Application", u"\u7ec4\u95f4\u53d1\u9001", None))
    # retranslateUi

