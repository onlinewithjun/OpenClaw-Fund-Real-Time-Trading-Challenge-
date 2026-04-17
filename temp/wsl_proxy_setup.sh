#!/bin/bash

# WSL uses Windows gateway (172.23.16.1) to reach host Clash
export http_proxy="http://172.23.16.1:7890"
export https_proxy="http://172.23.16.1:7890"
export HTTP_PROXY="http://172.23.16.1:7890"
export HTTPS_PROXY="http://172.23.16.1:7890"

echo "=== Proxy set to Windows Clash ==="
echo "http_proxy=$http_proxy"
echo "https_proxy=$https_proxy"

# Test connectivity through proxy
echo "=== Testing GitHub via proxy ==="
curl -I --proxy http://172.23.16.1:7890 https://github.com 2>&1 | head -5

echo "=== Downloading hermes-agent ==="
curl -L --proxy http://172.23.16.1:7890 https://github.com/NousResearch/hermes-agent/archive/refs/heads/main.zip -o /tmp/hermes-agent.zip
if [ $? -eq 0 ]; then
    echo "=== Download SUCCESS ==="
    ls -la /tmp/hermes-agent.zip
    echo "=== Extracting ==="
    unzip -o /tmp/hermes-agent.zip -d /tmp/
    echo "=== Done ==="
else
    echo "=== Download FAILED ==="
fi
