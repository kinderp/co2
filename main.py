#!/usr/bin/env python3

from co2.commands import CommandMkdir
from co2.commands import CommandRmdir
from co2.commands import CommandTouch
from co2.commands import CommandRm

import sys
import argparse

argparser = argparse.ArgumentParser(prog="co2", description="Back to the future...")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

COMMANDS = {
	"mkdir": CommandMkdir(argsubparsers),
	"rmdir": CommandRmdir(argsubparsers),
	"touch": CommandTouch(argsubparsers),
	"rm"   :    CommandRm(argsubparsers),
}

if __name__ == "__main__":
	argv = sys.argv[1:]
	args = argparser.parse_args(argv)
	COMMANDS[args.command].execute(args)
