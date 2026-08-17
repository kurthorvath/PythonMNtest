# Student scripts – Assignment 06

## Start

    sudo python3 start_lab.py

Base topology:

    client -- r1 -- r2 -- server

## Useful commands

On any Mininet node:

    ip -br addr
    ip route
    ip neigh

On routers:

    sysctl net.ipv4.ip_forward

## Connectivity

    ./run_ping_tests.sh

## traceroute

    ./run_traceroute.sh

## Packet capture

On a node:

    ./capture_interface.sh eth0 /tmp/a06-eth0.pcap

On a router:

    ./capture_all.sh

## TCP end-to-end experiment

Server:

    python3 tcp_server.py

Client:

    python3 tcp_client.py

## Topology editing

Beginning with Ü 6.6, edit topology.py.

The intended first modification is to add another client to the LAN connected to r1.
Do not change the application protocol.

You will also need to configure the new host's default route.
