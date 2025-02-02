import os
import sys
import argcomplete
import subprocess
from .command_parser import get_cached_commands

def fast_autocomplete(parser):
    """
    Improves autocomplete performance by caching command options.
    """
    cached_commands = get_cached_commands()
    
    def completer(prefix, parsed_args, **kwargs):
        """
        Custom autocomplete function that leverages cached commands.
        """
        return [cmd for cmd in cached_commands if cmd.startswith(prefix)]
    
    argcomplete.autocomplete(parser, validator=completer)

