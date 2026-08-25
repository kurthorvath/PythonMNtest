
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

class ForensicsTopo(Topo):
    def build(self):
        c1 = self.addHost("client1")
        c2 = self.addHost("client2")
        s = self.addHost("server")
        r = self.addHost("router", cls=LinuxRouter)
        sw1 = self.addSwitch("sw1")
        sw2 = self.addSwitch("sw2")

        self.addLink(c1, sw1, cls=TCLink, delay="2ms")
        self.addLink(c2, sw1, cls=TCLink, delay="2ms")
        self.addLink(sw1, r, cls=TCLink, delay="5ms")
        self.addLink(r, sw2, cls=TCLink, delay="5ms")
        self.addLink(s, sw2, cls=TCLink, delay="2ms")

topos = {"forensics": ForensicsTopo}
