#!/usr/bin/env python3
"""Install dependencies for Placeholder Image API"""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "uvicorn[standard]"],
    capture_output=True, text=True, timeout=120
)
print("STDOUT:", result.stdout[-1000:])
print("STDERR:", result.stderr[-1000:])
print("Return code:", result.returncode)