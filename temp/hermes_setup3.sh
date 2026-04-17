#!/bin/bash
set -e
cd /home/lizhuojun/hermes-agent-main

export https_proxy="http://172.23.16.1:7890"
export http_proxy="http://172.23.16.1:7890"

echo "=== Creating venv with uv ==="
uv venv /home/lizhuojun/.hermes/hermes-agent/venv --python 3.11 2>&1

echo "=== Installing requirements ==="
uv pip install --python /home/lizhuojun/.hermes/hermes-agent/venv/bin/python \
    openai python-dotenv fire httpx rich tenacity prompt_toolkit pyyaml requests jinja2 \
    "pydantic>=2.0" "PyJWT[crypto]" debugpy firecrawl-py "parallel-web>=0.4.2" \
    fal-client edge-tts croniter "python-telegram-bot[webhooks]>=22.6" \
    discord.py "aiohttp>=3.9.0" 2>&1 | tail -10

echo "=== Setup complete ==="
