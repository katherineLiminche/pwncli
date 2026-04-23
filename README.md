# pwnycli

`pwnycli` is a command-line controller for a Pwnagotchi capture-processing pipeline. It helps you move through the full workflow of transferring captures, analyzing them, converting them to hashcat format, cracking them, and cleaning up the workspace.

## What it does

`pwnycli` can:

- transfer capture files from a remote Pwnagotchi
- analyze and sort captures
- convert captures into `22000` hash files
- run `hashcat` against collected hashes
- clean up broken or orphaned files
- check your local environment
- show pipeline status and cracking statistics
- export cracked networks
- generate a simple wordlist for common SSID-based guessing
- run the full pipeline once or in a loop

## Project layout

- `pwnycli` — installed CLI entry point
- `dpwnycli/` — Python package source
- `dpwnycli/__main__.py` — CLI implementation
- `dpwnycli/scripts/` — pipeline stage scripts
- `dpwnycli/config.py` — local transfer configuration helpers

## Requirements

- Python 3.8+
- `ssh`
- `scp`
- `hashcat`
- `hcxpcapngtool`

On macOS, the external tools can be installed with Homebrew if they are missing.

## Installation

### From the repository

```bash
git clone https://github.com/katherineLiminche/pwnycli.git
cd pwnycli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### From PyPI

```bash
pip install pwnycli
```

## Initial setup

The CLI uses a base working directory controlled by the `PWN_BASE` environment variable.

By default, the base directory is:

```bash
~/pwnagotchi
```

From there, `pwnycli` expects and creates:

- `data/incoming`
- `data/good_pcaps`
- `data/bad_pcaps`
- `data/hashes`
- `db/networks.db`

Create the directory structure and database with:

```bash
pwnycli init
```

You can override the base directory like this:

```bash
export PWN_BASE=/path/to/pwnagotchi
pwnycli init
```

## Configuration

Transfer settings are stored in:

```bash
$PWN_BASE/config.json
```

The configuration includes:

- remote host
- remote user
- remote directory
- SSH port
- SSH key path

The CLI will prompt for these values when they are needed and not already configured.

## Usage

### Full pipeline

```bash
pwnycli run
```

Run continuously:

```bash
pwnycli run --loop
```

Custom loop delay:

```bash
pwnycli run --loop --delay 300
```

### Individual stages

```bash
pwnycli transfer
pwnycli analyze
pwnycli convert
pwnycli crack
pwnycli cleanup
```

### Diagnostics and status

```bash
pwnycli doctor
pwnycli status
pwnycli stats
pwnycli watch
```

### Maintenance

```bash
pwnycli purge
pwnycli export
```

### Cracking helpers

```bash
pwnycli bench
pwnycli autopwn
```

## Command reference

`run`  
Run the whole pipeline once. Use `--loop` to repeat it continuously.

`transfer`  
Run only the transfer stage.

`analyze`  
Run only the analysis stage.

`convert`  
Run only the conversion stage.

`crack`  
Run only the cracking stage.

`cleanup`  
Run only the cleanup stage.

`doctor`  
Check required tools and folders.

`status`  
Show counts of incoming PCAPs, processed PCAPs, bad PCAPs, and hash files.

`stats`  
Show total networks vs. cracked networks in the SQLite database.

`watch`  
Display live pipeline counts until interrupted.

`purge`  
Remove empty hash files and orphaned captures.

`export`  
Write cracked SSID/password pairs to `cracked_networks.txt`.

`bench`  
Run a `hashcat` benchmark.

`autopwn`  
Generate a simple SSID-based wordlist and use it with `hashcat`.

`init`  
Create the workspace folders and database.

## Output files

Depending on which commands you run, `pwnycli` may create:

- `~/pwnagotchi/data/incoming`
- `~/pwnagotchi/data/good_pcaps`
- `~/pwnagotchi/data/bad_pcaps`
- `~/pwnagotchi/data/hashes`
- `~/pwnagotchi/db/networks.db`
- `~/pwnagotchi/cracked_networks.txt`
- `~/pwnagotchi/tmp_autopwn.txt`

## Notes

- The `pwnycli` command is the installed entry point.
- The Python package lives under `dpwnycli/`.
- The project is designed around a simple file-based workflow and local SQLite storage.
- Some commands depend on external tools, so `doctor` is the easiest way to verify your setup.

## Safety

Use this tool only on networks and captures you own or are explicitly authorized to test.

## License

MIT

