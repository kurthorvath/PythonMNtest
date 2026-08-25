#!/bin/bash
OUT="${1:-/tmp/ub10-client.pcap}"
echo "Capturing client traffic -> $OUT"
tcpdump -i any -nn -e -s 0 -w "$OUT"
