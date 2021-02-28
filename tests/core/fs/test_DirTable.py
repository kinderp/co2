import pytest
from co2.core.fs.dir_table import  DirTable

class TestClassDirTable:
    @pytest.fixture
    def instance(self):
        return DirTable()

    def test_add(self, instance):
        instance._add(1, "test" )
        instance._add(3, "test_")
        assert instance._get("test")  == 1
        assert instance._get("test_") == 3

    def test_rem(self, instance):
        instance._add(1, "test" )
        instance._add(3, "test_")
        assert instance._get("test") == 1
        instance._rem("test")
        assert instance._get("test") == None

    def test_get(self, instance):
        instance._add(13, "test")
        assert instance._get("test") == 13
