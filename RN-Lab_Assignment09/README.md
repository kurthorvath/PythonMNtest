# ÜB9 student environment

The assignment text and pedagogical scope are unchanged. The Python
infrastructure has been cleaned up so that topology definition and
runtime network configuration are separated.

## Start

```bash
sudo python3 start_lab.py
```

The startup script:

1. creates the existing four-host / one-switch LAN
2. explicitly configures the IPv4 addresses
3. prints the actual interface and routing state
4. verifies LAN connectivity
5. opens the host terminals only after successful verification

## Base LAN

```text
client1 ----\
client2 ----- switch ---- server1
server2 ----/
```

Addresses:

- client1: 10.0.1.2/24
- client2: 10.0.1.3/24
- server1: 10.0.1.10/24
- server2: 10.0.1.11/24

There is no router or default gateway because all four hosts are on
the same IPv4 LAN.

## Useful commands

```bash
ip -br addr
ip neigh
ping -c 3 10.0.1.10
./capture.sh eth0 /tmp/ub9.pcap
./inspect_switch.sh
```

The focus remains Ethernet, ARP, MAC addresses, broadcast/flooding
and switch learning.
