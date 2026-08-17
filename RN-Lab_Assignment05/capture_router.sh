#!/bin/bash
# Run inside the router Mininet terminal.
# Stop with Ctrl+C.
tcpdump -i any -nn -s 0 -w /tmp/a05-router.pcap
