#!/bin/bash
OUT="${1:-/tmp/ub10-server.pcap}"
echo "Capturing server traffic -> $OUT"
tcpdump -i any -nn -e -s 0 -w "$OUT"
