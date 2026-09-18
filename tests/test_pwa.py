from pathlib import Path
def test_pwa_assets_exist():
 assert Path("frontend/public/manifest.webmanifest").exists()
 assert Path("frontend/public/sw.js").exists()
def test_offline_store():
 from frontend.src.stores.offline import loadMessages
 assert callable(loadMessages)
