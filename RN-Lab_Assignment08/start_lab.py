#!/usr/bin/env python3
"""Start the RN-Lab environment for Assignment 08.

The topology is defined in topology.py. This script performs the
runtime IP/routing configuration, prints the actual state, verifies
connectivity, and opens terminals only after successful verification.
"""

import sys

from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

from topology import RoutingLabTopo


def configure_interface(node, interface, address):
    node.cmd(f"ip addr flush dev {interface}")
    node.cmd(f"ip addr add {address} dev {interface}")
    node.cmd(f"ip link set dev {interface} up")


def configure_addresses(net):
    addresses = {
        "client1": [("client1-eth0", "10.0.1.2/24")],
        "client2": [("client2-eth0", "10.0.1.3/24")],
        "r1": [
            ("r1-eth0", "10.0.1.1/24"),
            ("r1-eth0b", "10.0.1.4/24"),
            ("r1-eth1", "10.0.12.1/30"),
            ("r1-eth2", "10.0.13.1/30"),
        ],
        "r2": [
            ("r2-eth0", "10.0.12.2/30"),
            ("r2-eth1", "10.0.2.1/24"),
        ],
        "r3": [
            ("r3-eth0", "10.0.13.2/30"),
            ("r3-eth1", "10.0.3.1/24"),
        ],
        "server": [
            ("server-eth0", "10.0.2.2/24"),
            ("server-eth1", "10.0.3.2/24"),
        ],
    }

    for node_name, interfaces in addresses.items():
        node = net[node_name]
        for interface, address in interfaces:
            configure_interface(node, interface, address)


def configure_routes(net):
    client1 = net["client1"]
    client2 = net["client2"]
    r1 = net["r1"]
    r2 = net["r2"]
    r3 = net["r3"]
    server = net["server"]

    client1.cmd("ip route replace default via 10.0.1.1 dev client1-eth0")
    client2.cmd("ip route replace default via 10.0.1.4 dev client2-eth0")

    r1.cmd("ip route replace 10.0.2.0/24 via 10.0.12.2 dev r1-eth1")
    r1.cmd("ip route replace 10.0.3.0/24 via 10.0.13.2 dev r1-eth2")

    r2.cmd("ip route replace 10.0.1.0/24 via 10.0.12.1 dev r2-eth0")
    r2.cmd("ip route replace 10.0.3.0/24 via 10.0.12.1 dev r2-eth0")

    r3.cmd("ip route replace 10.0.1.0/24 via 10.0.13.1 dev r3-eth0")
    r3.cmd("ip route replace 10.0.2.0/24 via 10.0.13.1 dev r3-eth0")

    server.cmd("ip route replace 10.0.1.0/24 via 10.0.2.1 dev server-eth0")


def print_network_state(net):
    info("\n" + "=" * 72 + "\n")
    info("*** ÜB8: actual network configuration\n")
    info("=" * 72 + "\n")

    for node in net.hosts:
        info(f"\n--- {node.name} ---\n")
        info(node.cmd("ip -br addr"))
        info("\n")
        info(node.cmd("ip route"))
        info("\n")

    info("=" * 72 + "\n")


def check(node, command, description):
    """Run a command and determine success without lastCmdWasOK()."""
    marker = "__RN_LAB_RC__"
    output = node.cmd(f"{command}; printf '\\n{marker}%s\\n' $?")
    lines = output.rstrip().splitlines()

    rc = None
    clean_lines = []
    for line in lines:
        if line.startswith(marker):
            try:
                rc = int(line[len(marker):])
            except ValueError:
                rc = None
        else:
            clean_lines.append(line)

    success = rc == 0
    status = "OK" if success else "FAILED"
    info(f"  [{status}] {description}\n")

    if not success:
        detail = "\n".join(clean_lines).strip()
        if detail:
            info(f"       {detail}\n")

    return success


def verify_connectivity(net):
    client1 = net["client1"]
    client2 = net["client2"]
    r1 = net["r1"]
    r2 = net["r2"]
    r3 = net["r3"]
    server = net["server"]

    info("\n*** Verifying connectivity before opening terminals...\n")

    tests = [
        (client1, "ping -c 1 -W 1 10.0.1.1", "client1 -> r1"),
        (client2, "ping -c 1 -W 1 10.0.1.4", "client2 -> r1"),

        (r1, "ping -c 1 -W 1 10.0.12.2", "r1 -> r2"),
        (r1, "ping -c 1 -W 1 10.0.13.2", "r1 -> r3"),

        (r2, "ping -c 1 -W 1 10.0.2.2", "r2 -> server"),
        (r3, "ping -c 1 -W 1 10.0.3.2", "r3 -> server"),

        (client1, "ping -c 1 -W 1 10.0.2.2", "client1 -> server"),
        (client2, "ping -c 1 -W 1 10.0.2.2", "client2 -> server"),

        (server, "ping -c 1 -W 1 10.0.1.2", "server -> client1"),
        (server, "ping -c 1 -W 1 10.0.1.3", "server -> client2"),
    ]

    failures = 0
    for node, command, description in tests:
        if not check(node, command, description):
            failures += 1

    if failures:
        info(
            f"\n*** ERROR: {failures} connectivity test(s) failed.\n"
            "*** Terminals will not be opened.\n"
            "*** Inspect the configuration above.\n"
        )
        return False

    info("\n*** All connectivity checks passed.\n")
    return True


def main():
    net = Mininet(
        topo=RoutingLabTopo(),
        controller=None,
        autoSetMacs=True
    )

    try:
        info("*** Starting ÜB8 Mininet environment...\n")
        net.start()

        configure_addresses(net)
        configure_routes(net)
        print_network_state(net)

        if not verify_connectivity(net):
            net.stop()
            sys.exit(1)

        info("\n*** Opening ÜB8 terminals...\n")

        for host, title in [
            (net["client1"], "ÜB8 Client 1"),
            (net["client2"], "ÜB8 Client 2"),
            (net["r1"], "ÜB8 Router 1"),
            (net["r2"], "ÜB8 Router 2"),
            (net["r3"], "ÜB8 Router 3"),
            (net["server"], "ÜB8 Server"),
        ]:
            makeTerm(host, title=title)

        try:
            input("\nPress ENTER to stop ÜB8...")
        except KeyboardInterrupt:
            pass

    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
