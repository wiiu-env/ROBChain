ATTACKER_IP = [192, 168, 178, 161]  # IP of the device which runs the python scripts
TCP_SERVER_PORT = 12345             # A free usable port on the attacking device

CODE_BIN_PATH = 'code.bin'                   # Path to the code.bin payload that will be executed
CODE_BIN_TARGET_ADDR = 0x011DE200            # Address where the payload should be copied to
CODE_BIN_ENTRYPOINT = CODE_BIN_TARGET_ADDR   # Absolute address of the entrypoint of the copied payload
