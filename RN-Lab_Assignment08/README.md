# RN-Lab – Assignment 08

The assignment text remains unchanged. This package only updates the
Mininet infrastructure so that the existing topology and routing
experiments are configured reliably.

## Start

```bash
sudo python3 start_lab.py
```

The startup script:

1. creates the topology from `topology.py`
2. explicitly configures all IPv4 addresses
3. enables IPv4 forwarding on the routers
4. installs the required static routes
5. prints the actual `ip -br addr` and `ip route` state
6. verifies local and end-to-end connectivity
7. opens the host/router terminals only if verification succeeds

## Topology

The original two-path routing topology is retained:

- client1 → r1
- client2 → r1
- r1 → r2 → server
- r1 → r3 → server

The R1–R2–server path uses 5 ms links, while the R1–R3–server
path uses 30 ms links.

## Files

- `topology.py` – topology and link characteristics
- `start_lab.py` – runtime IP/routing configuration and verification
- `capture.sh` – packet capture helper
