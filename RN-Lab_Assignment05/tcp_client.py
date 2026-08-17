#!/usr/bin/env python3
"""Simple TCP client for Assignment 05."""

import socket
import time

SERVER = "10.0.2.2"
PORT = 5000

messages = [
    b"Hello\n",
    b"from\n",
    b"Python\n",
    b"and Mininet!\n",
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((SERVER, PORT))
    print(f"Connected to {SERVER}:{PORT}")

    for message in messages:
        print(f"Sending {message!r}")
        client.sendall(message)

        reply = client.recv(4096)
        print(f"Received {reply!r}")

        time.sleep(0.2)
