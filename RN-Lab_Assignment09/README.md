# RN-Lab – ÜB9

This package keeps the ÜB9 assignment scope unchanged:
Ethernet, ARP and switching on a four-host LAN.

Start:

    sudo python3 start_lab.py

The startup script:
- creates the four-host / one-switch LAN
- explicitly configures the IPv4 addresses
- prints the actual interface/routing state
- verifies LAN connectivity
- opens terminals only after successful verification

Addresses:
- client1: 10.0.1.2/24
- client2: 10.0.1.3/24
- server1: 10.0.1.10/24
- server2: 10.0.1.11/24

No router or default gateway is required because all hosts are in the
same IPv4 LAN.

Useful commands from the assignment:

    ip -br addr
    ip link
    ip neigh
    ping -c 4 10.0.1.3
    ip neigh flush all
    tcpdump -i client1-eth0 -nn -e arp
    ovs-ofctl dump-flows s1

The capture helper includes Ethernet headers with tcpdump -e.
