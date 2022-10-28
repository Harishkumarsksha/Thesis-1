########################################################################################################################
# Import required packages

from PyMCP2221A import PyMCP2221A

########################################################################################################################
# Class code
from typing import List


class UsbBridge:
    """Class for USB bridge """

    # Class attributes

    # Class constructor
    def __init__(self, **data):
        self.I2C_speeds = ['100kHz', '400kHz', '1MHz']
        self.I2C_speed_values = [100000, 400000, 1000000]
        self.default_speed_idx = 1
        self.usb_bridge = None

    def get_speeds(self):
        return self.I2C_speeds

    def connect(self, do_connect: bool, speed_idx: int, devnum = 0):
        if do_connect:
            self.usb_bridge = PyMCP2221A.PyMCP2221A(devnum = devnum)
            self.reset()
            self.usb_bridge = PyMCP2221A.PyMCP2221A(devnum = devnum)
            self.init(speed_idx)
            state = self.I2C_State()[0]
        else:
            self.usb_bridge = PyMCP2221A.PyMCP2221A()
            state = self.I2C_State()[0]
            self.reset()
        return state

    def reset(self):
        self.usb_bridge.Reset()

    def init(self, speed_idx: int):
        self.usb_bridge.I2C_Init(self.I2C_speed_values[speed_idx])

    def detect(self):
        slave_addresses = []
        for i in range(0x00, 0x7F):
            if self.usb_bridge.I2C_Read(i, 1) != -1:
                slave_addresses.append('{:02X}'.format(i))
        # if len(slave_addresses) == 0:
        #	raise ValueError('No I2C slave detected!')
        return slave_addresses

    def write(self, sad: int, dat: List[int]):
        self.usb_bridge.I2C_Write(sad, dat)
        return self.I2C_State()[0]

    def read(self, sad: int, num_bytes: int) -> List[int]:
        out = self.usb_bridge.I2C_Read(sad, num_bytes)
        return out

    def I2C_w(self, sad: int, add: int, dat):
        data = [add]
        if type(dat) == list:
            data.extend(dat)
        else:
            data.append(dat)
        return self.write(sad, data)

    def I2C_r(self, sad: int, add: int, num_bytes: int) -> List[int]:
        try:
            self.usb_bridge.I2C_Write(sad, [add])
            out = self.usb_bridge.I2C_Read(sad, num_bytes)
            return out
        except:
            return -1

    def I2C_w_page(self, page, sad, reg, data, reg_page):
        page_old = self.I2C_r(sad, reg_page, 1)[0]
        if page != page_old:
            self.I2C_w(sad, reg_page, page)
        self.I2C_w(sad, reg, data)
        if page != page_old:
            self.I2C_w(sad, reg_page, page_old)

    def I2C_r_page(self, page, sad, reg, reg_page):
        page_old = self.I2C_r(sad, reg_page, 1)[0]
        if page != page_old:
            self.I2C_w(sad, reg_page, page)
        dat = self.I2C_r(sad, reg, 1)[0]
        if page != page_old:
            self.I2C_w(sad, reg_page, page_old)
        return dat

    def create_mask(self, lsb, length):
        mask_neg = 0
        for i in range(length):
            mask_neg = (1 << lsb + i) | mask_neg
        self.mask = (~mask_neg) & 0xFF

    def I2C_w_bits(self, page, sad, reg, data, lsb, length, reg_page):
        page_old = self.I2C_r(sad, reg_page, 1)[0]
        if page != page_old:
            self.I2C_w(sad, reg_page, page)

        self.create_mask(lsb, length)
        reg_value = self.I2C_r(sad, reg, 1)[0]
        value = reg_value & self.mask
        data_w = data << lsb
        new_value = value | data_w
        self.I2C_w(sad, reg, new_value)
        if page != page_old:
            self.I2C_w(sad, reg_page, page_old)

        return self.I2C_State()

    def I2C_r_bits(self, page, sad, reg, lsb, length, reg_page):
        page_old = self.I2C_r(sad, reg_page, 1)[0]
        if page != page_old:
            self.I2C_w(sad, reg_page, page)
        self.create_mask(lsb, length)
        reg_value = self.I2C_r(sad, reg, 1)[0]
        value = reg_value & (~(self.mask) & 0xFF)
        data_r = value >> lsb
        if page != page_old:
            self.I2C_w(sad, reg_page, page_old)
        return data_r

    def I2C_State(self):
        state = self.usb_bridge.I2C_State_Check()
        if state == 0:
            return [True, state]
        else:
            return [False, state]
