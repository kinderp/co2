import pytest
from co2.core.fs import TNode
from co2.core.fs import Block

class TestClassTNode:
    @pytest.fixture
    def instance(self):
        filename = "Francesco"
        children = [Block("Giuseppe"), Block("Antonio"), Block("Teresa")]
        parent   = Block("Peppino")
        return TNode(
            filename = filename,
            block    = Block(filename, parent, children),
        )

    def test_add_dir_entry(self, instance):
        instance.add_dir_entry(12, "Test")
        assert  instance.get_dir_entry("Test") == 12

    def test_rem_dir_entry(self, instance):
        instance.add_dir_entry(12, "Test")
        assert  instance.get_dir_entry("Test") == 12
        removed = instance.rem_dir_entry("Test")
        assert instance.get_dir_entry("Test") == None
