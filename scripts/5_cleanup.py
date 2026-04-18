import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path.home() / "pwnagotchi"

GOOD = BASE / "data/good_pcaps"
BAD = BASE / "data/bad_pcaps"
HASHES = BASE / "data/hashes"

DB = BASE / "db/networks.db"

BAD_RETENTION_DAYS = 7

conn = sqlite3.connect(DB)
cur = conn.cursor()

print("Starting cleanup...")

# удалить старые плохие pcaps
limit = datetime.now() - timedelta(days=BAD_RETENTION_DAYS)

for pcap in BAD.glob("*.pcap"):

    mtime = datetime.fromtimestamp(pcap.stat().st_mtime)

    if mtime < limit:
        print("Removing old bad capture:", pcap.name)
        pcap.unlink()

# удалить файлы если пароль найден
cur.execute("""
SELECT filename FROM captures
WHERE password IS NOT NULL
""")

rows = cur.fetchall()

for row in rows:

    filename = row[0]

    pcap_file = GOOD / filename
    hash_file = HASHES / (Path(filename).stem + ".22000")

    if pcap_file.exists():
        print("Removing cracked pcap:", filename)
        pcap_file.unlink()

    if hash_file.exists():
        print("Removing cracked hash:", hash_file.name)
        hash_file.unlink()

conn.close()

print("Cleanup complete")

