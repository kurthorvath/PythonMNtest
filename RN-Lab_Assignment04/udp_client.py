#!/usr/bin/env python3
import socket

SERVER = "10.0.2.2"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b"Hello from Mininet!"
client.sendto(message, (SERVER, PORT))
print(f"Sent {message!r} to {SERVER}:{PORT}")
