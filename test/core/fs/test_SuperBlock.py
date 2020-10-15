import pytest
from co2.core.fs import Superblock

class TestClassSuperblock:
    @pytest.fixture
    def instance(self):
        superblock = Superblock()
        yield superblock
        # teardown test_[reserve/release]_t_node_number
        superblock.release_t_node_number(1)

    def test_reserve_t_node_number(self, instance):
        reserved = instance.reserve_t_node_number()
        assert reserved == 1 # 0 is always already used

    def test_release_t_node_number(self, instance):
        reserved = instance.reserve_t_node_number() # reserve 1
        reserved = instance.reserve_t_node_number() # reserve 2
        assert reserved == 2 # 0 is always already used, 1 already used above
        is_released = instance.release_t_node_number(reserved)
        assert is_released == True
        assert instance.bitmap._get() == 2 # if correctly released it should be
                                           # returned back in a new _get() call
