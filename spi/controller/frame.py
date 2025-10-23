from .crc import CRC

# PC and MCU data frames definitions
Header = 0x5AA5
Msg_ID = 0x0000

CMD = {
    #PC -> MCU
    "Ping": 0x0001, # PC request general connection from MCU
    "GetCaseList": 0x0002, # PC request case list from MCU
    "RunCase": 0x1001, # PC issues run case command to MCU
    "Stop": 0x1002, # PC issues stop command to MCU
    "SendData": 0x1003, # PC issues data to MCU

    #MCU -> PC
    "Ack":0x8001, # General ack from MCU
    "Nack":0x8002, # General nack from MCU
    "CaseList":0x8003, # Case list from MCU
    "Log":0x9001, # Log from MCU 
    "CaseResult":0x9002 # Case result from MCU
}

current_msg_id = Msg_ID

case_list = []

class Frame():
    # Generate frame with no crc check
    def generate_frame(cmd, data=None):
        global current_msg_id
        msg_id = current_msg_id
        current_msg_id = (current_msg_id + 1) % 0x10000

        # Transform data to bytes
        if data is None:
            data_length = 0
            payload = b''
        else:
            if isinstance(data, bytes):
                payload = data
            else:
                payload = bytes(data)
            data_length = len(payload)

        # Generate frame
        frame = bytearray()

        frame.append((Header >> 8) & 0xFF)
        frame.append(Header & 0xFF)
        
        frame.append((msg_id >> 8) & 0xFF)
        frame.append(msg_id & 0xFF)
        
        frame.append((cmd >> 8) & 0xFF)
        frame.append(cmd & 0xFF)
        
        frame.append((data_length >> 24) & 0xFF)
        frame.append((data_length >> 16) & 0xFF)
        frame.append((data_length >> 8) & 0xFF)
        frame.append(data_length & 0xFF)
        
        frame.extend(payload)

        return frame

    # Parse receive frame with selectable crc check
    def parse_receive_frame(receive_data, use_crc=False):
        basic_length = 10

        if len(receive_data) < basic_length:
            return False,None,None,None,"data length error"
        
        header = (receive_data[0] << 8) | receive_data[1]
        if header != Header:
            return False,None,None,None,"header error"
        
        msg_id = (receive_data[2] << 8) | receive_data[3]

        cmd = (receive_data[4] << 8) | receive_data[5]

        data_length = (receive_data[6] << 24) | (receive_data[7] << 16) | (receive_data[8] << 8) | receive_data[9]
        
        expected_length = basic_length + data_length
        if use_crc:
            expected_length += 2
        
        if len(receive_data) < expected_length:
            return False, None, None, None, "data length error"

        payload = receive_data[basic_length:basic_length + data_length]

        if use_crc:
            original_data = receive_data[:basic_length + data_length]

            # if not isinstance(original_data, bytes):
            #     original_data = bytes(original_data)
            
            # print(original_data)

            crc_calc = CRC.crc_16_user(original_data)

            receive_crc = (receive_data[expected_length - 2] << 8) | receive_data[expected_length - 1]

            print(receive_crc)
            if crc_calc != receive_crc:
                return False, None, None, None, "CRC error"
        
        return True, msg_id, cmd, payload, "Success"

    # Parse case data from payload
    def parse_case(payload):
        try:
            case_str = payload.decode('ascii')

            case_list = case_str.split(',')
            case_list = [case for case in case_list if case]
            return case_list
        except Exception as e:
            return f"parse case error: {e}"
