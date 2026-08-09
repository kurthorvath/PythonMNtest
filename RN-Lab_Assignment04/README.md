# RN-Lab – Assignment 04

## Files

- `standard_mininet.py`: introductory h1–s1–h2 topology.
- `topology.py`: provided client–router–server infrastructure.
- `start_lab.py`: starts the Assignment 04 environment and opens three host consoles.
- `udp_client.py`, `udp_server.py`: example application programs.
- `check_environment.py`: checks the VM installation.

## Check the VM

    python3 check_environment.py

## Introductory Mininet

    sudo python3 standard_mininet.py

Use the Mininet CLI:

    nodes
    net
    links
    dump

and commands such as:

    h1 ip addr
    h1 ip route
    h1 ping -c 4 h2

## RN-Lab

    sudo python3 start_lab.py

Topology:

    client -------- router -------- server
    10.0.1.2       10.0.1.1        10.0.2.2
                   10.0.2.1

The infrastructure files are provided by the course and should not be modified unless an exercise explicitly says so.

## UDP example

Run `udp_server.py` in the server console and `udp_client.py` in the client console.

Network conditions are configured at the top of `topology.py`:

    LINK_DELAY = "20ms"
    LINK_LOSS = 0
