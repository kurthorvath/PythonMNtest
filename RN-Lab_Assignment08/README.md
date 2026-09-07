# RN-Lab – Assignment 08

Updated infrastructure only; the ÜB8 assignment text and topology
concept are unchanged.

Start with:

    sudo python3 start_lab.py

The startup script explicitly configures addresses/routes, prints the
actual network state, verifies connectivity, and opens terminals only
after successful verification.

The two routing paths remain:

    R1 -- R2 -- Server
    R1 -- R3 -- Server

with 5 ms links on the R2 path and 30 ms links on the R3 path.

Useful commands:

    ip -br addr
    ip route
    ping -c 3 10.0.2.2
    traceroute 10.0.2.2
    ./capture.sh eth0 /tmp/ub8.pcap
