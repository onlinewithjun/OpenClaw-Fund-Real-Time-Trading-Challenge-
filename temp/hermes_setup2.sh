#!/bin/bash
set -e
cd /home/lizhuojun/hermes-agent-main

echo "=== Checking venv ==="
if [ -d venv ]; then
    echo "venv exists"
else
    echo "Creating venv..."
    python3 -m venv venv
fi

echo "=== Upgrading pip ==="
/home/lizhuojun/hermes-agent-main/venv/bin/python -m pip install --upgrade pip 2>&1 | tail -3

echo "=== Installing requirements via proxy ==="
export https_proxy="http://172.23.16.1:7890"
export http_proxy="http://172.23.16.1:7890"

/home/lizhuojun/hermes-agent-main/venv/bin/pip install openai python-dotenv fire httpx rich tenacity prompt_toolkit pyyaml requests jinja2 "pydantic>=2.0" "PyJWT[crypto]" debugpy firecrawl-py "parallel-web>=0.4.2" fal-client edge-tts croniter "python-telegram-bot[webhooks]>=22.6" discord.py "aiohttp>=3.9.0" -i https://pypi.org/simple --trusted-host pypi.org 2>&1 | tail -5

echo "=== Done ==="
