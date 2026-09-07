#!/usr/bin/env python3
"""
Start the initial RN-Lab environment for ÜB8.

Only the initial topology from Ü8.1 is configured here.
The additional router r3 and alternative path required in Ü8.2
are deliberately left for the students to implement.
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


def configure_initial_addresses(net):
    addresses = {
        "client1": [("client1-eth0", "10.0.1.2/24")],
        "client2": [("client2-eth0", "10.0.1.3/24")],
        "r1": [
            ("r1-eth0", "10.0.1.1/24"),
            ("r1-eth1", "10.0.12.1/30"),
        ],
        "r2": [
            ("r2-eth0", "10.0.12.2/30"),
            ("r2-eth1", "10.0.2.1/24"),
        ],
        "server": [
            ("server-eth0", "10.0.2.2/24"),
        ],
    }

    for node_name, interfaces in addresses.items():
        for interface, address in interfaces:
            configure_interface(net[node_name], interface, address)


def configure_initial_routes(net):
    net["client1"].cmd(
        "ip route replace default via 10.0.1.1 dev client1-eth0"
    )
    net["client2"].cmd(
        "ip route replace default via 10.0.1.1 dev client2-eth0"
    )

    net["r1"].cmd(
        "ip route replace 10.0.2.0/24 via 10.0.12.2 dev r1-eth1"
    )

    net["r2"].cmd(
        "ip route replace 10.0.1.0/24 via 10.0.12.1 dev r2-eth0"
    )

    net["server"].cmd(
        "ip route replace 10.0.1.0/24 via 10.0.2.1 dev server-eth0"
    )


def print_network_state(net):
    info("\n" + "=" * 72 + "\n")
    info("*** ÜB8 initial network configuration\n")
    info("=" * 72 + "\n")

    for node in net.hosts:
        info(f"\n--- {node.name} ---\n")
        info(node.cmd("ip -br addr"))
        info("\n")
        info(node.cmd("ip route"))
        info("\n")

    info("--- switch s1 ---\n")
    info(net["s1"].cmd("ovs-vsctl get-fail-mode s1"))
    info("\n")
    info(net["s1"].cmd("ovs-ofctl show s1 2>/dev/null || true"))
    info("\n")

    info("=" * 72 + "\n")


def check(node, command, description):
    """Run a command and evaluate its shell return code portably."""
    marker = "__RN_RC__"
    output = node.cmd(f"{command}; printf '\\n{marker}%s\\n' $?")

    rc = None
    details = []

    for line in output.rstrip().splitlines():
        if line.startswith(marker):
            try:
                rc = int(line[len(marker):])
            except ValueError:
                rc = None
        else:
            details.append(line)

    success = rc == 0
    info(f"  [{'OK' if success else 'FAILED'}] {description}\n")

    if not success:
        detail = "\n".join(details).strip()
        if detail:
            info(f"       {detail}\n")

    return success


def verify_initial_topology(net):
    info("\n*** Verifying initial ÜB8 topology...\n")

    switch_mode = net["s1"].cmd(
        "ovs-vsctl get-fail-mode s1"
    ).strip()

    if switch_mode != "standalone":
        info(
            f"  [FAILED] switch s1 is not in standalone mode "
            f"(reported: {switch_mode or 'unknown'})\n"
        )
        return False

    info("  [OK] switch s1 is in standalone mode\n")

    tests = [
        (net["client1"], "ping -c 1 -W 1 10.0.1.1",
         "client1 -> r1"),
        (net["client2"], "ping -c 1 -W 1 10.0.1.1",
         "client2 -> r1"),
        (net["r1"], "ping -c 1 -W 1 10.0.12.2",
         "r1 -> r2"),
        (net["r2"], "ping -c 1 -W 1 10.0.2.2",
         "r2 -> server"),
        (net["client1"], "ping -c 1 -W 1 10.0.2.2",
         "client1 -> server"),
        (net["server"], "ping -c 1 -W 1 10.0.1.2",
         "server -> client1"),
    ]

    failures = 0
    for node, command, description in tests:
        if not check(node, command, description):
            failures += 1

    if failures:
        info(
            f"\n*** ERROR: {failures} initial connectivity test(s) failed.\n"
            "*** Terminals will not be opened.\n"
        )
        return False

    info("\n*** Initial topology verified successfully.\n")
    return True


def main():
    net = Mininet(
        topo=RoutingLabTopo(),
        controller=None,
        autoSetMacs=True
    )

    try:
        info("*** Starting ÜB8 initial Mininet environment...\n")
        net.start()

        configure_initial_addresses(net)
        configure_initial_routes(net)
        print_network_state(net)

        if not verify_initial_topology(net):
            return 1

        info("\n*** Opening ÜB8 terminals...\n")

        for host, title in [
            (net["client1"], "ÜB8 Client 1"),
            (net["client2"], "ÜB8 Client 2"),
            (net["r1"], "ÜB8 Router 1"),
            (net["r2"], "ÜB8 Router 2"),
            (net["server"], "ÜB8 Server"),
        ]:
            makeTerm(host, title=title)

        try:
            input("\nPress ENTER to stop ÜB8...")
        except KeyboardInterrupt:
            pass

        return 0

    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    sys.exit(main())
