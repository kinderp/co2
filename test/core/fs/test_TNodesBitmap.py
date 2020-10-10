import pytest
from co2.core.fs import TNodesBitmap

class TestClassTNodesBitmap:
    @pytest.fixture
    def instance(self):
        return TNodesBitmap()

    def test_add(self, instance):
        instance._add(1)
        instance._add(5)
        instance._add(99)

        assert 1  in instance.bitmap
        assert 5  in instance.bitmap
        assert 99 in instance.bitmap

    def test_rem(self, instance):
        instance._add(33)
        assert 33 in instance.bitmap
        instance._rem(33)
        assert 33 not in instance.bitmap

    def test_get(self, instance):
        instance._add(1)
        instance._add(2)
        instance._add(3)
        instance._rem(2)
        t_nodes_number = instance._get()
        assert t_nodes_number == 2

        instance._rem(0)
        t_nodes_number = instance._get()
        assert t_nodes_number == 0
