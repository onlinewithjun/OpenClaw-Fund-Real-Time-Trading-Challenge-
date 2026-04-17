@echo off
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
python fund_challenge\scripts\update_refresh_retry.py --mode retry
