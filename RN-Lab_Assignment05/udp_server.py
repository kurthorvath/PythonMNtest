#!/usr/bin/env python3
"""Simple UDP server for the TCP/UDP comparison."""

import socket

HOST = "10.0.2.2"
PORT = 5002

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    while True:
        data, address = server.recvfrom(65535)
        print(f"Received {len(data)} bytes from {address}")
        server.sendto(data, address)
