#!/usr/bin/env python3
import sys
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from topology import ForensicsTopo

def configure_network(net):
    c1, c2, r, s = [net[x] for x in ("client1", "client2", "router", "server")]

    for host, intf, addr in [
        (c1, "client1-eth0", "10.10.1.10/24"),
        (c2, "client2-eth0", "10.10.1.11/24"),
        (r, "router-eth0", "10.10.1.1/24"),
        (r, "router-eth1", "10.10.2.1/24"),
        (s, "server-eth0", "10.10.2.10/24"),
    ]:
        host.cmd(f"ip addr flush dev {intf}")
        host.cmd(f"ip addr add {addr} dev {intf}")
        host.cmd(f"ip link set dev {intf} up")

    c1.cmd("ip route replace default via 10.10.1.1 dev client1-eth0")
    c2.cmd("ip route replace default via 10.10.1.1 dev client2-eth0")
    r.cmd("sysctl -w net.ipv4.ip_forward=1")

    # INTENTIONAL FORENSIC FAULT: students must discover and repair this.
    s.cmd("ip route replace default via 10.10.2.254 dev server-eth0")

def print_state(net):
    info("\n" + "=" * 72 + "\n")
    info("*** ÜB10 forensic baseline – actual configuration\n")
    info("=" * 72 + "\n")
    for host in net.hosts:
        info(f"\n--- {host.name} ---\n")
        info(host.cmd("ip -br addr"))
        info(host.cmd("ip route"))
        info("\n")

def ping_ok(node, destination):
    # Portable check: do NOT use Host.lastCmdWasOK().
    output = node.cmd(f"ping -c 1 -W 1 {destination}; echo __RN_RC__$?")
    for line in output.splitlines():
        if line.startswith("__RN_RC__"):
            try:
                return int(line[len("__RN_RC__"):]) == 0
            except ValueError:
                return False
    return False

def verify_baseline(net):
    info("*** Verifying the forensic baseline...\n")

    tests = [
        ("client1", "10.10.1.1", "client1 -> router"),
        ("client2", "10.10.1.1", "client2 -> router"),
        ("router", "10.10.2.10", "router -> server"),
    ]

    failures = 0
    for host_name, destination, description in tests:
        ok = ping_ok(net[host_name], destination)
        info(f"  [{'OK' if ok else 'FAILED'}] {description}\n")
        if not ok:
            failures += 1

    if failures:
        info(f"\n*** ERROR: {failures} baseline infrastructure test(s) failed.\n")
        info("*** Terminals will not be opened.\n")
        return False

    info("\n*** Checking intentional forensic symptom...\n")

    c1_ok = ping_ok(net["client1"], "10.10.2.10")
    s_ok = ping_ok(net["server"], "10.10.1.10")

    info(f"  [{'UNEXPECTED SUCCESS' if c1_ok else 'EXPECTED FAILURE'}] "
         "client1 -> server\n")
    info(f"  [{'UNEXPECTED SUCCESS' if s_ok else 'EXPECTED FAILURE'}] "
         "server -> client1\n")

    info("\n*** Baseline accepted. The communication failure is intentional.\n")
    return True

def main():
    net = Mininet(topo=ForensicsTopo(), controller=None, autoSetMacs=True)
    try:
        info("*** Starting ÜB10 Network Forensics environment...\n")
        net.start()
        configure_network(net)
        print_state(net)

        if not verify_baseline(net):
            return 1

        info("\n*** Opening ÜB10 terminals...\n")
        for host, title in [
            (net["client1"], "ÜB10 client1"),
            (net["client2"], "ÜB10 client2"),
            (net["router"], "ÜB10 router"),
            (net["server"], "ÜB10 server"),
        ]:
            makeTerm(host, title=title)

        try:
            input("\nPress ENTER to stop the Mininet environment...")
        except KeyboardInterrupt:
            pass
        return 0
    finally:
        net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    sys.exit(main())
