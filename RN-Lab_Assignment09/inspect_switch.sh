#!/bin/bash

echo "=== Mininet switch information ==="
ovs-ofctl show s1 2>/dev/null || true

echo
echo "=== Forwarding database ==="
ovs-appctl fdb/show s1 2>/dev/null || true

echo
echo "If the commands above are unavailable, inspect the switch using:"
echo "    sh ovs-ofctl dump-flows s1"
