from mininet.topo import Topo
from mininet.link import TCLink

class EthernetLabTopo(Topo):
    def build(self):
        c1=self.addHost("client1", ip="10.0.1.2/24")
        c2=self.addHost("client2", ip="10.0.1.3/24")
        s1=self.addHost("server1", ip="10.0.1.10/24")
        s2=self.addHost("server2", ip="10.0.1.11/24")
        sw=self.addSwitch("s1")

        for h in (c1,c2,s1,s2):
            self.addLink(h,sw,cls=TCLink,delay="1ms")

topos={"ethernetlab":EthernetLabTopo}
