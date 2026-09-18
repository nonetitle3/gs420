#!/usr/bin/env python3
"""Run the complete repository pytest suite in one command."""
import subprocess,sys
raise SystemExit(subprocess.call([sys.executable,"-m","pytest","-q","tests"]))
