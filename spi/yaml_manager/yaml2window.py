#!/usr/bin/env python3.13
"""
filename: yaml2window.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-04
description: YAML connection main window, handling YAML related UI connections and logic
"""

import yaml
import os
from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox
from .yaml_new import YAMLNew


class YAML2Window(QObject):
    """
        YAML connection main window class, 
        handling YAML related UI connections and business logic
    """
    
    def __init__(self, main_window):
        """
            Initialize the YAML connection main window
            
            Args:
                main_window: The main window instance
        """
        super().__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.file_path = None
        self.setup_connections()
        self.save_timer()

    def setup_connections(self):
        """
            Set up connections for YAML related controls
        """

        self.ui.button_new_prj.clicked.connect(self.create_new_prj)
        self.ui.button_import_prj.clicked.connect(self.import_prj)

    def save_timer(self):
        """
            Save YAML project
        """

        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.yaml_auto_save)
        self.auto_save_timer.start(1000)
        

    def create_new_prj(self):
        """
            Create new YAML project
        """

        reply = QMessageBox.information(
            self.main_window,
            "提示",
            "创建新项目将清空当前数据，是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return
        
        self.clear_all()

        default_data = YAMLNew.create_yaml()

        # print(f"[INFO] 新项目数据: {default_data}")


        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "保存新项目",
            "新建项目.yml",
            "YAML Files (*.yml *.yaml)"
        )

        # print(f"[INFO] 新项目路径: {file_path}")

        if file_path:
            class OrderedDumper(yaml.Dumper):
                    def represent_dict(self, data):
                        return self.represent_mapping('tag:yaml.org,2002:map', data.items())
                
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    default_data, 
                    f, 
                    Dumper=OrderedDumper,
                    allow_unicode=True, 
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                    width=80,
                    encoding='utf-8'
                )
        
            # print(f"[INFO] 新项目已保存至: {file_path}")

        self.file_path = file_path

        default_data_group = {'默认组': {'data': []}}
        default_test_group = {'新建分组1': []}

        self.main_window.test_group_manager.set_test_group(default_test_group)
        self.main_window.data_group_manager.set_data_group(default_data_group)

    def yaml_auto_save(self):
        """
            Auto save YAML project
        """
        if self.file_path is None:
            return
        
        prj_name = self.ui.line_prj_name.text()

        if prj_name is None or prj_name.strip() == "":
            return
        
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        
        config['project_name'] = prj_name
        config['spi_config'] = {
            'vcc': self.ui.combo_box_vcc.currentText(),
            'io': self.ui.combo_box_io.currentText(),
            'speed': self.ui.combo_box_speed.currentText(),
            'clk': self.ui.combo_box_clk.currentText(),
            'bit': self.ui.combo_box_bit.currentText(),
            'rx_size': self.ui.combo_box_size.currentText(),
        }

        # print(config['spi_config'])

        if hasattr(self.main_window, 'data_group_manager'):
            self.main_window.data_group_manager.save_current_group_data()

            data_group = {}
            for group_name, group_content in self.main_window.data_group_manager.group_manager.items():
                # 将元组转换为列表以便正确保存到 YAML
                converted_data = []
                for item in group_content['data']:
                    if isinstance(item, tuple):
                        # 将元组转换为列表
                        converted_data.append({
                            'name': item[0],
                            'data': item[1]
                        })

                data_group[group_name] = {
                    'data': converted_data
                }

            config['data_group'] = data_group

            # print(config['data_group'])

        if hasattr(self.main_window, 'test_group_manager'):
            self.main_window.test_group_manager.save_current_mode_group()

            test_group = {}
            # 获取 test_group_manager 中的 group_data
            raw_group_data = self.main_window.test_group_manager.get_test_group()
            
            for group_name, items in raw_group_data.items():
                test_group[group_name] = []
                for item in items:
                    if isinstance(item, tuple) and len(item) >= 2:
                        # 将元组转换为包含 name 和 data 字段的字典
                        test_group[group_name].append({
                            'name': item[0],
                            'data': item[1]
                        })

            config['test_group'] = test_group

            # print(config['test_group'])

        class OrderedDumper(yaml.Dumper):
            def represent_dict(self, data):
                return self.represent_mapping('tag:yaml.org,2002:map', data.items())
            
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                config, 
                f, 
                Dumper=OrderedDumper,
                allow_unicode=True, 
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                width=80
            )
        # print(f"[INFO] 项目已自动保存: {self.file_path}")

        # print(f"[INFO] 项目名称: {prj_name}"))


    def import_prj(self):
        """
            Import YAML project
        """

        reply = QMessageBox.information(
            self.main_window,
            "提示",
            "导入文件将清空当前数据，是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return
        
        self.clear_all()

        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "导入项目",
            "",
            "YAML Files (*.yml *.yaml)"
        )

        if file_path is None:
            return
        
        self.file_path = file_path

        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        if 'project_name' in config:
            self.ui.line_prj_name.setText(config['project_name'])

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

        if 'data_group' in config and hasattr(self.main_window, 'data_group_manager'):
        # 转换数据格式以适应 set_data_group 方法
            data_group = {}
            for group_name, group_content in config['data_group'].items():
                # 将字典格式转换为元组列表
                converted_data = []
                if 'data' in group_content:
                    for item in group_content['data']:
                        if isinstance(item, dict) and 'name' in item and 'data' in item:
                            # 将字典转换为元组
                            converted_data.append((item['name'], item['data']))
                
                data_group[group_name] = {'data': converted_data}
            
            # 使用 set_data_group 方法设置数据
            self.main_window.data_group_manager.set_data_group(data_group)

        # 设置测试组
        if 'test_group' in config and hasattr(self.main_window, 'test_group_manager'):
            # 转换数据格式以适应 set_test_group 方法
            test_group = {}
            for group_name, items in config['test_group'].items():
                # 将字典格式转换为元组列表
                converted_items = []
                for item in items:
                    if isinstance(item, dict) and 'name' in item and 'data' in item:
                        # 将字典转换为元组
                        converted_items.append((item['name'], item['data']))
                
                test_group[group_name] = converted_items
            
            # 使用 set_test_group 方法设置数据
            self.main_window.test_group_manager.set_test_group(test_group)
    
    def clear_all(self):
        self.ui.line_prj_name.clear()
        self.ui.combo_box_data_group.clear()
        self.ui.combo_box_mode_group.clear()
        self.ui.list_group.clear()
        self.ui.list_data.clear()

# if __name__ == "__main__":
#         default_data = YAMLNew.create_yaml()

#         file_path = 'F:/PySide6/SPI上位机v1.27/spi/spi/yaml/新建项目.yml'

#         with open(file_path, 'w', encoding='utf-8') as f:
#             yaml.dump(default_data, f, allow_unicode=True, default_flow_style=False)
        
#         print(f"[INFO] 新项目已保存至: {file_path}")