#!/usr/bin/env python3
"""Start the RN-Lab environment for Assignment 04."""

from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

from topology import RNLabTopo, LINK_DELAY, LINK_LOSS


class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


def main():
    net = Mininet(topo=RNLabTopo(), controller=None, autoSetMacs=True)

    # The node is a normal Linux host configured to forward IPv4 packets.
    net["router"].__class__ = LinuxRouter

    info("*** Starting RN-Lab\n")
    net.start()

    client = net["client"]
    router = net["router"]
    server = net["server"]

    client.cmd("ip route replace default via 10.0.1.1")
    server.cmd("ip route replace default via 10.0.2.1")

    print("\n" + "=" * 60)
    print("RN-Lab - Assignment 04")
    print("=" * 60)
    print("client  : 10.0.1.2/24")
    print("router  : 10.0.1.1/24, 10.0.2.1/24")
    print("server  : 10.0.2.2/24")
    print(f"delay   : {LINK_DELAY}")
    print(f"loss    : {LINK_LOSS}%")
    print("\nHost PIDs:")
    for host in net.hosts:
        print(f"  {host.name:8s} PID={host.pid}")
    print("=" * 60 + "\n")

    # Separate consoles for client/server experiments and router diagnostics.
    makeTerm(client, title="RN-Lab Client")
    makeTerm(server, title="RN-Lab Server")
    makeTerm(router, title="RN-Lab Router")

    try:
        input("Press ENTER to stop RN-Lab...")
    except KeyboardInterrupt:
        pass
    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
