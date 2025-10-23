# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_function_config.ui'
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
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1102, 376)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.check_box_formula = QCheckBox(Form)
        self.check_box_formula.setObjectName(u"check_box_formula")

        self.gridLayout.addWidget(self.check_box_formula, 4, 0, 1, 1)

        self.line_addr_input = QLineEdit(Form)
        self.line_addr_input.setObjectName(u"line_addr_input")
        self.line_addr_input.setMinimumSize(QSize(0, 25))
        self.line_addr_input.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.line_addr_input, 2, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.button_config = QPushButton(Form)
        self.button_config.setObjectName(u"button_config")
        self.button_config.setMinimumSize(QSize(0, 40))
        self.button_config.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.button_config, 14, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 15, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 48, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 2)

        self.check_box_record = QCheckBox(Form)
        self.check_box_record.setObjectName(u"check_box_record")

        self.gridLayout.addWidget(self.check_box_record, 3, 0, 1, 1)

        self.line_function_input = QLineEdit(Form)
        self.line_function_input.setObjectName(u"line_function_input")
        self.line_function_input.setMinimumSize(QSize(0, 25))
        self.line_function_input.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.line_function_input, 2, 1, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.formula_widget = QWidget(Form)
        self.formula_widget.setObjectName(u"formula_widget")
        self.formula_widget.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.formula_widget)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_4 = QLabel(self.formula_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))

        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_3 = QLabel(self.formula_widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.combo_box_var = QComboBox(self.formula_widget)
        self.combo_box_var.setObjectName(u"combo_box_var")

        self.gridLayout_2.addWidget(self.combo_box_var, 5, 1, 1, 1)

        self.line_var_input = QLineEdit(self.formula_widget)
        self.line_var_input.setObjectName(u"line_var_input")
        self.line_var_input.setMinimumSize(QSize(0, 25))

        self.gridLayout_2.addWidget(self.line_var_input, 3, 0, 1, 1)

        self.line_range_val_input = QLineEdit(self.formula_widget)
        self.line_range_val_input.setObjectName(u"line_range_val_input")
        self.line_range_val_input.setMinimumSize(QSize(0, 25))
        self.line_range_val_input.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.line_range_val_input, 3, 1, 1, 1)

        self.line_formula_input = QLineEdit(self.formula_widget)
        self.line_formula_input.setObjectName(u"line_formula_input")
        self.line_formula_input.setMinimumSize(QSize(0, 25))
        self.line_formula_input.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.line_formula_input, 7, 0, 1, 2)

        self.label_5 = QLabel(self.formula_widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 20))

        self.gridLayout_2.addWidget(self.label_5, 2, 1, 1, 1)

        self.label_6 = QLabel(self.formula_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 20))

        self.gridLayout_2.addWidget(self.label_6, 4, 1, 1, 1)

        self.check_box_var_mode = QCheckBox(self.formula_widget)
        self.check_box_var_mode.setObjectName(u"check_box_var_mode")
        self.check_box_var_mode.setMinimumSize(QSize(0, 20))

        self.gridLayout_2.addWidget(self.check_box_var_mode, 4, 0, 1, 1)


        self.gridLayout.addWidget(self.formula_widget, 13, 0, 1, 2)

        self.check_box_sign = QCheckBox(Form)
        self.check_box_sign.setObjectName(u"check_box_sign")

        self.gridLayout.addWidget(self.check_box_sign, 5, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.tree_config = QTreeWidget(Form)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_config.setHeaderItem(__qtreewidgetitem)
        self.tree_config.setObjectName(u"tree_config")
        font = QFont()
        font.setPointSize(10)
        self.tree_config.setFont(font)
        self.tree_config.setLineWidth(1)

        self.gridLayout_3.addWidget(self.tree_config, 0, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u529f\u80fd\u914d\u7f6e\u7a97\u53e3", None))
        self.check_box_formula.setText(QCoreApplication.translate("Form", u"\u914d\u7f6e\u8868\u8fbe\u5f0f", None))
        self.line_addr_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u793a\u4f8b\uff1a0a", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5730\u5740", None))
        self.button_config.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u914d\u7f6e", None))
        self.check_box_record.setText(QCoreApplication.translate("Form", u"\u8bb0\u5f55\u5f00\u542f", None))
        self.line_function_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u793a\u4f8b\uff1a\u9971\u548c\u5ea6\u7b97\u6cd5", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7b97\u6cd5\u529f\u80fd", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u8868\u8fbe\u5f0f", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u8f93\u5165\u53c2\u6570\u540d\u79f0", None))
        self.line_var_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u793a\u4f8b:\u9971\u548c\u5ea6", None))
        self.line_range_val_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u793a\u4f8b\uff1a[1,2]", None))
        self.line_formula_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u793a\u4f8b\uff1a64*(\u9971\u548c\u5ea6-1)", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u53d6\u503c\u8303\u56f4", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u53ef\u7528\u53c2\u6570", None))
        self.check_box_var_mode.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u989d\u5916\u53c2\u6570", None))
        self.check_box_sign.setText(QCoreApplication.translate("Form", u"\u7b26\u53f7\u4f4d\u5f00\u542f", None))
    # retranslateUi

