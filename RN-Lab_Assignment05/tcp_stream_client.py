#!/usr/bin/env python3
"""
Client for the TCP byte-stream experiment.

Use this together with tcp_stream_server.py.
Students should experiment with message sizes and send/recv calls.
"""

import socket

SERVER = "10.0.2.2"
PORT = 5001

chunks = [
    b"AAAAA",
    b"BBBBB",
    b"CCCCC",
    b"DDDDD",
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((SERVER, PORT))
    print(f"Connected to {SERVER}:{PORT}")

    for chunk in chunks:
        print(f"send(): {chunk!r}")
        client.sendall(chunk)

    client.shutdown(socket.SHUT_WR)

    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"recv(): {len(data)} bytes -> {data!r}")
