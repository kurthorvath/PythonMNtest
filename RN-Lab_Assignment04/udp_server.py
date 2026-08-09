#!/usr/bin/env python3
import socket

HOST = "10.0.2.2"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

while True:
    data, address = server.recvfrom(4096)
    print(f"Received from {address}: {data!r}")
