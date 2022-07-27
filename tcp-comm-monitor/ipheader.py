# Reference: 「サイバーセキュリティプログラミング Pythonで学ぶハッカーの思考」オライリー・ジャパン
import socket
import struct
from ctypes import *

class IP(Structure):
    _fields_ = [
        ("ihl"          , c_uint8, 4),
        ("version"      , c_uint8, 4),
        ("tos"          , c_uint8   ),
        ("len"          , c_uint16  ),
        ("id"           , c_uint16  ),
        ("offset"       , c_uint16  ),
        ("ttl"          , c_uint8   ),
        ("protocol_num" , c_uint8   ),
        ("sum"          , c_uint16  ),
        ("src"          , c_uint32  ),
        ("dst"          , c_uint32  )
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
