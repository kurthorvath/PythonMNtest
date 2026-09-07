#!/usr/bin/env python3
"""Start the RN-Lab environment for Assignment 10.

The exercise deliberately contains a forensic configuration fault.
This script configures the complete network, prints the actual state,
checks the healthy local links, confirms the expected end-to-end
failure, and then opens the terminals.

The intentional fault is NOT repaired here: students must identify it
during the forensic exercise.
"""

import sys

from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

from topology import ForensicsTopo


def configure_interface(node, interface, address):
    """Explicitly configure one IPv4 interface."""
    node.cmd(f"ip addr flush dev {interface}")
    node.cmd(f"ip addr add {address} dev {interface}")
    node.cmd(f"ip link set dev {interface} up")


def configure_addresses(net):
    addresses = {
        "client1": [
            ("client1-eth0", "10.10.1.10/24"),
        ],
        "client2": [
            ("client2-eth0", "10.10.1.11/24"),
        ],
        "router": [
            ("router-eth0", "10.10.1.1/24"),
            ("router-eth1", "10.10.2.1/24"),
        ],
        "server": [
            ("server-eth0", "10.10.2.10/24"),
        ],
    }

    for node_name, interfaces in addresses.items():
        node = net[node_name]
        for interface, address in interfaces:
            configure_interface(node, interface, address)


def configure_routes(net):
    """Configure normal host routing, then install the intentional fault."""
    client1 = net["client1"]
    client2 = net["client2"]
    server = net["server"]

    client1.cmd("ip route replace default via 10.10.1.1 dev client1-eth0")
    client2.cmd("ip route replace default via 10.10.1.1 dev client2-eth0")

    # Intentional forensic fault:
    # the server's real gateway is 10.10.2.1, but the configured gateway
    # is deliberately invalid. Do not repair this in the startup script.
    server.cmd("ip route replace default via 10.10.2.254 dev server-eth0")


def print_network_state(net):
    info("\n" + "=" * 72 + "\n")
    info("*** ÜB10: actual network configuration\n")
    info("=" * 72 + "\n")

    for node in net.hosts:
        info(f"\n--- {node.name} ---\n")
        info(node.cmd("ip -br addr"))
        info("\n")
        info(node.cmd("ip route"))
        info("\n")

    info("=" * 72 + "\n")


def check(node, command, description):
    output = node.cmd(command).strip()
    success = node.lastCmdWasOK()

    status = "OK" if success else "FAILED"
    info(f"  [{status}] {description}\n")

    if not success and output:
        info(f"       {output}\n")

    return success


def verify_environment(net):
    """Check healthy infrastructure and confirm the intentional failure."""
    client1 = net["client1"]
    client2 = net["client2"]
    router = net["router"]

    info("\n*** Verifying the forensic baseline...\n")

    healthy_tests = [
        (client1, "ping -c 1 -W 1 10.10.1.1",
         "client1 -> router"),
        (client2, "ping -c 1 -W 1 10.10.1.1",
         "client2 -> router"),
        (router, "ping -c 1 -W 1 10.10.2.10",
         "router -> server"),
    ]

    failures = 0
    for node, command, description in healthy_tests:
        if not check(node, command, description):
            failures += 1

    if failures:
        info(
            f"\n*** ERROR: {failures} healthy infrastructure test(s) failed.\n"
            "*** The forensic environment cannot be started reliably.\n"
        )
        return False

    # This failure is intentional and is part of the forensic evidence.
    info("\n*** Expected forensic symptom:\n")
    server_reachable = check(
        client1,
        "ping -c 1 -W 1 10.10.2.10",
        "client1 -> server (expected to fail)"
    )

    if server_reachable:
        info(
            "*** WARNING: the expected end-to-end failure did not occur.\n"
            "*** Check whether the intentional fault was altered.\n"
        )
    else:
        info("*** Expected end-to-end failure confirmed.\n")

    return True


def main():
    net = Mininet(
        topo=ForensicsTopo(),
        controller=None,
        autoSetMacs=True
    )

    try:
        info("*** Starting ÜB10 forensic Mininet environment...\n")
        net.start()

        configure_addresses(net)
        configure_routes(net)

        print_network_state(net)

        if not verify_environment(net):
            net.stop()
            sys.exit(1)

        info(
            "\n*** Environment ready. "
            "Do not repair the configuration before following the "
            "forensic workflow in the assignment.\n"
        )

        for host, title in [
            (net["client1"], "ÜB10 client1"),
            (net["client2"], "ÜB10 client2"),
            (net["router"], "ÜB10 router"),
            (net["server"], "ÜB10 server"),
        ]:
            makeTerm(host, title=title)

        try:
            input("\nPress ENTER to stop the Mininet environment...")
        except KeyboardInterrupt:
            pass

    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
