#!/usr/bin/env python3
"""RN-Lab topology for ÜB9.

Infrastructure only:
- four hosts
- one Ethernet switch
- no router
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

        s1 = self.addSwitch("s1")

        self.addLink(client1, s1, intfName1="client1-eth0", cls=TCLink)
        self.addLink(client2, s1, intfName1="client2-eth0", cls=TCLink)
        self.addLink(server1, s1, intfName1="server1-eth0", cls=TCLink)
        self.addLink(server2, s1, intfName1="server2-eth0", cls=TCLink)


topos = {"ethernetlab": EthernetLabTopo}
