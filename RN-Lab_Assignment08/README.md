# RN-Lab – ÜB8

This package implements the **initial topology from Ü8.1**. The
assignment text is the specification.

## Initial topology

    client1 \
              switch -- r1 -- r2 -- server
    client2 /

The two clients are on the same left LAN.

## Important

The additional router `r3` and the alternative path are deliberately
NOT included in the supplied topology. They are introduced by the
student in Ü8.2, exactly as required by the assignment.

Likewise, the different link delays of Ü8.3 are configured by the
student in `topology.py`.

The startup script only prepares and verifies the initial Ü8.1
environment.

## Start

    sudo python3 start_lab.py

The script explicitly configures the initial IP addresses and routes,
prints the actual configuration, verifies the initial end-to-end
connection, and then opens the terminals.

## Initial addressing

- client1: 10.0.1.2/24
- client2: 10.0.1.3/24
- r1-eth0: 10.0.1.1/24
- r1-eth1: 10.0.12.1/30
- r2-eth0: 10.0.12.2/30
- r2-eth1: 10.0.2.1/24
- server-eth0: 10.0.2.2/24

Useful commands from the assignment:

    ip -br addr
    ip route
    ping -c 3 10.0.2.2
    traceroute 10.0.2.2

The TCP client/server remain unchanged.
