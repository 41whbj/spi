#!/usr/bin/env python3.13
"""
filename: yaml_template.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-25
description: YAML模板生成器，负责创建新的YAML配置文件模板
"""

from typing import Dict, Any

class YAMLTemplate:
    """
    YAML模板类，负责创建标准的YAML配置文件模板
    
    该类提供了创建新YAML项目所需的标准模板结构，
    包括项目基本信息、SPI配置参数、数据组和测试组等部分。
    """

    def __init__(self):
        """
        初始化YAML模板生成器
        """
        pass

    @staticmethod
    def create_template() -> Dict[str, Any]:
        """
        创建新的YAML文件模板
        
        返回一个包含标准YAML结构的字典，用于初始化新的YAML项目文件。
        模板包含项目名称、SPI配置参数、数据组和测试组等主要部分。
        
        Returns:
            Dict[str, Any]: 包含标准YAML结构的字典
                - project_name (str): 项目名称
                - spi_config (dict): SPI配置参数
                - data_group (dict): 数据组配置
                - test_group (dict): 测试组配置
        """
        template = {
            "project_name": "项目名称",
            "spi_config": {
                "vcc": "",      # VCC电压设置
                "io": "",       # IO电压设置
                "speed": "",    # SPI通信速度
                "clk": "",      # 时钟模式
                "bit": "",      # 位序模式
                "rx_size": ""   # 接收数据大小
            },
            "data_group": {'默认组': {'data': []}},   # 数据组配置
            "test_group": {'新建分组': []}    # 测试组配置
        }

        return template