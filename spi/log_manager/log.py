from datetime import datetime
import csv

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

    def add_message(self, message):
        message_process = self.message_process(message)
        self.message_list.append(message_process)

    def message_process(self, message):
        # Get the timestamp
        timestamp = datetime.now().strftime("%d %H:%M:%S")

        # Process the message
        processed_message = f"[{timestamp}] {message}"
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
            
            # Write log content
            for message in self.message_list:
                # Parse the message to separate timestamp and content
                if '] ' in message:
                    timestamp, content = message.split('] ', 1)
                    timestamp = timestamp.strip('[')
                    writer.writerow([timestamp, content])
                else:
                    writer.writerow(['', message])





    


    