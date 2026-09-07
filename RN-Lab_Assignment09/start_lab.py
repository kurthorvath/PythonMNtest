#!/usr/bin/env python3
"""Start the RN-Lab environment for Assignment 09.

The topology is defined in topology.py. This script explicitly
configures the IPv4 addresses, prints the actual network state,
verifies LAN connectivity, and only then opens the terminals.
"""

import sys

from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

from topology import EthernetLabTopo


HOST_ADDRESSES = {
    "client1": ("client1-eth0", "10.0.1.2/24"),
    "client2": ("client2-eth0", "10.0.1.3/24"),
    "server1": ("server1-eth0", "10.0.1.10/24"),
    "server2": ("server2-eth0", "10.0.1.11/24"),
}


def configure_addresses(net):
    """Explicitly configure all host IPv4 addresses."""
    for host_name, (interface, address) in HOST_ADDRESSES.items():
        host = net[host_name]
        host.cmd(f"ip addr flush dev {interface}")
        host.cmd(f"ip addr add {address} dev {interface}")
        host.cmd(f"ip link set dev {interface} up")


def print_network_state(net):
    info("\\n" + "=" * 72 + "\\n")
    info("*** ÜB9: actual Ethernet/LAN configuration\\n")
    info("=" * 72 + "\\n")

    for host in net.hosts:
        info(f"\\n--- {host.name} ---\\n")
        info(host.cmd("ip -br addr"))
        info("\\n")
        info(host.cmd("ip route"))

    info("\\n--- switch s1 ---\\n")
    info(net["s1"].cmd("ovs-ofctl show s1 2>/dev/null || true"))
    info("\\n")

    info("=" * 72 + "\\n")


def check(node, command, description):
    """Run one connectivity check and report its result."""
    output = node.cmd(command).strip()
    success = node.lastCmdWasOK()

    status = "OK" if success else "FAILED"
    info(f"  [{status}] {description}\\n")

    if not success and output:
        info(f"       {output}\\n")

    return success


def verify_connectivity(net):
    """Verify all hosts can communicate on the LAN."""
    info("\\n*** Verifying LAN connectivity before opening terminals...\\n")

    tests = [
        (net["client1"], "ping -c 1 -W 1 10.0.1.3",
         "client1 -> client2"),
        (net["client1"], "ping -c 1 -W 1 10.0.1.10",
         "client1 -> server1"),
        (net["client1"], "ping -c 1 -W 1 10.0.1.11",
         "client1 -> server2"),

        (net["client2"], "ping -c 1 -W 1 10.0.1.2",
         "client2 -> client1"),
        (net["client2"], "ping -c 1 -W 1 10.0.1.10",
         "client2 -> server1"),
        (net["client2"], "ping -c 1 -W 1 10.0.1.11",
         "client2 -> server2"),

        (net["server1"], "ping -c 1 -W 1 10.0.1.2",
         "server1 -> client1"),
        (net["server2"], "ping -c 1 -W 1 10.0.1.3",
         "server2 -> client2"),
    ]

    failures = sum(
        not check(node, command, description)
        for node, command, description in tests
    )

    if failures:
        info(
            f"\\n*** ERROR: {failures} connectivity test(s) failed.\\n"
            "*** Terminals will not be opened.\\n"
        )
        return False

    info("\\n*** All LAN connectivity checks passed.\\n")
    return True


def main():
    net = Mininet(
        topo=EthernetLabTopo(),
        controller=None,
        autoSetMacs=True
    )

    try:
        info("*** Starting ÜB9 Mininet environment...\\n")
        net.start()

        configure_addresses(net)
        print_network_state(net)

        if not verify_connectivity(net):
            net.stop()
            sys.exit(1)

        info("\\n*** Opening ÜB9 terminals...\\n")

        for host in net.hosts:
            makeTerm(host, title=f"ÜB9 {host.name}")

        try:
            input("\\nPress ENTER to stop ÜB9...")
        except KeyboardInterrupt:
            pass

    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
