# ÜB9 student environment

Start:
    sudo python3 start_lab.py

The base LAN is:
    client1 ----\
    client2 ----- switch ---- server1
    server2 ----/

Useful:
    ip -br addr
    ip neigh
    ping -c 3 10.0.1.10
    ./capture.sh eth0 /tmp/ub9.pcap
    ./inspect_switch.sh

The focus is Ethernet, ARP, MAC addresses, broadcast/flooding and switch learning.
