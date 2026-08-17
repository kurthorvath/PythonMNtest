#!/usr/bin/env python3
"""Start the Assignment 06 multi-router Mininet environment."""

from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import RoutingTopo

def main():
    net = Mininet(topo=RoutingTopo(), controller=None, autoSetMacs=True)
    net.start()

    client = net["client"]
    r1 = net["r1"]
    r2 = net["r2"]
    server = net["server"]

    client.cmd("ip route replace default via 10.0.1.1")
    r1.cmd("ip route replace 10.0.2.0/24 via 10.0.12.2")
    r2.cmd("ip route replace 10.0.1.0/24 via 10.0.12.1")
    server.cmd("ip route replace default via 10.0.2.1")

    info("\n*** RN-Lab Assignment 06\n")
    info("*** client -- r1 -- r2 -- server\n\n")

    for host in net.hosts:
        info(f"*** {host.name}: {host.IP()} {host.MAC()}\n")

    for host, title in [
        (client, "A06 Client"),
        (r1, "A06 Router 1"),
        (r2, "A06 Router 2"),
        (server, "A06 Server"),
    ]:
        makeTerm(host, title=title)

    try:
        input("\nPress ENTER to stop...")
    except KeyboardInterrupt:
        pass
    finally:
        net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    main()
