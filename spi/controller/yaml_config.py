#!/usr/bin/env python3.13
"""
filename: main.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-10-21
description: yaml config file
"""

import os
import yaml
from PySide6.QtWidgets import QFileDialog, QMessageBox, QComboBox
from PySide6.QtCore import QTimer, Signal, QObject, Qt, QUrl

class YamlConfig(QObject):
    log_signal = Signal(str, int)
    
    def __init__(self, parent=None, ui=None, data_map=None, group_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = ui
        self.data_map = data_map
        self.group_manager = group_manager
        self.current_config_path = None
        self.temp_stop_auto_save = False
        # Prevent recursion save
        self.is_saving = False

        self.auto_save_timer = QTimer(self)

        # setting single-shot timer
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.timeout.connect(self.auto_save_config)
        self.auto_save_delay = 300

        self.project_path = None

        self.data_group_configs = {}
        self.data_group_files = {}

    # link parent widget signals
    def setup_auto_save_connections(self):
        self.ui.combo_box_data_group.currentTextChanged.connect(self.data_group_changed)
        # self.ui.combo_box_data_group.currentIndexChanged.connect(self.schedule_auto_save)
        
        self.ui.list_data.model().rowsInserted.connect(self.save_mode_group_config)
        self.ui.list_data.model().rowsRemoved.connect(self.save_mode_group_config)
        self.ui.list_data.model().rowsMoved.connect(self.on_rows_moved)

        self.ui.list_group.model().rowsRemoved.connect(self.save_mode_group_config)

    # import project folder
    def import_folder(self):
        try:
            folder_path = QFileDialog.getExistingDirectory(
                self.parent,
                "选择项目文件夹",
                "", 
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )

            if not folder_path:
                return
            
            self.temp_stop_auto_save = True
            self.project_path = folder_path
            top_path = os.path.join(folder_path, 'top.yml')

            if not os.path.exists(top_path):
                self.log(f"项目文件夹中不存在 top.yml 文件: {top_path}", 2)
                return
            
            # get the setting from top.yml
            with open(top_path, 'r', encoding='utf-8') as file:
                top_config = yaml.safe_load(file)

            if 'project_name' in top_config:
                project_name = top_config['project_name']
                project_name = str(project_name)

                self.ui.line_prj.setText(project_name)

            if 'markdown_path' not in top_config:
                return
            
            markdown_path = top_config['markdown_path']
            if not markdown_path:
                return

            full_markdown_path = os.path.join(folder_path, markdown_path)
            if os.path.exists(full_markdown_path):
                markdown_dir = os.path.dirname(full_markdown_path)
                self.ui.text_prj.setSearchPaths([markdown_dir])
                self.ui.text_prj.setSource(QUrl.fromLocalFile(full_markdown_path))
            else:
                self.log(f"Markdown 文件不存在: {full_markdown_path}", 2)

            data_group_paths = []

            if 'data_group_path' in top_config:
                data_group_paths = top_config['data_group_path']
                if not isinstance(data_group_paths, list):
                    data_group_paths = [data_group_paths]

            group_folder  = os.path.join(folder_path, 'data_group')
            if os.path.exists(group_folder):
                additional_group_paths = []
                for file_name in os.listdir(group_folder):
                    if file_name.endswith('.yml') or file_name.endswith('.yaml'):
                        additional_group_paths.append(file_name)
                data_group_paths.extend(additional_group_paths)

            self.ui.list_group.clear()

            mode_group_path = os.path.join(folder_path, 'mode_group', 'mode_group.yml')
            if os.path.exists(mode_group_path) and self.group_manager:
                with open(mode_group_path, 'r', encoding='utf-8') as file:
                    mode_group_config = yaml.safe_load(file)
                    if 'mode_group' in mode_group_config:
                        self.group_manager.set_data_group(mode_group_config['mode_group'])

            # clear to advoid conflict
            self.ui.combo_box_data_group.clear()

            all_data_group = []

            for group_path in data_group_paths:

                full_group_path = os.path.join(folder_path, 'data_group', group_path)

                if os.path.exists(full_group_path):
                    with open(full_group_path, 'r', encoding='utf-8') as file:
                        group_config = yaml.safe_load(file)

                        if 'data_group_name' in group_config:
                            data_group_name = group_config['data_group_name']
                            self.data_group_files[data_group_name] = full_group_path
                            all_data_group.append(data_group_name)
                            self.data_group_configs[data_group_name] = group_config
                            if hasattr(self.ui, 'combo_box_data_group') and isinstance(self.ui.combo_box_data_group, QComboBox):
                                if data_group_name not in [self.ui.combo_box_data_group.itemText(i) for i in range(self.ui.combo_box_data_group.count())]:
                                    self.ui.combo_box_data_group.addItem(data_group_name)

            if all_data_group:
                first_group_name = all_data_group[0]
                if first_group_name in self.data_group_configs:
                    self.load_data_group_config(self.data_group_configs[first_group_name])

            def enable_auto_save():
                if self.group_manager and self.project_path:
                    self.save_mode_group_config()
                self.temp_stop_auto_save = False

            QTimer.singleShot(2000, enable_auto_save)

        except Exception as e:
            self.log(f"导入项目文件夹失败: {str(e)}", 2)
            return

    # Import project config from yaml file
    def import_config(self):
        try:
            file_paths, _ = QFileDialog.getOpenFileNames(
                self.parent, "导入配置文件", "", 
                "YAML文件 (*.yml *.yaml);;所有文件 (*)"
            )

            if not file_paths:
                return

            self.temp_stop_auto_save = True

            for file_path in file_paths:
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)

                if 'data_group_name' in config:
                    data_group_name = config['data_group_name']
                    self.data_group_files[data_group_name] = file_path

                self.data_group_configs[data_group_name] = config

                if data_group_name not in [self.ui.combo_box_data_group.itemText(i) for i in range(self.ui.combo_box_data_group.count())]:
                    self.ui.combo_box_data_group.addItem(data_group_name)

            self.current_config_path = file_path
            self.load_data_group_config(config)

            def enable_auto_save():
                self.temp_stop_auto_save = False

            QTimer.singleShot(2000, enable_auto_save)

            self.parent.signals_connected = True

            self.log(f"成功导入{len(file_paths)}个配置文件", 1)

        except Exception as e:
            self.log(f"配置文件导入失败, 请检查配置文件是否符合要求: {e}", 2)
            QMessageBox.critical(
                self.parent, '错误', '配置文件导入失败'
            )

    # Export project config to yaml file
    def export_config(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, "导出配置文件", "spi_config.yml", 
            "YAML文件 (*.yml *.yaml);;所有文件 (*)"
        )

        if not file_path:
            return
    
        config = {
            'data_group_name': self.ui.combo_box_data_group.currentText(),
            'spi_config': {
                'vcc': self.ui.combo_box_vcc.currentText(),
                'io': self.ui.combo_box_io.currentText(),
                'speed': self.ui.combo_box_speed.currentText(),
                'clk': self.ui.combo_box_clk.currentText(),
                'bit': self.ui.combo_box_bit.currentText(),
                's_or_q': self.ui.combo_box_s_or_q.currentText(),
                'rx_size': self.ui.combo_box_size.currentText()
            },
            'data_group': [],
            # 'mode_group': {}
        }

        for name, data in self.data_map.items():
            config['data_group'].append({
                'name': name,
                'data': data
            })

        class QuotedStrDumper(yaml.Dumper):
            def represent_str(self, data):
                return self.represent_scalar('tag:yaml.org,2002:str', data, style='"')
            
            def increase_indent(self, flow=False, indentless=False):
                return super().increase_indent(flow=False, indentless=False)

        QuotedStrDumper.add_representer(str, QuotedStrDumper.represent_str)

        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, 
                Dumper=QuotedStrDumper,      
                allow_unicode=True, 
                default_flow_style=False, 
                sort_keys=False, 
                indent=2, 
                width=80
            )

        self.log(f"配置文件导出成功: {os.path.basename(file_path)}", 1)

    # load config from yaml
    def load_data_group_config(self, config):
        try:

            if 'data_group_name' in config:
                data_group_name = config['data_group_name']
                if hasattr(self.ui, 'combo_box_data_group') and isinstance(self.ui.combo_box_data_group, QComboBox):
                    index = self.ui.combo_box_data_group.findText(data_group_name)
                    if index >= 0:
                        self.ui.combo_box_data_group.setCurrentIndex(index)

            if 'spi_config' in config:
                spi_config = config['spi_config']
                
                if hasattr(self.parent, 'signals_connected') and self.parent.signals_connected:
                    if hasattr(self.ui, 'combo_box_vcc'):
                        self.ui.combo_box_vcc.currentIndexChanged.disconnect(self.parent.vcc_changed)
                    if hasattr(self.ui, 'combo_box_io'):
                        self.ui.combo_box_io.currentIndexChanged.disconnect(self.parent.io_changed)
                    if hasattr(self.ui, 'combo_box_speed'):
                        self.ui.combo_box_speed.currentIndexChanged.disconnect(self.parent.speed_changed)
                    if hasattr(self.ui, 'combo_box_clk'):
                        self.ui.combo_box_clk.currentIndexChanged.disconnect(self.parent.clk_changed)
                    if hasattr(self.ui, 'combo_box_bit'):
                        self.ui.combo_box_bit.currentIndexChanged.disconnect(self.parent.bit_changed)
                    if hasattr(self.ui, 'combo_box_s_or_q'):
                        self.ui.combo_box_s_or_q.currentIndexChanged.disconnect(self.parent.s_or_q_changed)
                    if hasattr(self.ui, 'combo_box_size'):
                        self.ui.combo_box_size.currentIndexChanged.disconnect(self.parent.size_changed)
                    
                    self.parent.signals_connected = False
                
                if 'vcc' in spi_config and hasattr(self.ui, 'combo_box_vcc'):
                    vcc_value = str(spi_config['vcc'])
                    vcc_index = self.ui.combo_box_vcc.findText(vcc_value)
                    if vcc_index >= 0:
                        self.ui.combo_box_vcc.setCurrentIndex(vcc_index)
                
                if 'io' in spi_config and hasattr(self.ui, 'combo_box_io'):
                    io_value = str(spi_config['io'])
                    io_index = self.ui.combo_box_io.findText(io_value)
                    if io_index >= 0:
                        self.ui.combo_box_io.setCurrentIndex(io_index)
                
                if 'speed' in spi_config and hasattr(self.ui, 'combo_box_speed'):
                    speed_value = str(spi_config['speed'])
                    speed_index = self.ui.combo_box_speed.findText(speed_value)
                    if speed_index >= 0:
                        self.ui.combo_box_speed.setCurrentIndex(speed_index)
                
                if 'clk' in spi_config and hasattr(self.ui, 'combo_box_clk'):
                    clk_value = str(spi_config['clk'])
                    clk_index = self.ui.combo_box_clk.findText(clk_value)
                    if clk_index >= 0:
                        self.ui.combo_box_clk.setCurrentIndex(clk_index)
                
                if 'bit' in spi_config and hasattr(self.ui, 'combo_box_bit'):
                    bit_value = str(spi_config['bit'])
                    bit_index = self.ui.combo_box_bit.findText(bit_value)
                    if bit_index >= 0:
                        self.ui.combo_box_bit.setCurrentIndex(bit_index)
                
                if 's_or_q' in spi_config and hasattr(self.ui, 'combo_box_s_or_q'):
                    s_or_q_value = str(spi_config['s_or_q'])
                    s_or_q_index = self.ui.combo_box_s_or_q.findText(s_or_q_value)
                    if s_or_q_index >= 0:
                        self.ui.combo_box_s_or_q.setCurrentIndex(s_or_q_index)
                
                if 'rx_size' in spi_config and hasattr(self.ui, 'combo_box_size'):
                    rx_size_value = str(spi_config['rx_size'])
                    rx_size_index = self.ui.combo_box_size.findText(rx_size_value)
                    if rx_size_index >= 0:
                        self.ui.combo_box_size.setCurrentIndex(rx_size_index)
                
                if hasattr(self.parent, 'signals_connected') and not self.parent.signals_connected:
                    if hasattr(self.ui, 'combo_box_vcc'):
                        self.ui.combo_box_vcc.currentIndexChanged.connect(self.parent.vcc_changed)
                    if hasattr(self.ui, 'combo_box_io'):
                        self.ui.combo_box_io.currentIndexChanged.connect(self.parent.io_changed)
                    if hasattr(self.ui, 'combo_box_speed'):
                        self.ui.combo_box_speed.currentIndexChanged.connect(self.parent.speed_changed)
                    if hasattr(self.ui, 'combo_box_clk'):
                        self.ui.combo_box_clk.currentIndexChanged.connect(self.parent.clk_changed)
                    if hasattr(self.ui, 'combo_box_bit'):
                        self.ui.combo_box_bit.currentIndexChanged.connect(self.parent.bit_changed)
                    if hasattr(self.ui, 'combo_box_s_or_q'):
                        self.ui.combo_box_s_or_q.currentIndexChanged.connect(self.parent.s_or_q_changed)
                    if hasattr(self.ui, 'combo_box_size'):
                        self.ui.combo_box_size.currentIndexChanged.connect(self.parent.size_changed)
                    
                    self.parent.signals_connected = True

                if hasattr(self.parent, 'spi_device') and self.parent.spi_device and self.parent.spi_device.dev_handle:
                    if hasattr(self.parent, 'vcc_changed'):
                        self.parent.vcc_changed(self.ui.combo_box_vcc.currentIndex(), log_set=False)
                    if hasattr(self.parent, 'io_changed'):
                        self.parent.io_changed(self.ui.combo_box_io.currentIndex(), log_set=False)
                    if hasattr(self.parent, 'speed_changed'):
                        self.parent.speed_changed(self.ui.combo_box_speed.currentIndex(), log_set=False)
                    if hasattr(self.parent, 'clk_changed'):
                        self.parent.clk_changed(self.ui.combo_box_clk.currentIndex(), log_set=False)
                    if hasattr(self.parent, 'bit_changed'):
                        self.parent.bit_changed(self.ui.combo_box_bit.currentIndex(), log_set=False)
                    if hasattr(self.parent, 's_or_q_changed'):
                        self.parent.s_or_q_changed(self.ui.combo_box_s_or_q.currentIndex(), log_set=False)
                    if hasattr(self.parent, 'size_changed'):
                        self.parent.size_changed(self.ui.combo_box_size.currentIndex(), log_set=False)

            if 'data_group' in config and hasattr(self.ui, 'list_data') and hasattr(self.parent, 'mainwindow_data'):
                self.ui.list_data.clear()
                self.data_map.clear()
                
                for item in config['data_group']:
                    if 'name' in item and 'data' in item:
                        self.parent.mainwindow_data(
                            item['name'], item['data']
                        )

        except Exception as e:
            self.log(f"加载数据分组配置失败: {str(e)}", 2)

    # Update the data map when the items are moved
    def on_rows_moved(self):
        items = []
        for i in range(self.ui.list_data.count()):
            item = self.ui.list_data.item(i)
            data_tuple = item.data(Qt.UserRole)
            if data_tuple and len(data_tuple) >= 2:
                name, data = data_tuple
                items.append((name, data))

        self.data_map.clear()
        for name, data in items:
            self.data_map[name] = data

        self.schedule_auto_save()

    # combobox changed to load data group
    def data_group_changed(self, text):
        try:
            self.temp_stop_auto_save = True
            if hasattr(self, 'data_group_files'):
                for data_group_name, file_path in self.data_group_files.items():
                    if data_group_name == text and os.path.exists(file_path):
                        self.current_config_path = file_path

                        with open(file_path, 'r', encoding='utf-8') as file:
                            config = yaml.safe_load(file)
                            self.load_data_group_config(config)
                        break

        finally:
            def enable_auto_save():
                self.temp_stop_auto_save = False
            QTimer.singleShot(2000, enable_auto_save)

    def rename_sync(self, old_name, new_name):
        if old_name in self.data_group_files and old_name in self.data_group_configs:
            file_path = self.data_group_files[old_name]
            config = self.data_group_configs[old_name]

            del self.data_group_files[old_name]
            del self.data_group_configs[old_name]
            
            self.data_group_files[new_name] = file_path
            self.data_group_configs[new_name] = config

            if config and 'data_group_name' in config:
                config['data_group_name'] = new_name

            self.temp_stop_auto_save = False
            self.current_config_path = file_path
            self.schedule_auto_save()

    def auto_save_config(self):
        if self.temp_stop_auto_save or not self.current_config_path or not os.path.exists(self.current_config_path):
            return

        try:
            self.is_saving = True
            config = {
                'data_group_name': self.ui.combo_box_data_group.currentText(),
                'spi_config': {
                    'vcc': self.ui.combo_box_vcc.currentText(),
                    'io': self.ui.combo_box_io.currentText(),
                    'speed': self.ui.combo_box_speed.currentText(),
                    'clk': self.ui.combo_box_clk.currentText(),
                    'bit': self.ui.combo_box_bit.currentText(),
                    's_or_q': self.ui.combo_box_s_or_q.currentText(),
                    'rx_size': self.ui.combo_box_size.currentText()
                },
                'data_group': [],
            }

            for name, data in self.data_map.items():
                config['data_group'].append({
                    'name': name,
                    'data': data
                })

            class QuotedStrDumper(yaml.Dumper):
                def represent_str(self, data):
                    return self.represent_scalar('tag:yaml.org,2002:str', data, style='"')
                
                def increase_indent(self, flow=False, indentless=False):
                    return super().increase_indent(flow=False, indentless=False)

            QuotedStrDumper.add_representer(str, QuotedStrDumper.represent_str)

            with open(self.current_config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, 
                    Dumper=QuotedStrDumper,      
                    allow_unicode=True, 
                    default_flow_style=False, 
                    sort_keys=False, 
                    indent=2, 
                    width=80
                )

        finally:
            self.is_saving = False

    def save_mode_group_config(self):
        if not self.project_path or not self.group_manager:
            return
        
        if self.is_saving:
            return

        try:
            self.is_saving = True

            mode_group_dir = os.path.join(self.project_path, 'mode_group')
            if not os.path.exists(mode_group_dir):
                os.makedirs(mode_group_dir)

            mode_group_path = os.path.join(mode_group_dir, 'mode_group.yml')
            
            if self.group_manager.current_group is not None:
                self.group_manager.save_current_mode_group()

            raw_group_data = self.group_manager.get_data_group()

            config = {'mode_group': {}}
            for group_name, items in raw_group_data.items():
                config['mode_group'][group_name] = []
                for item in items:
                    if isinstance(item, tuple) and len(item) >= 2:
                        name, data = item
                        config['mode_group'][group_name].append({
                            'name': name,
                            'data': data
                        })
                    else:
                        config['mode_group'][group_name].append(item)

            class QuotedStrDumper(yaml.Dumper):
                def represent_str(self, data):
                    return self.represent_scalar('tag:yaml.org,2002:str', data, style='"')
                
                def increase_indent(self, flow=False, indentless=False):
                    return super().increase_indent(flow=False, indentless=False)

            QuotedStrDumper.add_representer(str, QuotedStrDumper.represent_str)

            with open(mode_group_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file,
                    Dumper=QuotedStrDumper,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                    width=80
                )

        except Exception as e:
            self.log(f"保存模式组配置失败: {str(e)}", 2)
        finally:
            self.is_saving = False

    # auto save debouncing
    def schedule_auto_save(self):
        self.auto_save_timer.start(self.auto_save_delay)
            
    def log(self, message, level=0):
        self.log_signal.emit(message, level)