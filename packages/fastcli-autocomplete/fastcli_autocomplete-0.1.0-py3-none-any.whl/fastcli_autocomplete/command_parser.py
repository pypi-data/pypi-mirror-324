import os
import subprocess
import json

CACHE_FILE = "/tmp/fastcli_cache.json"

def extract_cli_commands(cli_path="mycli.py"):
    """
    Extracts available commands from the CLI script.
    """
    try:
        result = subprocess.run(
            ["python", cli_path, "--help"],
            capture_output=True,
            text=True
        )
        commands = [
            line.strip().split()[0] for line in result.stdout.split("\n") if line.strip()
        ]
        return commands
    except Exception:
        return []

def get_cached_commands():
    """
    Returns cached commands if available; otherwise, regenerates them.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    
    commands = extract_cli_commands()
    
    with open(CACHE_FILE, "w") as f:
        json.dump(commands, f)
    
    return commands

