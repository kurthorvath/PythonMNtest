from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import RoutingLabTopo

def main():
    net=Mininet(topo=RoutingLabTopo(),controller=None,autoSetMacs=True)
    net.start()
    c,c2,r1,r2,r3,s=[net[x] for x in ("client1","client2","r1","r2","r3","server")]

    c.cmd("ip route replace default via 10.0.1.1")
    c2.cmd("ip route replace default via 10.0.1.4")
    r1.cmd("ip route replace 10.0.2.0/24 via 10.0.12.2")
    r1.cmd("ip route replace 10.0.3.0/24 via 10.0.13.2")
    r2.cmd("ip route replace 10.0.1.0/24 via 10.0.12.1")
    r2.cmd("ip route replace 10.0.3.0/24 via 10.0.12.1")
    r3.cmd("ip route replace 10.0.1.0/24 via 10.0.13.1")
    r3.cmd("ip route replace 10.0.2.0/24 via 10.0.13.1")
    s.cmd("ip route add 10.0.1.0/24 via 10.0.2.1")
    s.cmd("ip route add 10.0.3.0/24 via 10.0.3.1")

    info("*** ÜB8: routing/topology/Wireshark\n")
    for h,t in [(c,"ÜB8 Client"),(r1,"ÜB8 R1"),(r2,"ÜB8 R2"),(r3,"ÜB8 R3"),(s,"ÜB8 Server")]:
        makeTerm(h,title=t)
    try: input("Press ENTER to stop...")
    except KeyboardInterrupt: pass
    finally: net.stop()

if __name__=="__main__":
    setLogLevel("info"); main()
