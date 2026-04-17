#!/bin/bash
set -e
cd /home/lizhuojun/hermes-agent-main

export https_proxy=""
export http_proxy=""
unset https_proxy http_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy

echo "=== Testing direct connectivity ==="
timeout 5 curl -I https://pypi.org/simple 2>&1 | head -3 || echo "Direct PyPI blocked"

echo "=== Testing via GitHub proxy ==="
timeout 5 curl -I --proxy http://172.23.16.1:7890 https://github.com 2>&1 | head -3 || echo "Proxy also blocked"

echo "=== Checking WSL name resolution ==="
cat /etc/resolv.conf
