#!/bin/bash
# Run inside the client Mininet terminal.
# Stop with Ctrl+C.
tcpdump -i client-eth0 -nn -s 0 -w /tmp/a05-client.pcap
