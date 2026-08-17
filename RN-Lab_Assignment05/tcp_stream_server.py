#!/usr/bin/env python3
"""Server for the TCP byte-stream experiment."""

import socket

HOST = "10.0.2.2"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Listening on {HOST}:{PORT}")

    connection, address = server.accept()

    with connection:
        print(f"Connection from {address}")

        while True:
            data = connection.recv(8)

            if not data:
                break

            print(f"recv(8) -> {len(data)} bytes: {data!r}")
