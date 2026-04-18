import subprocess
import sqlite3
import shutil
from pathlib import Path

BASE = Path.home() / "pwnagotchi"

INCOMING = BASE / "data/incoming"
GOOD = BASE / "data/good_pcaps"
BAD = BASE / "data/bad_pcaps"
HASHES = BASE / "data/hashes"

DB = BASE / "db/networks.db"

GOOD.mkdir(parents=True, exist_ok=True)
BAD.mkdir(parents=True, exist_ok=True)
HASHES.mkdir(parents=True, exist_ok=True)

DB.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS captures(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT UNIQUE,
    bssid TEXT,
    ssid TEXT,
    password TEXT,
    handshake INTEGER,
    pmkid INTEGER,
    hashfile TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

for pcap in INCOMING.glob("*.pcap"):

    print(f"Analyzing {pcap.name}")

    result = subprocess.run(
        [
            "hcxpcapngtool",
            str(pcap)
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout.lower()

    handshake = "eapol" in output
    pmkid = "pmkid" in output

    if handshake or pmkid:
        print("  usable capture found")
        shutil.move(pcap, GOOD / pcap.name)
    else:
        print("  no authentication material")
        shutil.move(pcap, BAD / pcap.name)

    c.execute(
        "INSERT OR IGNORE INTO captures(filename, handshake, pmkid) VALUES(?,?,?)",
        (pcap.name, int(handshake), int(pmkid))
    )

conn.commit()
conn.close()

