cd C:\Users\Administrator\.openclaw\workspace
$env:NO_PROXY = "*"
python fund_challenge/scripts/maintenance_cleanup.py 2>&1
