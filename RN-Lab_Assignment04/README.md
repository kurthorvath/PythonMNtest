# RN-Lab – Assignment 04

This package contains the complete starting environment for ÜB4.

The important design principle is:

> **Infrastructure and application code are separate.**

`topology.py` and `start_lab.py` create the network. The Python UDP programs are applications that run inside the already-created Mininet hosts.

## 1. Check the VM

Run:

```bash
python3 check_environment.py
```

The check should report Python, Mininet, `mn`, `xterm`, `ovs-vsctl` and `tc`.

## 2. A first Mininet example

Before using the RN-Lab topology:

```bash
sudo python3 standard_mininet.py
```

This creates:

```text
h1 -------- s1 -------- h2
```

In the terminal, try:

```bash
h1 ip addr
h2 ip addr
h1 ping -c 4 h2
```

This is a useful first demonstration that commands such as `ip addr` and `ping` are executed inside the corresponding Mininet host namespace.

## 3. Start the RN-Lab

Run:

```bash
sudo python3 start_lab.py
```

The script creates:

```text
10.0.1.2/24        10.0.1.1/24       10.0.2.1/24        10.0.2.2/24
   client  ---------------- router ---------------- server
                 20 ms                         20 ms
```

There are **three separate terminals**:

- RN-Lab Client
- RN-Lab Router
- RN-Lab Server

The startup script explicitly configures the addresses and routes and then verifies connectivity before opening the terminals.

## 4. Check the hosts

In the client terminal:

```bash
ip addr
ip route
```

You should see:

```text
10.0.1.2/24
default via 10.0.1.1
```

In the router terminal:

```bash
ip addr
ip route
```

You should see:

```text
10.0.1.1/24
10.0.2.1/24
```

In the server terminal:

```bash
ip addr
ip route
```

You should see:

```text
10.0.2.2/24
default via 10.0.2.1
```

`ifconfig` also works if installed:

```bash
ifconfig
```

## 5. Ping between the terminals

Yes: the terminals are actual Mininet network namespaces, so you can use `ping` exactly as you would on separate machines.

From the client:

```bash
ping -c 4 10.0.1.1
ping -c 4 10.0.2.2
```

The first ping reaches the router directly. The second crosses the router.

From the server:

```bash
ping -c 4 10.0.2.1
ping -c 4 10.0.1.2
```

The second ping crosses the router in the opposite direction.

The startup script performs these checks automatically.

## 6. Run the UDP example

In the **server** terminal:

```bash
python3 udp_server.py
```

In the **client** terminal:

```bash
python3 udp_client.py
```

The default destination is:

```text
10.0.2.2:5000
```

You can also specify the destination explicitly:

```bash
python3 udp_client.py 10.0.2.2 5000 "Hello server"
```

The server accepts the same parameters:

```bash
python3 udp_server.py 10.0.2.2 5000
```

The client should receive an acknowledgement from the server.

## 7. Important

Do not modify `topology.py` unless the exercise explicitly asks you to do so.

The infrastructure is deliberately provided separately from the application programs. This separation is important for the rest of the RN-Lab.

## 8. Stopping the lab

Return to the terminal in which `start_lab.py` is running and press ENTER.

If Mininet is left behind after an experiment, run:

```bash
sudo mn -c
```

Use `mn -c` only when necessary to clean up stale Mininet state.
