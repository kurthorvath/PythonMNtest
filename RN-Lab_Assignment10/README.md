
# ÜB10 – Network Forensics

## Start

    sudo python3 start_lab.py

The environment opens terminals for client1, client2, router and server.

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
