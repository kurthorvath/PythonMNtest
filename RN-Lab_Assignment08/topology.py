#!/usr/bin/env python3
"""
RN-Lab ÜB8 initial topology.

IMPORTANT:
This file deliberately contains only the topology supplied for Ü8.1.
Students extend topology.py themselves in Ü8.2 by adding r3 and the
alternative path.

IP addresses and routing are configured by start_lab.py.
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
    """
    Initial topology for Ü8.1:

        client1 \
                  s1 ---- r1 ---- r2 ---- server
        client2 /

    client1 and client2 are on the same left LAN.
    """

    def build(self):
        client1 = self.addHost("client1")
        client2 = self.addHost("client2")
        r1 = self.addHost("r1", cls=LinuxRouter)
        r2 = self.addHost("r2", cls=LinuxRouter)
        server = self.addHost("server")

        # Left LAN: client1, client2 and r1 share 10.0.1.0/24.
        s1 = self.addSwitch("s1")

        self.addLink(
            client1, s1,
            intfName1="client1-eth0",
            cls=TCLink
        )
        self.addLink(
            client2, s1,
            intfName1="client2-eth0",
            cls=TCLink
        )
        self.addLink(
            s1, r1,
            intfName2="r1-eth0",
            cls=TCLink
        )

        # R1 -- R2 point-to-point network.
        self.addLink(
            r1, r2,
            intfName1="r1-eth1",
            intfName2="r2-eth0",
            cls=TCLink
        )

        # R2 -- server network.
        self.addLink(
            r2, server,
            intfName1="r2-eth1",
            intfName2="server-eth0",
            cls=TCLink
        )


topos = {"routinglab": RoutingLabTopo}
