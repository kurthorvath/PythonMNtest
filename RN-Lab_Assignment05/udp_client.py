#!/usr/bin/env python3
"""Simple UDP client for the TCP/UDP comparison."""

import socket

SERVER = "10.0.2.2"
PORT = 5002

message = b"Hello UDP from Mininet!"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(2)
    client.sendto(message, (SERVER, PORT))

    try:
        data, address = client.recvfrom(65535)
        print(f"Received {data!r} from {address}")
    except socket.timeout:
        print("No UDP response received.")
