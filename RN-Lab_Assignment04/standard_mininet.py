#!/usr/bin/env python3
"""Introductory h1 -- s1 -- h2 Mininet topology."""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.log import setLogLevel


def main():
    net = Mininet(switch=OVSSwitch)
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")
    s1 = net.addSwitch("s1")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.start()

    print("\nTopology: h1 -------- s1 -------- h2\n")
    try:
        input("Press ENTER to stop the topology...")
    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
