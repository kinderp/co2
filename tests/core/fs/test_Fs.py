import pytest
from co2.core.fs.fs import Fs
from co2.core.fs.fs import OFlags

from co2.system_calls import IOSystemCalls

class TestClassFs:
    @pytest.yield_fixture
    def instance(self):
        IOSystemCalls.init()
        yield IOSystemCalls.super_table["ram0"]
        # teardown test_do_opem
        IOSystemCalls.super_table["ram0"].do_unlink("/file")

    def test_do_open(self, instance):
        assert instance.do_open("/file", OFlags.O_CREAT | OFlags.O_WRONLY) >= 0
        assert instance.do_open("/missing_dir/file", OFlags.O_CREAT |
                                OFlags.O_WRONLY) < 0

    def test_do_unlink(self, instance):
        assert instance.do_open("/file2", OFlags.O_CREAT | OFlags.O_WRONLY) >= 0
        assert instance.do_unlink("/file2") >= 0
        assert instance.do_unlink("/missing_file") < 0
        assert instance.do_unlink("/missing_dir/file") < 0

    def test_do_mkdir(self, instance):
        assert instance.do_mkdir("/dir", OFlags.O_CREAT | OFlags.O_WRONLY) >= 0
        assert instance.do_mkdir("/dir", OFlags.O_RDONLY) >= 0
        assert instance.do_mkdir("/missing_dir", OFlags.O_RDONLY) < 0

    def test_do_rmdir(self, instance):
        assert instance.do_mkdir("/dir", OFlags.O_CREAT | OFlags.O_WRONLY) >= 0
        assert instance.do_rmdir("/dir") >= 0
        assert instance.do_rmdir("/missing_dir") < 0

