# -*- coding: utf-8 -*-
import subprocess
import sys
import io
import codecs

result = subprocess.run(
    [sys.executable, r"C:\Users\Administrator\.openclaw\workspace\fund_challenge\scripts\review_summary_script.py"],
    capture_output=True
)

out = result.stdout.decode('utf-8', errors='replace')
err = result.stderr.decode('utf-8', errors='replace')

# Write to file with utf-8
with codecs.open(r"C:\Users\Administrator\.openclaw\workspace\review_output.txt", "w", "utf-8") as f:
    f.write("=== STDOUT ===\n")
    f.write(out)
    f.write("\n=== STDERR ===\n")
    f.write(err)
    f.write(f"\n=== RC: {result.returncode} ===\n")

print("Done - output written to review_output.txt")
