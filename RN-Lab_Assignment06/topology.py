#!/usr/bin/env python3
"""
Assignment 06 base topology.

Students modify this file beginning with Ü 6.6.
"""

from mininet.topo import Topo
from mininet.node import Node
from mininet.link import TCLink

LINK_DELAY = "10ms"


class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


class RoutingTopo(Topo):
    def build(self):
        client = self.addHost("client")
        r1 = self.addHost("r1", cls=LinuxRouter)
        r2 = self.addHost("r2", cls=LinuxRouter)
        server = self.addHost("server")

        self.addLink(
            client, r1,
            intfName1="client-eth0",
            intfName2="r1-eth0",
            params1={"ip": "10.0.1.2/24"},
            params2={"ip": "10.0.1.1/24"},
            cls=TCLink,
            delay=LINK_DELAY
        )

        self.addLink(
            r1, r2,
            intfName1="r1-eth1",
            intfName2="r2-eth0",
            params1={"ip": "10.0.12.1/30"},
            params2={"ip": "10.0.12.2/30"},
            cls=TCLink,
            delay=LINK_DELAY
        )

        self.addLink(
            r2, server,
            intfName1="r2-eth1",
            intfName2="server-eth0",
            params1={"ip": "10.0.2.1/24"},
            params2={"ip": "10.0.2.2/24"},
            cls=TCLink,
            delay=LINK_DELAY
        )


topos = {"routingtopo": RoutingTopo}
