import machine
from nv24c32lv import nv24c32lv

i2c=machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=400_000) #xiao rp2040
eeprom = nv24c32lv(i2c=i2c)

eeprom.get_messages()
eeprom.append_message('this is a long message')
eeprom.get_messages()
eeprom.append_message('another really good message to append is this')
eeprom.get_messages()
eeprom.clear_all_messages()
eeprom.get_messages()