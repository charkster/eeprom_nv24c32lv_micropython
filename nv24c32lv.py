import time

class nv24c32lv:

    # Constructor
    def __init__(self, i2c):
        self.i2c      = i2c
        self.slave_id = 0x50
       
    def write_data(self, address=0x00, data=0x00, num_bytes=0):
        self.i2c.writeto_mem(self.slave_id, address, bytearray(data, "ascii"), addrsize=16) # MicroPython

    def read_data(self, address=0x00, num_bytes=1):
        read_bytes = self.i2c.readfrom_mem(self.slave_id, address, num_bytes, addrsize=16) # MicroPython
        return read_bytes

    def get_end_addr(self):
        for page in range(0,1024):
            read_32 = self.read_data(page*32, 32)
            for i in range(0,32):
                if (read_32[i] > 127):
                    return i + page*32
        print("all full")
        return -1

    def get_messages(self):
        messages = []
        msg_str = ""
        for page in range(0,1024):
            read_32 = self.read_data(page*32, 32)
            for i in range(0,32):
                if (read_32[i] > 127):
                    return messages
                if (read_32[i] != ord('\n')):
                    msg_str += chr(read_32[i])
                else:
                    messages.append(msg_str)
                    msg_str = ""
        return messages

    # writing to eeprom must be done on 32 byte page boundaries, and must wait 100ms after each page is written
    def append_message(self, message=''):
        msg_list = []
        if (message[-1] != '\n'):
            message += '\n'
        end_address = self.get_end_addr()
        page_length = 32 # this is in datasheet
        remain_addr_in_page = page_length - (end_address % page_length)
        msg_list.append(message[0:remain_addr_in_page])
        message = message[remain_addr_in_page:]
        msg_list += [ message[i:i+page_length] for i in range(0, len(message), page_length) ]
        for msg_piece in msg_list:
            if (len(msg_piece) > 0):
                self.write_data(end_address, msg_piece)
                end_address += len(msg_piece)
                time.sleep(0.01)
    
    # takes about 10 seconds
    def clear_all_messages(self):
        for page in range(0,1024):
            self.write_data(page*32, [0xFF] * 32)
            time.sleep(0.01)