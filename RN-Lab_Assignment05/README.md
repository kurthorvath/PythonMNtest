# Student scripts – Assignment 05

## Start the environment

Run from this directory:

    sudo python3 start_lab.py

Three Mininet terminals are opened:
- A05 Client
- A05 Router
- A05 Server

## TCP

On the server terminal:

    python3 tcp_server.py

On the client terminal:

    python3 tcp_client.py

## TCP byte stream

Server:

    python3 tcp_stream_server.py

Client:

    python3 tcp_stream_client.py

Then modify the programs as required by Ü 5.2.

## Packet capture

Inside the client terminal:

    ./capture_client.sh

or directly:

    tcpdump -i client-eth0 -nn -s 0 -w /tmp/a05-client.pcap

Copy the pcap file to the host if required for Wireshark.

## iperf3

Server:

    ./run_iperf_server.sh

Client:

    ./run_iperf_tcp.sh

UDP:

    ./run_iperf_udp.sh

## Experiments

Change only the parameters requested in the assignment:

    LINK_DELAY = "20ms"
    LINK_LOSS = 0

Examples:

    LINK_DELAY = "50ms"
    LINK_LOSS = 5

Restart the Mininet experiment after changing topology.py.
