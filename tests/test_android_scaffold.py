from pathlib import Path
import json
def test_capacitor_scaffold():
 p=Path("mobile/capacitor/package.json");assert p.exists()
 data=json.loads(p.read_text());assert "sync" in data["scripts"]
def test_capacitor_config():
 assert Path("mobile/capacitor/capacitor.config.ts").exists()
