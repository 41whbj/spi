#!/usr/bin/env python3.13
"""
filename: log_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-12-31
description: 日志解析类，用于解析测试用例运行结果
"""
from datetime import datetime

import reportlab.pdfgen.canvas as canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import csv

class CaseResultParser():

    def __init__(self):
        self.timestamp = []
        self.err_case = []
        self.log_content = []

    def save_result(self, timestamp, err_case, log_content):
        """保存测试用例运行结果"""

        self.timestamp.append(timestamp)
        self.err_case.append(err_case)
        self.log_content.append(log_content)

    def parse_all_case_results(self):
        """
        解析所有已保存的测试用例运行结果，返回按测例分组的错误记录
        """
        grouped_error_records = {}
        
        for idx, (timestamp, err_case, log_content) in enumerate(zip(self.timestamp, self.err_case, self.log_content)):

            unique_key = timestamp

            case_name = f"测例{err_case}错误"
            
            # 直接解析原始log_content（移除多余的分号拼接，避免分割错误）
            # 过滤空字符串 + 处理末尾分号
            log_parts = [part.strip() for part in log_content.split(';') if part.strip()]
            
            if len(log_parts) < 2:
                continue
            
            # 3. 解析表头和数据
            header_str = log_parts[0]
            error_info = [field.strip() for field in header_str.split(',')]
            field_count = len(error_info)
            data_rows = log_parts[1:]
            
            # 4. 初始化测例记录
            grouped_error_records[unique_key] = {
                'timestamp': timestamp,
                'case_name': case_name,
                'error_info': error_info,
                'error_records': []
            }
            
            # 5. 解析每一行数据
            for row_idx, data_str in enumerate(data_rows):
                data_values = [value.strip() for value in data_str.split(',')]
                
                # 校验字段数量
                if len(data_values) != field_count:
                    print(f"警告: 第{row_idx+1}行数据字段不匹配（期望{field_count}个，实际{len(data_values)}个）- {data_str}")
                    continue
                
                # 构建数据记录
                record = dict(zip(error_info, data_values))
                grouped_error_records[unique_key]['error_records'].append(record)
        
        return grouped_error_records

    def export_csv(self, file_path):
        """
        导出所有错误记录到CSV文件
        """
        grouped_error_records = self.parse_all_case_results()
        
        if not grouped_error_records:
            return
        
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            for _, case_data in grouped_error_records.items():
                # 验证数据是否存在
                if not case_data['error_records']:
                    continue
                
                # 第一行：完整表头（时间 + 错误测例 + 自定义字段）
                header_row = ['时间', '错误测例'] + case_data['error_info']
                writer.writerow(header_row)
                
                # 第二行：时间戳 + 测例名（后续列空）
                time_case_row = [case_data['timestamp'], case_data['case_name']] + [''] * len(case_data['error_info'])
                writer.writerow(time_case_row)
                
                # 数据行：前两列空，填充数据
                for record in case_data['error_records']:
                    data_row = ['', '']  # 前两列空
                    for field in case_data['error_info']:
                        value = record.get(field, '')

                        # 检查值是否为纯数字且长度较长，如果是则转换为文本格式
                        if self.format_as_text(value):
                            # 在值前添加制表符以确保Excel将其视为文本
                            formatted_value = '\t' + str(value)
                        else:
                            formatted_value = value
                        data_row.append(formatted_value)
                    writer.writerow(data_row)
                
                # 测例间分隔（空行）
                writer.writerow([])
                writer.writerow([])

    def export_pdf(self, file_path):
        """
        导出所有错误记录到PDF文件
        """
        grouped_error_records = self.parse_all_case_results()
        
        if not grouped_error_records:
            return
        
        # 创建PDF文档
        doc = canvas.Canvas(file_path, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()
        
        # 添加标题
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
        )
        title = Paragraph("测试用例运行结果报告", title_style)
        elements.append(title)
        
        for key, case_data in grouped_error_records.items():
            if not case_data['error_records']:
                continue
            
            # 添加测例标题
            case_title = Paragraph(f"时间: {case_data['timestamp']} | 错误测例: {case_data['case_name']}", styles['Heading2'])
            elements.append(case_title)
            elements.append(Spacer(1, 12))
            
            # 准备表格数据
            table_data = []
            
            # 表头
            header_row = ['序号'] + case_data['error_info']
            table_data.append(header_row)
            
            # 数据行
            for idx, record in enumerate(case_data['error_records'], 1):
                data_row = [str(idx)]
                for field in case_data['error_info']:
                    value = record.get(field, '')
                    # 处理长文本，防止超出页面边界
                    str_value = str(value)
                    if len(str_value) > 50:  # 如果文本太长，截断并加省略号
                        str_value = str_value[:47] + "..."
                    data_row.append(str_value)
                table_data.append(data_row)
            
            # 创建表格
            table = Table(table_data)
            
            # 设置表格样式
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)
            
            # 计算每列宽度以适应页面
            col_widths = []
            page_width = landscape(A4)[0] - 100  # 页面宽度减去边距
            num_cols = len(header_row)
            col_width = page_width / num_cols
            
            # 限制最大列宽，防止某些列过宽
            max_col_width = 2 * inch  # 最大列宽2英寸
            min_col_width = 0.5 * inch  # 最小列宽0.5英寸
            
            for i in range(num_cols):
                if col_width > max_col_width:
                    col_widths.append(max_col_width)
                elif col_width < min_col_width:
                    col_widths.append(min_col_width)
                else:
                    col_widths.append(col_width)
            
            table._argW = col_widths
            
            elements.append(table)
            elements.append(Spacer(1, 20))
        
        # 构建PDF
        doc.build(elements)

    def format_as_text(self, value):
        """
        判断值是否应该格式化为文本格式
        """
        if not value:
            return False

        str_value = str(value)

        # 检查是否为纯数字
        if str_value.isdigit():
            # 如果数字长度大于10位，或者以0开头（除了单独的0），则格式化为文本
            return len(str_value) > 10 or (len(str_value) > 1 and str_value[0] == '0')

        # 检查是否为十六进制数（如FFFF格式）或包含字母E的格式（如68E9）
        if isinstance(value, str):
            # 如果包含字母E（可能是十六进制或类似68E9的格式），则格式化为文本
            if 'E' in str_value.upper():
                # 检查是否符合十六进制格式或类似68E9的格式（字母E前后都是十六进制字符）
                # 这种格式应该作为文本处理以避免被Excel解释为科学计数法
                return True
            # 检查是否为十六进制数（如FFFF格式）
            if all(c.upper() in '0123456789ABCDEF' for c in str_value):
                return len(str_value) > 4  # 如果十六进制数长度超过4位，也视为文本

        return False