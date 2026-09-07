#!/usr/bin/env python3
"""RN-Lab topology for Assignment 08.

Infrastructure only:
- topology and link characteristics are defined here
- IP addresses and routing are configured by start_lab.py
"""

from mininet.topo import Topo
from mininet.node import Node
from mininet.link import TCLink


class LinuxRouter(Node):
    """Linux host configured to forward IPv4 packets."""

    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


class RoutingLabTopo(Topo):
    """Two-path routing topology used in ÜB8."""

    def build(self):
        client1 = self.addHost("client1")
        client2 = self.addHost("client2")
        r1 = self.addHost("r1", cls=LinuxRouter)
        r2 = self.addHost("r2", cls=LinuxRouter)
        r3 = self.addHost("r3", cls=LinuxRouter)
        server = self.addHost("server")

        self.addLink(
            client1, r1,
            intfName1="client1-eth0",
            intfName2="r1-eth0",
            cls=TCLink, delay="5ms"
        )

        self.addLink(
            client2, r1,
            intfName1="client2-eth0",
            intfName2="r1-eth0b",
            cls=TCLink, delay="5ms"
        )

        self.addLink(
            r1, r2,
            intfName1="r1-eth1",
            intfName2="r2-eth0",
            cls=TCLink, delay="5ms"
        )

        self.addLink(
            r1, r3,
            intfName1="r1-eth2",
            intfName2="r3-eth0",
            cls=TCLink, delay="30ms"
        )

        self.addLink(
            r2, server,
            intfName1="r2-eth1",
            intfName2="server-eth0",
            cls=TCLink, delay="5ms"
        )

        self.addLink(
            r3, server,
            intfName1="r3-eth1",
            intfName2="server-eth1",
            cls=TCLink, delay="30ms"
        )


topos = {"routinglab": RoutingLabTopo}
