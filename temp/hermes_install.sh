#!/bin/bash
# Clear proxy variables
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy

# Clear git global proxy
git config --global --unset http.proxy 2>/dev/null
git config --global --unset https.proxy 2>/dev/null

echo "=== Proxy cleared ==="
echo "http_proxy=$http_proxy"
echo "https_proxy=$https_proxy"

# Download zip
echo "=== Downloading hermes-agent zip ==="
curl -L https://github.com/NousResearch/hermes-agent/archive/refs/heads/main.zip -o /tmp/hermes-agent.zip
if [ $? -eq 0 ]; then
    echo "=== Download OK ==="
    ls -la /tmp/hermes-agent.zip
    echo "=== Extracting ==="
    unzip -o /tmp/hermes-agent.zip -d /tmp/
    echo "=== Files ==="
    ls /tmp/hermes-agent-*/
else
    echo "=== Download FAILED ==="
fi
