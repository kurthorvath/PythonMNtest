#!/usr/bin/env python3
"""RN-Lab topology for Assignment 10.

The topology is intentionally simple. The forensic fault is configured
at runtime in start_lab.py, not in the topology definition.
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


class ForensicsTopo(Topo):
    def build(self):
        client1 = self.addHost("client1")
        client2 = self.addHost("client2")
        server = self.addHost("server")
        router = self.addHost("router", cls=LinuxRouter)

        sw1 = self.addSwitch("sw1")
        sw2 = self.addSwitch("sw2")

        # Client LAN
        self.addLink(
            client1, sw1,
            intfName1="client1-eth0",
            cls=TCLink,
            delay="2ms"
        )
        self.addLink(
            client2, sw1,
            intfName1="client2-eth0",
            cls=TCLink,
            delay="2ms"
        )
        self.addLink(
            sw1, router,
            intfName2="router-eth0",
            cls=TCLink,
            delay="5ms"
        )

        # Router/server LAN
        self.addLink(
            router, sw2,
            intfName1="router-eth1",
            cls=TCLink,
            delay="5ms"
        )
        self.addLink(
            server, sw2,
            intfName1="server-eth0",
            cls=TCLink,
            delay="2ms"
        )


topos = {"forensics": ForensicsTopo}
