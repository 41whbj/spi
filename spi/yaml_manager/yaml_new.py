#!/usr/bin/env python3.13
"""
filename: yaml_new.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-03
description: Create new YAML file example
"""

from typing import Dict, Any

class YAMLNew:
    """
        YAMLNew class, responsible for creating new YAML files
    """

    def __init__(self):
        pass

    def create_yaml() -> Dict[str, Any]:
        """
            Create new YAML file

            Returns:
                Dict[str, Any]
        """
        example = {
            "project_name": "项目名称",
            "spi_config": {
                "vcc": "",
                "io": "",
                "speed": "",
                "clk": "",
                "bit": "",
                "rx_size": ""
            },
            "data_group": {},
            "test_group": {}
        }

        return example

