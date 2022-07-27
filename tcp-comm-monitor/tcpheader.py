import socket
import struct
from ctypes import *

class TCP(Structure):
    _fields_ = [
        ("src"     ,c_uint16   ),
        ("dst"     ,c_uint16   ),
        ("seq"     ,c_uint32   ),
        ("ack_seq" ,c_uint32   ),
        ("res1"    ,c_uint16, 4),
        ("doff"    ,c_uint16, 4),
        ("fin"     ,c_uint16, 1),
        ("syn"     ,c_uint16, 1),
        ("rst"     ,c_uint16, 1),
        ("psh"     ,c_uint16, 1),
        ("ack"     ,c_uint16, 1),
        ("urg"     ,c_uint16, 1),
        ("res2"    ,c_uint16, 2),
        ("window"  ,c_uint16   ),
        ("check"   ,c_uint16   ),
        ("urg_ptr" ,c_uint16   )
    ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.src_port    = socket.ntohs(self.src)
        #self.src_port    = struct.unpack("<H",struct.pack(">H",self.src))[0]
        self.dst_port    = socket.ntohs(self.dst)
        self.seq_no      = socket.ntohl(self.seq)
        self.ack_seq_no  = socket.ntohl(self.ack_seq)
        self.window_size = socket.ntohs(self.window)
