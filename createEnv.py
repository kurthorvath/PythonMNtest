#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.term import makeTerm


class LinuxRouter(Node):
    """A Linux host acting as an IP router."""

    def config(self, **params):
        super().config(**params)
        # Enable IPv4 forwarding
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


def run():

    net = Mininet(link=TCLink)

    print("*** Creating nodes")

    h1 = net.addHost("h1", ip="10.0.1.2/24")
    r1 = net.addHost("r1", cls=LinuxRouter)
    h2 = net.addHost("h2", ip="10.0.2.2/24")

    print("*** Creating links")

    net.addLink(
        h1,
        r1,
        intfName2="r1-eth0",
        params2={"ip": "10.0.1.1/24"},
        delay="30ms",
        loss=10,
    )

    net.addLink(
        r1,
        h2,
        intfName1="r1-eth1",
        params1={"ip": "10.0.2.1/24"},
        delay="30ms",
        loss=10,
    )

    print("*** Starting network")

    net.start()

    print("*** Configuring routing")

    h1.cmd("ip route add default via 10.0.1.1")
    h2.cmd("ip route add default via 10.0.2.1")

    print("*** Opening terminals")

    makeTerm(h1, title="Client (h1)")
    makeTerm(h2, title="Server (h2)")
    makeTerm(r1, title="Router (r1)")

    print()
    print("Topology ready")
    print("------------------------------")
    print("Client : 10.0.1.2")
    print("Router : 10.0.1.1 / 10.0.2.1")
    print("Server : 10.0.2.2")
    print()
    print("Example:")
    print("Server terminal:")
    print("    python3 server.py")
    print()
    print("Client terminal:")
    print("    python3 client.py")
    print()

    input("Press ENTER to stop the lab...")

    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
