#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import TCPTopo, LINK_DELAY, LINK_LOSS

def main():
    net = Mininet(topo=TCPTopo(), controller=None, autoSetMacs=True)
    net.start()

    client = net["client"]
    router = net["router"]
    server = net["server"]

    client.cmd("ip route replace default via 10.0.1.1")
    server.cmd("ip route replace default via 10.0.2.1")

    info("\n*** RN-Lab Assignment 05\n")
    info(f"*** Link delay: {LINK_DELAY}\n")
    info(f"*** Link loss : {LINK_LOSS}%\n\n")

    for host in net.hosts:
        info(f"*** {host.name}: {host.IP()} {host.MAC()}\n")

    makeTerm(server, title="A05 Server")
    makeTerm(client, title="A05 Client")
    makeTerm(router, title="A05 Router")

    try:
        input("\nPress ENTER to stop the experiment...")
    except KeyboardInterrupt:
        pass
    finally:
        net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    main()
