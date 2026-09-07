# ÜB10 – Network Forensics

The assignment text and forensic scenario remain unchanged. The Python
infrastructure has been cleaned up so that topology definition and
runtime configuration are separated.

## Start

    sudo python3 start_lab.py

The environment opens terminals for client1, client2, router and server.

At startup the script:

1. creates the existing topology
2. explicitly configures all IPv4 addresses
3. configures the client routes
4. preserves the intentional server-side configuration fault
5. prints the actual interface and routing state
6. verifies the healthy local infrastructure
7. confirms the expected end-to-end failure
8. opens the terminals

The intentional fault is deliberately not repaired by the startup script.

## Application test

On the server:

    python3 tcp_server.py

On client1:

    python3 tcp_client.py 10.10.2.10

Do not immediately change the configuration. Follow the forensic workflow in the assignment.

## Useful commands

    ip -br addr
    ip route
    ip neigh
    ping -c 3 10.10.2.10
    traceroute 10.10.2.10

## Packet capture

    ./capture_client.sh
    ./capture_router.sh
    ./capture_server.sh

Open the resulting PCAP files in Wireshark.

## Important

The environment contains an intentional configuration fault. Students are expected
to identify it from evidence. The application code is not the intended place to fix
the problem.
