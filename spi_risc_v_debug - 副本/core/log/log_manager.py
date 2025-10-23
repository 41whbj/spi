
#!/usr/bin/env python3.13
"""
filename: log_manager.py
author: [spx]
email: [3123002434@mail2.gdut.edu.cn]
date: 2025-11-25
description: 日志类，预先处理日志信息
"""

from datetime import datetime
import csv
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table  # 新增Table
from reportlab.lib import colors  # 新增colors



 

# class LogManager():

#     def __init__(self, CMD):
#         self.record = []
#         self.CMD = CMD

    
#     def frame_record(self, msg_id, cmd, payload = None):

#         self.record.append({
#             "msg_id": format(msg_id, "04X"),
#             "cmd": format(cmd, "04X"),
#             "payload": payload
#         })
        
#     def compare_record(self, msg_id):
#         for item in self.record:
#             if item["msg_id"] == format(msg_id, "04X"):
#                 self.cmd_record = item["cmd"]

#         for cmd in self.CMD.values():
#             if self.cmd_record == format(cmd, "04X"):
#                 print(f"命令字: {cmd}")
#                 break

#     def cmd_show(self, cmd):
#         for key, value in self.CMD.items():
#             if value == cmd:
#                 print(f"命令字: {key}")
#                 break
        

class SpecialLog():

    message_list = []
    def __init__(self):
        pass
        
    def add_message(self, message, timestamp = True):
        """
        添加消息到消息列表中
        
        Args:
            message (str): 要添加的原始消息内容
            timestamp (bool): 是否为消息添加时间戳，默认为False
        """

        # 处理消息（可能添加时间戳）
        message_process = self.message_process(message, timestamp)

        # 将处理后的消息添加到消息列表
        self.message_list.append(message_process)

    def add_error_message(self, error_round, hw_count, write_base_address, write_address, write_data, read_base_address, read_address, read_data, packet_type):
        """接收错误详情字段，格式化后存入message_list（自动带时间戳）

        Args:
            error_round: 错误出现轮次（int）
            hw_count: 写入半字数（int）
            write_base_address: 写基地址（str，十六进制）
            write_address: 写数据地址（str，十六进制）
            write_data: 写数据（str，十六进制）
            read_base_address: 读基地址（str，十六进制）
            read_address: 读数据地址（str，十六进制）
            read_data: 读数据（str，十六进制）
            packet_type: 测试类型（str，如"写包测试"）
        """

        
        # 使用新格式（包含新增字段）
        error_message = f"错误出现轮次:{error_round},写入半字数:{hw_count},写基地址:{write_base_address},写数据地址:{write_address},写数据:{write_data},读基地址:{read_base_address},读数据地址:{read_address},读数据:{read_data},测试类型:{packet_type}"


        # 调用已有方法添加时间戳并存入列表
        self.add_message(error_message)

    def message_process(self, message, timestamp = False):
        """处理消息，添加时间戳（可选）
        
        Args:
            message: 原始消息内容（str）
            timestamp: 是否添加时间戳（bool，默认False）
        Returns:
            处理后的消息（str，格式为 "时间戳  消息内容"）
        """

        if timestamp is True:

            # 生成当前时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp = ""

        # 将时间戳和消息内容组合成最终的字符串格式
        processed_message = f"{timestamp}  {message}"
        return processed_message

    def export_pdf(self, filename="log_export.pdf"):
        """将message_list中的消息导出为PDF文件，错误信息生成为表格格式

        Args:
            filename: 导出的PDF文件名（str，默认"log_export.pdf"）
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']

        # 注册并设置中文字体（Windows路径，非Windows需调整为对应字体路径）
        pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
        normal_style.fontName = 'SimSun'
        normal_style.fontSize = 10

        title_style = styles['Title']
        title_style.fontName = 'SimSun'
        title_style.textColor = colors.black
        
        # 添加PDF标题
        story.append(Paragraph("日志导出文件", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        i = 0
        while i < len(self.message_list):
            message = self.message_list[i]
            
            # 分离时间戳和内容（适配 "时间戳  内容" 的双空格分隔格式）
            timestamp_part = ""
            content = message
            if '  ' in message and len(message.split('  ')) >= 2:
                timestamp_part, content = message.split('  ', 1)
                timestamp_part = f"[{timestamp_part}] "  # 统一时间戳显示格式
            
            # 识别错误提示行（如："实例XX运行结果出现错误"），下一行开始是表格数据
            if "运行结果出现错误" in content:

                # 添加错误提示行（单独显示，不放入表格）
                story.append(Paragraph(f"{timestamp_part}{content}", normal_style))
                story.append(Spacer(1, 0.1*inch))
                
                # 当前版本总是使用新格式，因为add_error_message方法已更新
                table_headers = ["错误出现轮次", "写入半字数", "写基地址", "写数据地址", "写数据", "读基地址", "读数据地址", "读数据", "测试类型"]
                    
                table_data = [table_headers]
                
                # 从下一行开始收集错误详情行（表格数据行）
                i += 1
                while i < len(self.message_list):
                    next_msg = self.message_list[i]

                    # 分离下一行的时间戳和内容
                    next_content = next_msg.split('  ', 1)[1] if '  ' in next_msg else next_msg
                    
                    # 识别错误详情行：包含英文逗号（分隔字段）和英文冒号（key:value）
                    if ',' in next_content and ':' in next_content:

                        # 按英文逗号分割字段（如 "错误出现次数:0", "写数据地址: 9" ...）
                        field_parts = [p.strip() for p in next_content.split(',')]
                        row_data = []

                        # 提取每个字段的 value（跳过 key）
                        for field in field_parts:
                            if ':' in field:
                                value = field.split(':', 1)[1].strip()  # 取冒号后的值
                                row_data.append(value)

                        # 确保数据列数和表头一致，避免表格错乱
                        if len(row_data) == len(table_headers):
                            table_data.append(row_data)
                        i += 1
                    else:
                        break
                
                # 生成表格（至少需要1行表头+1行数据）
                if len(table_data) > 1:
                    # 根据表头数量调整表格列宽
                    num_cols = len(table_headers)
                    col_widths = [(A4[0] / num_cols - 10) if num_cols > 0 else 50] * num_cols  # 平均分配宽度并留出边距
                    
                    table = Table(table_data, colWidths=col_widths, repeatRows=1)  # 表头重复显示（跨页时）
                    # 设置表格样式
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 减小字体以适应更多内容
                        ('PADDING', (0, 0), (-1, -1), 3),  # 减小单元格内边距
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 表格边框
                        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # 支持中文换行
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 0.2*inch))
                continue  # 跳过已处理的表格数据行，继续下一条日志
            
            # 非错误表格内容，直接显示文本
            full_content = f"{timestamp_part}{content}" if timestamp_part else content
            
            # 转义PDF特殊字符（&、<、>）
            escaped_content = full_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(escaped_content, normal_style))
            story.append(Spacer(1, 0.1*inch))
            i += 1
        
        # 生成最终PDF文件
        doc.build(story)

    def export_csv(self, filename="log_export.csv"):
        """将message_list中的消息导出为CSV文件，错误信息生成为表格格式

        Args:
            filename: 导出的CSV文件名（str，默认"log_export.csv"）
        """
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            # 写入CSV标题 - 使用统一的标题结构，为错误信息预留所有可能的列
            writer.writerow(["时间戳", "日志内容", "错误出现轮次", "写入半字数", "写基地址", "写数据地址", "写数据", "读基地址", "读数据地址", "读数据", "测试类型"])
            
            i = 0
            while i < len(self.message_list):
                message = self.message_list[i]
                
                # 分离时间戳和内容（适配 "时间戳  内容" 的双空格分隔格式）
                timestamp_part = ""
                content = message
                if '  ' in message and len(message.split('  ')) >= 2:
                    timestamp_part, content = message.split('  ', 1)
                
                # 识别错误提示行（如："测例XX运行结果出现错误"），下一行开始是表格数据
                if "运行结果出现错误" in content:
                    # 写入错误提示行，其他错误相关字段留空
                    writer.writerow([timestamp_part, content, "", "", "", "", "", "", "", "", ""])
                    
                    # 当前版本总是使用新格式，因为add_error_message方法已更新
                    # 从下一行开始收集错误详情行（表格数据行）
                    i += 1
                    while i < len(self.message_list):
                        next_msg = self.message_list[i]

                        # 分离下一行的时间戳和内容
                        next_content = next_msg.split('  ', 1)[1] if '  ' in next_msg else next_msg
                        
                        # 识别错误详情行：包含英文逗号（分隔字段）和英文冒号（key:value）
                        if ',' in next_content and ':' in next_msg:

                            # 按英文逗号分割字段（如 "错误出现次数:0", "写数据地址: 9" ...）
                            field_parts = [p.strip() for p in next_content.split(',')]
                            row_data = []

                            # 提取每个字段的 value（跳过 key）
                            for field in field_parts:
                                if ':' in field:
                                    value = field.split(':', 1)[1].strip()  # 取冒号后的值
                                    row_data.append(value)

                            # 确保数据列数和表头一致，避免表格错乱
                            # 表头有11列：["时间戳", "日志内容", "错误出现轮次", "写入半字数", "写基地址", "写数据地址", "写数据", "读基地址", "读数据地址", "读数据", "测试类型"]
                            # 错误数据本身有9列，需要在前面插入空的"时间戳"和"日志内容"列
                            if len(row_data) == 9:  # 确保我们有9个错误数据字段
                                full_row = ["", ""]  # 前两列（时间戳和日志内容）为空
                                full_row.extend(row_data)  # 添加9个错误字段
                                writer.writerow(full_row)
                            i += 1
                        else:
                            break
                    
                    continue  # 跳过已处理的表格数据行，继续下一条日志
                
                # 非错误表格内容，直接写入CSV，错误相关字段留空
                writer.writerow([timestamp_part, content, "", "", "", "", "", "", "", "", ""])
                i += 1