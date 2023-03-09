from ctypes import windll, c_ulong, byref, create_string_buffer, sizeof
from struct import unpack
from .data import *

import win32api

from ctypes import WinDLL

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

buf_dword = create_string_buffer(4)
buf_dword64 = create_string_buffer(8)
bytes_read = c_ulong(0)


def read_buffer(process_handle, address, buffer):
    if windll.kernel32.ReadProcessMemory(process_handle,
                                         address, buffer, sizeof(buffer), byref(bytes_read)):
        return buffer
    else:
        raise MemoryError()


class MemoryReader(object):

    def __init__(self, pid):
        self.pid = pid
        self.process_handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def __exit__(self):
        CloseHandle(self.pid)

    def read_int(self, address):
        buffer = read_buffer(self.process_handle, address, buf_dword)
        return unpack('i', buffer)[0]

    def read_uint(self, address):
        buffer = read_buffer(self.process_handle, address, buf_dword)
        return unpack('l', buffer)[0]

    def read_float(self, address):
        buffer = read_buffer(self.process_handle, address, buf_dword)
        return unpack('f', buffer)[0]

    # python porting from https://github.com/binvec/TH10_DataReversing/blob/master/TH10_DataReversing/data.cpp


    # this project will only use here
    def player_info(self):
        pidAddr = 0x950000
        h = self.read_int(pidAddr + 0xD77824)
        p = self.read_int(pidAddr + 0xD77850)
        if h<0 or h > 100000:
            h = 0
        if p < 0 or p > 1000:
            p = 0
        # read here

        return Player(health=h,power=p)


