import subprocess
from pathlib import Path

from config import ensure_config

cfg = ensure_config()

REMOTE_HOST = cfg["remote_host"]
REMOTE_USER = cfg["remote_user"]
REMOTE_DIR = cfg["remote_dir"]
SSH_PORT = cfg["ssh_port"]
SSH_KEY = cfg["ssh_key"]

LOCAL_DIR = Path.home() / "pwnagotchi/data/incoming"
LOCAL_DIR.mkdir(parents=True, exist_ok=True)

ssh_cmd = ["ssh", "-p", str(SSH_PORT)]
if SSH_KEY:
    ssh_cmd.extend(["-i", SSH_KEY])

print("Syncing pcaps from pwnagotchi...")

cmd = [
    "rsync",
    "-avz",
    "--remove-source-files",
    "-e",
    " ".join(ssh_cmd),
    f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_DIR}/*.pcap",
    str(LOCAL_DIR),
]

result = subprocess.run(cmd)

if result.returncode == 0:
    print("Transfer complete")
else:
    print("Transfer failed")
