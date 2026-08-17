#!/usr/bin/env python3
"""
Assignment 05 topology.

Students may change LINK_DELAY and LINK_LOSS for experiments.
Do not change the topology structure unless explicitly requested.
"""

from mininet.topo import Topo
from mininet.node import Node
from mininet.link import TCLink

LINK_DELAY = "20ms"
LINK_LOSS = 0


class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


class TCPTopo(Topo):
    def build(self):
        client = self.addHost("client")
        router = self.addHost("router", cls=LinuxRouter)
        server = self.addHost("server")

        self.addLink(
            client, router,
            intfName1="client-eth0",
            intfName2="router-eth0",
            params1={"ip": "10.0.1.2/24"},
            params2={"ip": "10.0.1.1/24"},
            cls=TCLink,
            delay=LINK_DELAY,
            loss=LINK_LOSS
        )

        self.addLink(
            router, server,
            intfName1="router-eth1",
            intfName2="server-eth0",
            params1={"ip": "10.0.2.1/24"},
            params2={"ip": "10.0.2.2/24"},
            cls=TCLink,
            delay=LINK_DELAY,
            loss=LINK_LOSS
        )


topos = {"tcptopo": TCPTopo}
