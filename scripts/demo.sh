#!/bin/bash
set -euo pipefail

game_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$game_root"

python3 - <<'PY'
import re
import subprocess
import sys
from pathlib import Path

cmd = ["python3", "app/game.py"]
proc = subprocess.Popen(
    cmd,
    cwd=str(Path.cwd()),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

def read_until_prompt():
    buffer = ""
    while True:
        ch = proc.stdout.read(1)
        if ch == "":
            break
        buffer += ch
        if buffer.endswith("\n> "):
            break
    if buffer:
        sys.stdout.write(buffer)
        sys.stdout.flush()
    return buffer

def send(command: str) -> str:
    if proc.poll() is not None:
        return ""
    proc.stdin.write(command + "\n")
    proc.stdin.flush()
    return read_until_prompt()

output = read_until_prompt()
password = None

def capture_password(output_text: str) -> str | None:
    match = re.search(r"password to unlock the door is: ([A-Z]+)", output_text)
    if match:
        return match.group(1)
    return None

send("look")
send("take key")
note_output = send("read note")
password = capture_password(note_output)
if not password:
    raise SystemExit("Failed to capture password from note.")

send("open door")
send(f"unlock door with {password}")
send("go north")
send("read inscription")
send("go north")

for _ in range(10):
    if proc.poll() is not None:
        break
    attack_output = send("attack")
    if proc.poll() is not None or not attack_output:
        break

proc.wait()
remaining = proc.stdout.read()
if remaining:
    sys.stdout.write(remaining)
    sys.stdout.flush()
PY
