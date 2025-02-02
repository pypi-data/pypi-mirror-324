import unittest
from fastcli_autocomplete.command_parser import extract_cli_commands

class TestCommandParser(unittest.TestCase):
    def test_extract_cli_commands(self):
        commands = extract_cli_commands("cli_example/mycli.py")
        self.assertIn("start", commands)
        self.assertIn("stop", commands)
        self.assertIn("restart", commands)

if __name__ == "__main__":
    unittest.main()

