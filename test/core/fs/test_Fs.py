import pytest
from co2.core.fs import Fs
from co2.core.fs import OFlags

class TestClassFs:
    @pytest.yield_fixture
    def instance(self):
        fs = Fs()
        yield fs
        # teardown test_do_opem
        fs.do_unlink("/file")

    def test_do_open(self, instance):
        assert instance.do_open("/file", OFlags.O_CREAT | OFlags.O_WRONLY) == True
        assert instance.do_open("/missing_dir/file", OFlags.O_CREAT |
                                OFlags.O_WRONLY) == False

    def test_do_unlink(self, instance):
        assert instance.do_open("/file2", OFlags.O_CREAT | OFlags.O_WRONLY) == True
        assert instance.do_unlink("/file2") == True
        assert instance.do_unlink("/missing_file") == False
        assert instance.do_unlink("/missing_dir/file") == False

    def test_do_mkdir(self, instance):
        assert instance.do_mkdir("/dir", OFlags.O_CREAT | OFlags.O_WRONLY) == True
        assert instance.do_mkdir("/dir", OFlags.O_RDONLY) == True
        assert instance.do_mkdir("/missing_dir", OFlags.O_RDONLY) == False

    def test_do_rmdir(self, instance):
        assert instance.do_rmdir("/dir") == True
        assert instance.do_rmdir("/missing_dir") == False

