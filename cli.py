import sys

args = sys.argv[1:]

if "create-strategy" in args:
    pass

if len(args) == 0:
    print("Usage: python3 cli.py <command>")
    print("Commands:")
    print("\thelp: show this help message and exit")
    print("\tcreate-strategy [name]: create a new strategy")
