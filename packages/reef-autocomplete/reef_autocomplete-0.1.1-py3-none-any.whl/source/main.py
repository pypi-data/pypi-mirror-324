import argparse
import argcomplete

def custom_completer(prefix, parsed_args, **kwargs):
    options = ["install", "update", "uninstall"]
    return [cmd for cmd in options if cmd.startswith(prefix)]

parser = argparse.ArgumentParser()
parser.add_argument("command", help="Select a command").completer = custom_completer

argcomplete.autocomplete(parser)
args = parser.parse_args()

print(f"Selected command: {args.command}")