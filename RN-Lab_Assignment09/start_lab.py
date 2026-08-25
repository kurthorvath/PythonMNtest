from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import EthernetLabTopo

def main():
    net=Mininet(topo=EthernetLabTopo(),controller=None,autoSetMacs=True)
    net.start()
    info("*** ÜB9: Ethernet, ARP and switching\n")
    for h in net.hosts:
        info(f"*** {h.name}: IP={h.IP()} MAC={h.MAC()}\n")
        makeTerm(h,title=f"ÜB9 {h.name}")
    try: input("Press ENTER to stop...")
    except KeyboardInterrupt: pass
    finally: net.stop()

if __name__=="__main__":
    setLogLevel("info"); main()
