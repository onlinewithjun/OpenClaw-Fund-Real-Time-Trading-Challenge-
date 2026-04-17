@echo off
set no_proxy=*
python -u fund_challenge\scripts\update_refresh_retry.py --mode retry
