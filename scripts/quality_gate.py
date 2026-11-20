
import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

command = [
    sys.executable,
    "-m",
    "pytest",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml:reports/coverage.xml",
    "--cov-report=json:reports/coverage.json",
]

print("Starting Quality Gate...")

result = subprocess.run(command, cwd=ROOT_DIR)

if result.returncode != 0:
    print("CRITICAL FAILURE: Unit tests failed.")
    sys.exit(1)

coverage_file = REPORTS_DIR / "coverage.json"

with coverage_file.open(encoding="utf-8") as file:
    coverage_data = json.load(file)

coverage = coverage_data["totals"]["percent_covered"]

print(f"\nCode coverage: {coverage:.2f}%")

if coverage < 70:
    print("CRITICAL FAILURE: Coverage is below 70%.")
    sys.exit(1)

elif coverage < 80:
    print("WARNING: Coverage is between 70% and 80%.")
    print("Pipeline can continue, but coverage should be improved.")

else:
    print("QUALITY GATE PASSED: Coverage is at least 80%.")

print("\nQUALITY GATE COMPLETED.")
