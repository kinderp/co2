import pytest
from co2.core.fs import TNodesVector
from co2.core.fs import TNode
from co2.core.fs import Block

class TestClassTNodesVector:
    @pytest.fixture
    def instance(self):
        return TNodesVector()

    def test_add_entry(self, instance):
        children = [Block("Giuseppe"), Block("Antonio"), Block("Teresa")]
        parent   = Block("Peppino")
        block    = Block("Francesco", parent, children)
        t_n = TNode("Francesco", block)
        instance.add_entry(t_n, 0)

        assert instance.get_entry(0).filename == "Francesco"

    def test_get_entry(self, instance):
        block = Block("Test")
        t_n   = TNode("Test")
        instance.add_entry(t_n, 11)
        assert instance.get_entry(11).filename == "Test"

    def test_rem_entry(self, instance):
        block = Block("Test")
        t_n   = TNode("Test")
        instance.add_entry(t_n, 11)
        assert instance.get_entry(11).filename == "Test"
        removed = instance.rem_entry(11)
        assert instance.get_entry(11) == None
