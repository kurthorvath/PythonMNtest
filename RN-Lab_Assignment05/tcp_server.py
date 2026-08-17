#!/usr/bin/env python3
"""Simple TCP echo server for Assignment 05."""

import socket

HOST = "10.0.2.2"
PORT = 5000
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"TCP server listening on {HOST}:{PORT}")

    while True:
        connection, address = server.accept()
        print(f"Connection from {address}")

        with connection:
            while True:
                data = connection.recv(BUFFER_SIZE)

                if not data:
                    break

                print(f"Received {len(data)} bytes: {data[:80]!r}")
                connection.sendall(data)
