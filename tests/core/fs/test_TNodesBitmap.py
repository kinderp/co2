import pytest
from co2.core.fs.t_nodes_bitmap import TNodesBitmap

class TestClassTNodesBitmap:
    @pytest.yield_fixture
    def instance(self):
        bitmap = TNodesBitmap()
        yield bitmap

        # teardown for test_add()
        bitmap._rem(1)
        bitmap._rem(5)
        bitmap._rem(99)

        # teardown for test_rem()
        # nothing to do

        # teardown for test_get()
        bitmap._rem(1)
        bitmap._rem(3)


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

