#!/usr/bin/env python3
import sys
import argparse

from co2.commands import CommandMkdir
from co2.commands import CommandRmdir
from co2.commands import CommandTouch
from co2.commands import CommandRm
from co2.commands import CommandsFactory

from co2.utils import CLIParser


if __name__ == "__main__":
    CLIParser.init()
    args = CLIParser.parse(sys.argv[1:])
    CommandsFactory.create(args.command).execute(args)
