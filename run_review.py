# -*- coding: utf-8 -*-
import subprocess
import sys

result = subprocess.run(
    [sys.executable, r"C:\Users\Administrator\.openclaw\workspace\fund_challenge\scripts\review_summary_script.py"],
    capture_output=True
)

print("STDOUT:", result.stdout.decode('utf-8', errors='replace'))
print("STDERR:", result.stderr.decode('utf-8', errors='replace'))
print("RC:", result.returncode)
