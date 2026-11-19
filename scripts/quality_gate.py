
import subprocess
import sys
from pathlib import Path

# Racine du projet
ROOT_DIR = Path(__file__).resolve().parents[1]

# Exécution des tests avec contrôle de couverture
command = [
    sys.executable,
    "-m",
    "pytest",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]

print("Starting Quality Gate...")

result = subprocess.run(command, cwd=ROOT_DIR)

if result.returncode == 0:
    print("QUALITY GATE PASSED")
else:
    print("QUALITY GATE FAILED")
    sys.exit(result.returncode)
