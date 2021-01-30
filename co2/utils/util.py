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
        argsp.add_argument("abs_filename", help="Create a file", type=str)

        argsp = cls.argsubparsers.add_parser("rm", help="Remove a file")
        argsp.add_argument("abs_filename", help="Remove a file", type=str)


        argsp = cls.argsubparsers.add_parser("mkdir", help="Create a new directory")
        argsp.add_argument("abs_filename", help="Create a new directory", type=str)

        argsp = cls.argsubparsers.add_parser("rmdir", help="Remove a directory")
        argsp.add_argument("abs_filename", help="Remove a directory", type=str)

        argsp = cls.argsubparsers.add_parser("mount", help="Mount a device")
        argsp.add_argument("abs_filename", help="Mount a device", type=str)

        argsp = cls.argsubparsers.add_parser("umount", help="Unount a device")
        argsp.add_argument("abs_filename", help="Unmount a device", type=str)

    @classmethod
    def parse(cls, argv):
        return cls.argparser.parse_args(argv)

