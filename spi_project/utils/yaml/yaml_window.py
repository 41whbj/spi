#!/usr/bin/env python3.13
"""
filename: yaml_window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-25
description: YAML连接主窗口，处理YAML相关的UI连接和业务逻辑
"""

import yaml
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox
from .yaml_template import YAMLTemplate


class YAMLWindow(QObject):
    """
    YAML连接主窗口类，处理YAML相关的UI连接和业务逻辑
    """

    def __init__(self, application):
        """
        初始化YAML连接主窗口
        
        Args:
            application: 应用程序实例
        """
        super().__init__()
        self.application = application
        self.ui = application.ui
        self.file_path = None
        self.setup_connections()

    def setup_connections(self):
        """
        设置YAML相关控件的连接信号槽
        """
        self.ui.button_new_prj.clicked.connect(self.create_new_prj)
        self.ui.button_import_prj.clicked.connect(self.import_prj)
        self.ui.line_prj_name.editingFinished.connect(self.update_project_name)

    def create_new_prj(self):
        """
        创建新的YAML项目
        """
        
        # 弹出确认对话框，询问用户是否创建新项目
        reply = QMessageBox.information(
            self.application,
            "提示",
            "创建新项目将清空当前数据，是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # 如果用户选择否，则返回不执行任何操作
        if reply == QMessageBox.StandardButton.No:
            return
        
        # 清空所有现有数据
        self.clear_all()

        # 获取默认的YAML模板数据
        default_data = YAMLTemplate.create_template()

        # 打开文件保存对话框，让用户选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self.application,
            "保存新项目",
            "新建项目.yml",
            "YAML Files (*.yml *.yaml)"
        )

        # 如果用户选择了保存路径，则保存文件
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(
                    default_data, 
                    file, 
                    allow_unicode=True, 
                    default_flow_style=False,
                    sort_keys=False
                )
        
        # 保存文件路径
        self.file_path = file_path

        # 设置默认的数据组和测试组
        default_data_group = {'默认组': {'data': []}}
        default_test_group = {'新建分组1': []}

        # # 初始化测试组和数据组管理器
        self.application.test_group_window.test_group_manager.set_test_group(default_test_group)
        self.application.data_group_window.data_group_manager.set_data_group(default_data_group)

        self.ui.line_prj_name.setText(default_data['project_name'])

    def import_prj(self):
        """
        导入YAML项目
        """
        # 弹出确认对话框，询问用户是否导入项目
        reply = QMessageBox.information(
            self.application,
            "提示",
            "导入文件将清空当前数据，是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # 如果用户选择否，则返回不执行任何操作
        if reply == QMessageBox.StandardButton.No:
            return
        
        # 清空所有现有数据
        self.clear_all()

        # 打开文件选择对话框，让用户选择要导入的项目文件
        file_path, _ = QFileDialog.getOpenFileName(
            self.application,
            "导入项目",
            "",
            "YAML Files (*.yml *.yaml)"
        )

        # 如果用户没有选择文件，则返回
        if file_path is None:
            return
        
        # 保存文件路径
        self.file_path = file_path

        # 读取选定的YAML文件
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # 如果配置中包含项目名称，则设置到界面中
        if 'project_name' in config:
            self.ui.line_prj_name.setText(config['project_name'])

        # 如果配置中包含SPI配置，则设置到界面中
        if 'spi_config' in config:
            spi_config = config['spi_config']
            if 'vcc' in spi_config:
                index = self.ui.combo_box_vcc.findText(spi_config['vcc'])
                if index >= 0:
                    self.ui.combo_box_vcc.setCurrentIndex(index)
            if 'io' in spi_config:
                index = self.ui.combo_box_io.findText(spi_config['io'])
                if index >= 0:
                    self.ui.combo_box_io.setCurrentIndex(index)
            if 'speed' in spi_config:
                index = self.ui.combo_box_speed.findText(spi_config['speed'])
                if index >= 0:
                    self.ui.combo_box_speed.setCurrentIndex(index)
            if 'clk' in spi_config:
                index = self.ui.combo_box_clk.findText(spi_config['clk'])
                if index >= 0:
                    self.ui.combo_box_clk.setCurrentIndex(index)
            if 'bit' in spi_config:
                index = self.ui.combo_box_bit.findText(spi_config['bit'])
                if index >= 0:
                    self.ui.combo_box_bit.setCurrentIndex(index)
            if 'rx_size' in spi_config:
                index = self.ui.combo_box_size.findText(spi_config['rx_size'])
                if index >= 0:
                    self.ui.combo_box_size.setCurrentIndex(index)

        # 转换数据格式以适应 set_data_group 方法
        data_group = {}
        for group_name, group_content in config['data_group'].items():
            # 将字典格式转换为元组列表
            converted_data = []
            if 'data' in group_content:
                for item in group_content['data']:
                    # 将字典转换为元组
                    converted_data.append((item['name'], item['data']))

            data_group[group_name] = {'data': converted_data}
        
        # 使用 set_data_group 方法设置数据
        self.application.data_group_window.data_group_manager.set_data_group(data_group)


        # 转换数据格式以适应 set_test_group 方法
        test_group = {}
        for group_name, items in config['test_group'].items():
            # 将字典格式转换为元组列表
            converted_items = []
            for item in items:
                # 将字典转换为元组
                converted_items.append((item['name'], item['data']))
            
            test_group[group_name] = converted_items
        
        # 使用 set_test_group 方法设置数据
        self.application.test_group_window.test_group_manager.set_test_group(test_group)
        
        self.application.test_group_window.select_all_changed(Qt.Checked)

        self.application.ui.check_box_select_all.setChecked(True)

    def update_project_name(self):
        """
        更新项目名称
        """

        project_name = self.ui.line_prj_name.text()

        if not project_name:
            QMessageBox.warning(self.application, "警告", "项目名称不能为空")
            return
        
        # 读取现有的YAML文件内容
        with open(self.file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file) or {}
        
        # 更新project_name字段
        yaml_data['project_name'] = self.ui.line_prj_name.text()
        
        # 写回YAML文件
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(
                yaml_data, 
                file, 
                allow_unicode=True, 
                default_flow_style=False,
                sort_keys=False
            )

        self.update_spi_config()

    def update_spi_config(self):
        """
        更新SPI配置到YAML文件
        """
        # 检查是否有有效的文件路径
        if self.file_path is None:
            return

        # 读取现有的YAML文件内容
        with open(self.file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file) or {}

        # 更新SPI配置
        yaml_data['spi_config'] = {
            'vcc': self.ui.combo_box_vcc.currentText(),
            'io': self.ui.combo_box_io.currentText(),
            'speed': self.ui.combo_box_speed.currentText(),
            'clk': self.ui.combo_box_clk.currentText(),
            'bit': self.ui.combo_box_bit.currentText(),
            'rx_size': self.ui.combo_box_size.currentText(),
        }

        # print(f"yaml类中当前spi配置: {yaml_data['spi_config']}")

        # 将更新后的配置写回YAML文件
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(
                yaml_data, 
                file, 
                allow_unicode=True, 
                default_flow_style=False,
                sort_keys=False
            )

    def update_data_group(self):
        """
        更新数据组
        """

        data_group = self.application.data_group_window.data_group_manager.get_data_group_manager()

        # print(f"yaml类中当前数据组管理器内容: {data_group}")

        if self.file_path is None:
            return

        if not data_group:
            return
        
         # 读取现有的YAML文件内容
        with open(self.file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file) or {}
        
        # 准备要保存的数据组数据
        # 需要将元组转换为列表以便正确保存到YAML
        converted_data_group = {}
        for group_name, group_content in data_group.items():
            converted_data = []
            if 'data' in group_content:
                for item in group_content['data']:
                    if isinstance(item, tuple):
                        # 将元组转换为字典格式
                        converted_data.append({
                            'name': item[0],
                            'data': item[1]
                        })
            
            converted_data_group[group_name] = {
                'data': converted_data
            }
        
        # 更新data_group字段
        yaml_data['data_group'] = converted_data_group
        
        # 写回YAML文件
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(
                yaml_data, 
                file, 
                allow_unicode=True, 
                default_flow_style=False,
                sort_keys=False
            )

        self.update_spi_config()
            
        # print(f"数据组已保存到 {self.file_path}")

    def update_test_group(self):
        """
        更新测试组
        """

        # 检查是否有有效的文件路径
        if self.file_path is None:
            return

        # 读取现有的YAML文件内容
        with open(self.file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file) or {}

        # print("测试程序运行到此处")

        # 获取测试组管理器中的所有测试组数据
        test_group_data = self.application.test_group_window.test_group_manager.get_test_group_manager()

        # print(f"yaml类中当前测试组管理器内容: {test_group_data}")

        # 构造测试组配置
        test_group = {}
        for group_name, items in test_group_data.items():
            test_group[group_name] = []
            for item in items:
                if isinstance(item, tuple) and len(item) >= 2:
                    # 将元组转换为包含 name 和 data 字段的字典
                    test_group[group_name].append({
                        'name': item[0],
                        'data': item[1]
                    })

        # 更新YAML数据中的测试组部分
        yaml_data['test_group'] = test_group

        # print(f"yaml类中当前测试组内容: {test_group}")

        # 将更新后的配置写回YAML文件
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(
                yaml_data, 
                file, 
                allow_unicode=True, 
                default_flow_style=False,
                sort_keys=False
            )

        self.update_spi_config()

    def clear_all(self):
        """
        清空所有界面数据
        """
        self.ui.line_prj_name.clear()
        self.ui.combo_box_data_group.clear()
        self.ui.tree_group.clear()
        self.ui.list_data.clear()