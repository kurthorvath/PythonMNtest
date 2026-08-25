from mininet.topo import Topo
from mininet.node import Node
from mininet.link import TCLink

class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")
    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()

class RoutingLabTopo(Topo):
    def build(self):
        c = self.addHost("client1")
        c2 = self.addHost("client2")
        r1 = self.addHost("r1", cls=LinuxRouter)
        r2 = self.addHost("r2", cls=LinuxRouter)
        r3 = self.addHost("r3", cls=LinuxRouter)
        s = self.addHost("server")

        self.addLink(c, r1, intfName1="client1-eth0", intfName2="r1-eth0",
                     params1={"ip":"10.0.1.2/24"}, params2={"ip":"10.0.1.1/24"}, cls=TCLink, delay="5ms")
        self.addLink(c2, r1, intfName1="client2-eth0", intfName2="r1-eth0b",
                     params1={"ip":"10.0.1.3/24"}, params2={"ip":"10.0.1.4/24"}, cls=TCLink, delay="5ms")
        self.addLink(r1, r2, intfName1="r1-eth1", intfName2="r2-eth0",
                     params1={"ip":"10.0.12.1/30"}, params2={"ip":"10.0.12.2/30"}, cls=TCLink, delay="5ms")
        self.addLink(r1, r3, intfName1="r1-eth2", intfName2="r3-eth0",
                     params1={"ip":"10.0.13.1/30"}, params2={"ip":"10.0.13.2/30"}, cls=TCLink, delay="30ms")
        self.addLink(r2, s, intfName1="r2-eth1", intfName2="server-eth0",
                     params1={"ip":"10.0.2.1/24"}, params2={"ip":"10.0.2.2/24"}, cls=TCLink, delay="5ms")
        self.addLink(r3, s, intfName1="r3-eth1", intfName2="server-eth1",
                     params1={"ip":"10.0.3.1/24"}, params2={"ip":"10.0.3.2/24"}, cls=TCLink, delay="30ms")

topos={"routinglab":RoutingLabTopo}
