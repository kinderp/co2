import argparse

class CLIParser:

    argparser = None
    argsubparsers = None

    @classmethod
    def init(cls):
        cls.argparser = argparse.ArgumentParser(prog="co2", description="Back to the future...")
        cls.argsubparsers = cls.argparser.add_subparsers(title="Commands", dest="command")
        cls.argsubparsers.required = True

        argsp = cls.argsubparsers.add_parser("touch", help="Create a new file")
        argsp.add_argument("path", help="Create a file", type=str)

        argsp = cls.argsubparsers.add_parser("rm", help="Remove a file")
        argsp.add_argument("path", help="Remove a file", type=str)


        argsp = cls.argsubparsers.add_parser("mkdir", help="Create a new directory")
        argsp.add_argument("path", help="Remove a file", type=str)

        argsp = cls.argsubparsers.add_parser("rmdir", help="Remove a directory")
        argsp.add_argument("path", help="Remove a file", type=str)

    @classmethod
    def parse(cls, argv):
        return cls.argparser.parse_args(argv)

