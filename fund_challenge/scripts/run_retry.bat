@echo off
set NO_PROXY=*
set no_proxy=*
python fund_challenge\scripts\update_refresh_retry.py --mode retry
