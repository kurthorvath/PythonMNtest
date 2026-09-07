# ÜB4 instructor verification

Run inside the RN-Lab VM:

```bash
sudo python3 check_environment.py
sudo python3 start_lab.py
```

Expected:
- three xterm windows open
- client has 10.0.1.2/24
- router has 10.0.1.1/24 and 10.0.2.1/24
- server has 10.0.2.2/24
- client can ping router and server
- server can ping router and client
- UDP client/server communicate through the router

In the client terminal:

```bash
ip addr
ip route
ping -c 4 10.0.2.2
python3 udp_client.py
```

In the server terminal:

```bash
ip addr
ip route
ping -c 4 10.0.1.2
python3 udp_server.py
```

The expected end-to-end path is:

client -> client-eth0 -> router-eth0 -> router-eth1 -> server-eth0

and in the reverse direction:

server -> server-eth0 -> router-eth1 -> router-eth0 -> client-eth0
