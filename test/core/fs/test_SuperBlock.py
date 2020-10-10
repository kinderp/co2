import pytest
from co2.core.fs import Superblock

class TestClassSuperblock:
    @pytest.fixture
    def instance(self):
        return Superblock()

    def test_reserve_t_node_number(self, instance):
        reserved = instance.reserve_t_node_number()
        assert reserved == 1 # 0 is always already used

    def test_release_t_node_number(self, instance):
        reserved = instance.reserve_t_node_number()
        assert reserved == 2 # 0 is always already used, 1 already used above
        is_released = instance.release_t_node_number(reserved)
        assert is_released == True
