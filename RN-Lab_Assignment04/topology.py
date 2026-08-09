#!/usr/bin/env python3
"""RN-Lab topology for Assignment 04. Infrastructure provided by the course."""

from mininet.topo import Topo
from mininet.link import TCLink

LINK_DELAY = "20ms"
LINK_LOSS = 0


class RNLabTopo(Topo):
    """client -- Linux router -- server"""

    def build(self):
        client = self.addHost("client")
        router = self.addHost("router")
        server = self.addHost("server")

        self.addLink(
            client, router,
            intfName1="client-eth0",
            intfName2="router-eth0",
            params1={"ip": "10.0.1.2/24"},
            params2={"ip": "10.0.1.1/24"},
            cls=TCLink, delay=LINK_DELAY, loss=LINK_LOSS)

        self.addLink(
            router, server,
            intfName1="router-eth1",
            intfName2="server-eth0",
            params1={"ip": "10.0.2.1/24"},
            params2={"ip": "10.0.2.2/24"},
            cls=TCLink, delay=LINK_DELAY, loss=LINK_LOSS)


topos = {"rnlab": RNLabTopo}
