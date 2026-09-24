"""Run course release, link and integrity checks."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable,'-m','unittest','discover','-s',str(root/'tests'),'-v']))
