$ErrorActionPreference = 'Stop'

# Disable proxy only for this process scope
$env:HTTP_PROXY = ''
$env:HTTPS_PROXY = ''
$env:ALL_PROXY = ''
$env:http_proxy = ''
$env:https_proxy = ''
$env:all_proxy = ''

python fund_challenge/scripts/universe_refresh_script_only.py
