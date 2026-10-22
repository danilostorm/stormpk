#!/usr/bin/env python3
"""Local-only protocol compatibility probe. Captures an 8-byte header, never credentials.

The listener is a disposable synthetic test endpoint, not a Login Server or relay.
It does not proxy connections, accept accounts or query databases.
"""
import argparse
import json
import socket
import struct
import sys

LOGIN_PACKET=0x48480001
VERSION=1309
MAX_PACKET_SIZE=0x2000


def inspect_header(data):
    if len(data)!=8:
        return {'status':'incomplete', 'header_bytes':len(data)}
    length, enc_index, encrypted, opcode=struct.unpack('<HBBI',data)
    valid=8 <= length <= MAX_PACKET_SIZE
    return {'status': 'stormpk-header-candidate' if valid else 'invalid-stormpk-frame',
            'declared_length':length, 'encrypted_flag':bool(encrypted),
            'encryption_key_index':enc_index,'opcode_hex':f'0x{opcode:08X}',
            'stormpk_login_opcode': opcode==LOGIN_PACKET,
            'stormpk_login_version': VERSION,
            'note':'Only header checked; never validates client/protocol/login compatibility'}


def run_probe():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1',0))
        server.listen(1)
        server.settimeout(20)
        print('LOCAL_PROBE_PORT='+str(server.getsockname()[1]), flush=True)
        try:
            connection,_=server.accept()
        except socket.timeout:
            print(json.dumps({'status':'timed-out-no-client'}));return
        with connection:
            connection.settimeout(4)
            data=b''
            while len(data)<8:
                try:chunk=connection.recv(8-len(data))
                except socket.timeout:break
                if not chunk:break
                data+=chunk
            print(json.dumps(inspect_header(data),ensure_ascii=False,sort_keys=True), flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--decode',help='Decode exactly 8 header bytes as hex')
    p.add_argument('--listen',action='store_true',help='Bind 127.0.0.1 on an ephemeral port and inspect first header only')
    args=p.parse_args()
    if args.decode:
        data=bytes.fromhex(args.decode)
        print(json.dumps(inspect_header(data),indent=2,sort_keys=True))
    elif args.listen:run_probe()
    else:p.print_help()

if __name__=='__main__':main()
