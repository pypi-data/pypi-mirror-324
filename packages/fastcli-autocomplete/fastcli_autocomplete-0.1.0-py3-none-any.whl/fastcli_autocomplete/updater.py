import os
import subprocess
from .command_parser import extract_cli_commands, CACHE_FILE

def check_for_updates():
    """
    Checks if the CLI tool has been updated and refreshes autocomplete.
    """
    latest_commands = extract_cli_commands()
    
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cached_commands = json.load(f)
        
        if latest_commands != cached_commands:
            with open(CACHE_FILE, "w") as f:
                json.dump(latest_commands, f)
            print("Autocomplete updated to match new CLI version.")

