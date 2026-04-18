import subprocess
from pathlib import Path

BASE = Path.home() / "pwnagotchi"

GOOD = BASE / "data/good_pcaps"
HASHES = BASE / "data/hashes"

HASHES.mkdir(parents=True, exist_ok=True)

print("Starting conversion...")

for pcap in GOOD.glob("*.pcap"):

    hashfile = HASHES / (pcap.stem + ".22000")

    if hashfile.exists() and hashfile.stat().st_size > 0:
        print("Skipping (already converted):", pcap.name)
        continue

    print("Converting:", pcap.name)

    subprocess.run([
        "hcxpcapngtool",
        "-o",
        str(hashfile),
        str(pcap)
    ])

    if hashfile.exists() and hashfile.stat().st_size > 0:
        print("Hash created:", hashfile.name)
    else:
        print("No hash extracted from:", pcap.name)
        if hashfile.exists():
            hashfile.unlink()

print("Conversion complete")

