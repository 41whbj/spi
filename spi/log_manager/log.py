from datetime import datetime
import csv
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

class LogManager():

    def __init__(self, CMD):
        # self.msg_id = None
        # self.cmd = None
        # self.payload = None
        self.record = []
        self.CMD = CMD

    
    def frame_record(self, msg_id, cmd, payload = None):

        self.record.append({
            "msg_id": format(msg_id, "04X"),
            "cmd": format(cmd, "04X"),
            "payload": payload
        })
        
        # print(f"Record: {self.record}")

    def compare_record(self, msg_id):
        for item in self.record:
            if item["msg_id"] == format(msg_id, "04X"):
                self.cmd_record = item["cmd"]

        for cmd in self.CMD.values():
            if self.cmd_record == format(cmd, "04X"):
                print(f"命令字: {cmd}")
                break

    def cmd_show(self, cmd):
        for key, value in self.CMD.items():
            if value == cmd:
                print(f"命令字: {key}")
                break
        

class CsvManager():

    message_list = []
    def __init__(self):
        pass
        
    # def register_chinese_font(self):
    #     """
    #        Register Chinese font
    #     """

    #     # Use SimHei font
    #     pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.TTF'))
    #     self.font_name = 'SimHei'

    def add_message(self, message, timestamp = False):
        message_process = self.message_process(message, timestamp)
        self.message_list.append(message_process)

    def message_process(self, message, timestamp = False):
        if timestamp is True:
            # Get the timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
        else:
            timestamp = ""

        # Process the message
        processed_message = f"{timestamp}  {message}"
        return processed_message

    def export_csv(self, filename="log_export.csv"):
        """
           Export to CSV file
        """

        # Write to CSV file
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            
            # Write header
            writer.writerow(['时间戳', '日志内容'])
            
            for message in self.message_list:
                # Parse the message to separate timestamp and content
                # 新的日志格式使用双空格作为时间戳和内容的分隔符
                if '  ' in message and ':' in message[:8]:  # 简单判断是否包含时间戳
                    # 分离时间戳和内容
                    parts = message.split('  ', 1)
                    timestamp = parts[0].strip()
                    content = parts[1] if len(parts) > 1 else ''
                    writer.writerow([timestamp, content])
                else:
                    # 没有时间戳的消息
                    writer.writerow(['', message])

    def export_pdf(self, filename="log_export.pdf"):
        # 创建PDF文档
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        # 设置中文字体
        normal_style.fontName = 'SimSun'

        # 注册中文字体
        pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))

        title_style = styles['Title']
        title_style.fontName = 'SimSun'
        
        # 添加标题
        title = Paragraph("日志导出文件", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # 添加日志条目
        for message in self.message_list:
            # 处理消息格式，确保与CSV导出一致
            if '] ' in message:
                # 有时间戳的消息
                timestamp, content = message.split('] ', 1)
                timestamp = timestamp.strip('[')
                # 在PDF中显示为"[时间戳] 内容"格式
                display_message = f"[{timestamp}] {content}"
            else:
                display_message = message
            # 处理特殊字符
            escaped_message = display_message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            p = Paragraph(escaped_message, normal_style)
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
        
        # 构建PDF
        doc.build(story)

    


    