# ÜB6 infrastructure correction

This version applies the RN-Lab infrastructure standard used from ÜB4 onward.

## Base topology

```text
client -------- r1 -------- r2 -------- server
10.0.1.2/24     10.0.12.1/30  10.0.12.2/30     10.0.2.2/24
                10.0.1.1      10.0.2.1
```

All three links use the `LINK_DELAY` value in `topology.py` (10 ms by default).

## What `start_lab.py` now guarantees

Before opening terminals it:

1. explicitly configures every interface;
2. explicitly brings every interface up;
3. configures the client and server default routes;
4. configures the two static inter-router routes;
5. enables IPv4 forwarding on both routers;
6. prints the actual interface and routing state;
7. verifies connectivity on every hop;
8. verifies end-to-end client -> server and server -> client ping.

If any check fails, the terminals are not opened.

## Student topology editing

The base topology remains deliberately simple. Starting with Ü 6.6,
students modify `topology.py` as required by the exercise.

When a new host or interface is introduced, the corresponding IP
configuration and routes must also be added to `start_lab.py`. This is
intentional: the exercise is about understanding topology, addressing and
routing, not about hiding the configuration in a framework.

The existing `route_reference.txt` is only a reference and should not be
blindly copied into the solution.

## Useful tests

From the client:

```bash
ping -c 4 10.0.1.1
ping -c 4 10.0.2.2
```

From the server:

```bash
ping -c 4 10.0.2.1
ping -c 4 10.0.1.2
```

From the routers:

```bash
ip -br addr
ip route
sysctl net.ipv4.ip_forward
```

For path observation:

```bash
./run_traceroute.sh
```

For packet capture:

```bash
./capture_interface.sh eth0 /tmp/a06-eth0.pcap
```
