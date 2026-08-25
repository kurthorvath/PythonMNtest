
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import ForensicsTopo, LinuxRouter

def main():
    net = Mininet(topo=ForensicsTopo(), controller=None, autoSetMacs=True)
    net.start()

    c1, c2, r, s = [net[x] for x in ("client1", "client2", "router", "server")]

    # Addressing
    c1.setIP("10.10.1.10/24")
    c2.setIP("10.10.1.11/24")
    r.setIP("10.10.1.1/24", intf="router-eth0")
    r.setIP("10.10.2.1/24", intf="router-eth1")
    s.setIP("10.10.2.10/24")

    # Normal host configuration.
    c1.cmd("ip route replace default via 10.10.1.1")
    c2.cmd("ip route replace default via 10.10.1.1")
    s.cmd("ip route replace default via 10.10.2.1")

    # INTENTIONAL FORENSIC FAULT:
    # The server has the wrong default gateway. Students should discover
    # this from evidence rather than being told the cause.
    s.cmd("ip route replace default via 10.10.2.254")

    info("\n*** ÜB10 Network Forensics\n")
    info("*** Expected: client1/client2 should reach server over TCP.\n")
    info("*** The environment contains an intentional configuration fault.\n\n")

    for h, title in [(c1, "ÜB10 client1"), (c2, "ÜB10 client2"),
                     (r, "ÜB10 router"), (s, "ÜB10 server")]:
        makeTerm(h, title=title)

    try:
        input("Press ENTER to stop the Mininet environment...")
    except KeyboardInterrupt:
        pass
    finally:
        net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    main()
