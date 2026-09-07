#!/usr/bin/env python3
"""RN-Lab topology for Assignment 09.

Infrastructure only:
- topology and link characteristics are defined here
- IP addresses are configured by start_lab.py
"""

from mininet.topo import Topo
from mininet.link import TCLink


class EthernetLabTopo(Topo):
    """Single Ethernet LAN with four hosts and one switch."""

    def build(self):
        client1 = self.addHost("client1")
        client2 = self.addHost("client2")
        server1 = self.addHost("server1")
        server2 = self.addHost("server2")

        switch = self.addSwitch("s1")

        for host in (client1, client2, server1, server2):
            self.addLink(host, switch, cls=TCLink, delay="1ms")


topos = {"ethernetlab": EthernetLabTopo}
