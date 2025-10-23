#!/usr/bin/env python3
"""
filename: formula_parser.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-23
description: 解析和处理YAML配置中的公式
"""

import re
from typing import Dict, List, Any, Union

class FormulaParser:
    """处理YAML配置中的公式解析和计算"""
    
    def __init__(self):
        # 定义支持的操作符，包括算术运算符和逻辑运算符
        self.operators = [
            '+', '-', '*', '/', '(', ')',  # 算术运算符
            '==', '!=', '<', '>', '<=', '>=',  # 比较运算符
            'and', 'or', 'not',  # 逻辑运算符
            '&', '|', '^', '~'   # 位运算符
        ]
        
        # 定义额外的参数列表
        self.extra_parameters = ["通道", "色深", "水平分辨率", "垂直分辨率"]
    
    # ==================== 公式解析功能 ====================
    
    def parse_formula(self, formula_str: str) -> List[str]:
        """
        解析公式字符串，提取变量和操作符
        
        Args:
            formula_str (str): 公式字符串，例如 '对比度+通道'
            
        Returns:
            List[str]: 解析后的标记列表
        """
        # 移除空格
        formula_str = formula_str.replace(' ', '')
        
        # 构建正则表达式模式，按操作符分割
        # 按操作符长度降序排列，确保优先匹配较长的操作符
        sorted_operators = sorted(self.operators, key=len, reverse=True)
        pattern = '(' + '|'.join(re.escape(op) for op in sorted_operators) + ')'
        
        # 使用正则表达式分割变量和操作符
        tokens = re.split(pattern, formula_str)
        
        # 过滤掉空字符串
        tokens = [token for token in tokens if token]
        
        return tokens
    
    def extract_variables(self, formula_str: str) -> List[str]:
        """
        从公式字符串中提取变量名
        
        Args:
            formula_str (str): 公式字符串
            
        Returns:
            List[str]: 变量名列表
        """
        # 解析公式
        tokens = self.parse_formula(formula_str)
        
        # 提取非操作符的标记作为变量
        variables = [token for token in tokens if token not in self.operators]
        
        return variables
    
    # ==================== 变量处理功能 ====================
    
    def replace_variables_with_values(self, formula_str: str, var_dict: Dict[str, float]) -> str:
        """
        将公式中的变量替换为实际值
        
        Args:
            formula_str (str): 公式字符串
            var_dict (Dict[str, float]): 变量名到值的映射
            
        Returns:
            str: 替换变量后的公式字符串
        """
        # 简单替换实现
        result = formula_str
        
        # 按变量名长度降序排列，避免短变量名替换长变量名的一部分
        sorted_vars = sorted(var_dict.keys(), key=len, reverse=True)
        
        for var_name in sorted_vars:
            # 使用正则表达式进行精确匹配替换
            # 使用 (?<![a-zA-Z0-9_一-龯]) 和 (?![a-zA-Z0-9_一-龯]) 来匹配非字母数字下划线和非中文字符的边界
            escaped_var = re.escape(var_name)
            pattern = r'(?<![a-zA-Z0-9_一-龯])' + escaped_var + r'(?![a-zA-Z0-9_一-龯])'
            result = re.sub(pattern, str(var_dict[var_name]), result)
            
        return result
    
    def evaluate_formula(self, formula_str: str, var_dict: Dict[str, Union[float, bool]]) -> Union[float, bool]:
        """
        计算公式的结果
        
        Args:
            formula_str (str): 公式字符串
            var_dict (Dict[str, Union[float, bool]]): 变量名到值的映射
            
        Returns:
            Union[float, bool]: 计算结果
        """
        # 替换变量
        formula_with_values = self.replace_variables_with_values(formula_str, var_dict)
        
        # 安全地计算表达式
        try:
            # 移除空格
            formula_with_values = formula_with_values.replace(' ', '')
            
            # 验证表达式只包含允许的字符
            # 包含数字、基本运算符、比较运算符、逻辑运算符、位运算符和中文字符
            allowed_chars = set('0123456789+-*/().<>=!andort&|^~ ')
            # 检查是否包含中文字符（Unicode范围：\u4e00-\u9fff）
            is_valid = True
            invalid_chars = []
            for c in formula_with_values:
                if c not in allowed_chars and not ('\u4e00' <= c <= '\u9fff'):
                    is_valid = False
                    invalid_chars.append(c)
            
            if is_valid:
                # Python关键字替换
                formula_with_values = formula_with_values.replace('and', ' and ')
                formula_with_values = formula_with_values.replace('or', ' or ')
                formula_with_values = formula_with_values.replace('not', ' not ')
                
                # 检查是否仍有未替换的中文变量名
                remaining_chinese = re.findall(r'[\u4e00-\u9fff]+', formula_with_values)
                if remaining_chinese:
                    raise ValueError(f"Formula contains undefined variables: {remaining_chinese}")
                
                result = eval(formula_with_values)
                return result
            else:
                raise ValueError(f"Formula contains invalid characters: {formula_with_values}. Invalid characters: {set(invalid_chars)}")
        except Exception as e:
            raise ValueError(f"Error evaluating formula '{formula_with_values}': {str(e)}")
    
    # ==================== 数值转换功能 ====================
    
    def convert_to_hex(self, value: Union[int, float], sign_enabled: bool = False, bit_width: int = 16) -> str:
        """
        将数值转换为十六进制数，根据符号位设置和位宽进行处理
        
        Args:
            value (Union[int, float]): 要转换的数值
            sign_enabled (bool): 是否启用符号位
            bit_width (int): 位宽，支持8位或16位，默认为8位
            
        Returns:
            str: 十六进制数字符串
        """
        # 转换为整数
        int_value = int(value)
        
        if sign_enabled:
            if bit_width == 8:
                # 8位二进制数范围：-128 到 127
                if int_value < -128 or int_value > 127:
                    raise ValueError(f"Value {int_value} out of range for signed {bit_width}-bit integer ({-2**(bit_width-1)} to {2**(bit_width-1)-1})")
                
                # 转换为8位带符号整数的补码表示
                if int_value < 0:
                    # 负数的补码表示
                    hex_value = format(int_value & 0xFF, '02X')
                else:
                    # 正数直接转换
                    hex_value = format(int_value, '02X')
            elif bit_width == 16:
                # 16位二进制数范围：-32768 到 32767
                if int_value < -32768 or int_value > 32767:
                    raise ValueError(f"Value {int_value} out of range for signed {bit_width}-bit integer ({-2**(bit_width-1)} to {2**(bit_width-1)-1})")
                
                # 转换补码表示,只保留低8位
                if int_value < 0:
                    # 负数的补码表示
                    hex_value = format(int_value & 0x00FF, '04X')
                else:
                    # 正数直接转换
                    hex_value = format(int_value, '04X')
            else:
                raise ValueError(f"Unsupported bit width: {bit_width}, only 8 and 16 are supported")
        else:
            if bit_width == 8:
                # 8位无符号二进制数范围：0 到 255
                if int_value < 0 or int_value > 255:
                    raise ValueError(f"Value {int_value} out of range for unsigned {bit_width}-bit integer (0 to {2**bit_width-1})")
                
                hex_value = format(int_value, '02X')
            elif bit_width == 16:
                # 16位无符号二进制数范围：0 到 65535 (0xFFFF)
                if int_value < 0 or int_value > 65535:
                    raise ValueError(f"Value {int_value} out of range for unsigned {bit_width}-bit integer (0 to {2**bit_width-1})")
                
                hex_value = format(int_value, '04X')
            else:
                raise ValueError(f"Unsupported bit width: {bit_width}, only 8 and 16 are supported")
        
        return hex_value
    
    # ==================== 验证功能 ====================
    
    def validate_var_name(self, var_name: str, multi_var: str) -> tuple[bool, str]:
        """
        验证var_name字段是否合理
        
        Args:
            var_name (str): 变量名字符串
            multi_var (str): 多变量开关 ('是' 或 '否')
            
        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        # 分割变量名（支持中英文逗号）
        variables = re.split(r'[,\，]', var_name.strip())
        # 过滤掉空字符串
        variables = [var.strip() for var in variables if var.strip()]
        
        # 检查是否为空
        if not variables:
            return False, "变量名不能为空"
        
        # 如果multi_var为'否'，只能有一个变量
        if multi_var == '否':
            if len(variables) > 1:
                return False, f"多变量模式关闭，但提供了{len(variables)}个变量: {', '.join(variables)}"
            return True, ""
        
        # 如果multi_var为'是'，可以有多个变量，但需要遵循特定规则
        if multi_var == '是':
            # 分离额外参数和其他变量
            extra_params = [var for var in variables if var in self.extra_parameters]
            other_vars = [var for var in variables if var not in self.extra_parameters]
            
            # 除了额外参数外，只能有一个其他变量
            if len(other_vars) > 1:
                return False, f"除了额外参数({', '.join(self.extra_parameters)})外，只能有一个其他变量，但提供了{len(other_vars)}个: {', '.join(other_vars)}"
            
            # 在多变量模式下，即使没有使用额外参数也应该通过验证
            return True, ""
        
        return False, f"无效的multi_var值: {multi_var}，应为'是'或'否'"

    # ==================== 配置处理功能 ====================
    
    @staticmethod
    def process_yaml_config(config_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        处理YAML配置列表中的公式
        
        Args:
            config_list (List[Dict[str, Any]]): YAML配置列表
            
        Returns:
            List[Dict[str, Any]]: 处理后的配置列表
        """
        parser = FormulaParser()
        processed_configs = []
        
        for config in config_list:
            processed_config = config.copy()
            
            # 验证var_name字段
            if 'var_name' in config and 'multi_var' in config:
                is_valid, error_msg = parser.validate_var_name(config['var_name'], config['multi_var'])
                if not is_valid:
                    print(f"配置验证失败: {error_msg}")
                    # 可以选择跳过此配置或抛出异常
                    # 这里我们添加错误信息到配置中
                    processed_config['validation_error'] = error_msg
            
            # 如果有公式字段，则处理公式
            if 'formula' in config and config['formula']:
                formula_str = config['formula']
                
                # 提取变量
                variables = parser.extract_variables(formula_str)
                processed_config['formula_variables'] = variables
                
            processed_configs.append(processed_config)
        
        return processed_configs

    # ==================== 计算功能 ====================
    
    @staticmethod
    def calculate_and_format_result(formula: str, var_dict: Dict[str, Union[float, bool]], 
                                sign_enabled: bool = False, bit_width: int = 8) -> str:
        """
        计算公式结果并格式化为十六进制数
        
        Args:
            formula (str): 公式字符串
            var_dict (Dict[str, Union[float, bool]]): 变量值字典
            sign_enabled (bool): 是否启用符号位
            bit_width (int): 位宽，支持8位或16位，默认为8位
            
        Returns:
            str: 格式化的十六进制数结果
        """
        parser = FormulaParser()
        
        # 计算公式结果
        result = parser.evaluate_formula(formula, var_dict)
        
        # 转换为十六进制数
        hex_result = parser.convert_to_hex(result, sign_enabled, bit_width)
        
        return hex_result

    @staticmethod
    def calculate_formula_result(formula: str, var_dict: Dict[str, Union[float, bool]]) -> float:
        """
        计算公式结果但不进行十六进制转换
        
        Args:
            formula (str): 公式字符串
            var_dict (Dict[str, Union[float, bool]]): 变量值字典
            
        Returns:
            float: 计算结果
        """
        parser = FormulaParser()
        
        # 计算公式结果
        result = parser.evaluate_formula(formula, var_dict)
        
        return result