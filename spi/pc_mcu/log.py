
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
        


# if __name__ == "__main__":
#     log_manager = LogManager()
#     print(log_manager.cmd)

    