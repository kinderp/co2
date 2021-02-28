import pytest
from co2.core.fs.f_table import FTable

class TestClassFTable:
    @pytest.fixture
    def instance(self):
        yield FTable()
        # teardown down below

    def test_add_entry(self, instance):
        t_node_number = 12
        s_dev = "ram0"
        ftable_index = instance.add_entry(t_node_number, s_dev)
        t_node_number_, count_, s_dev_ = instance.get_entry(ftable_index)
        assert t_node_number_ == t_node_number
        assert count_ == 1
        assert s_dev_ == s_dev

        s_dev_2 = "hda"
        ftable_index_2 = instance.add_entry(t_node_number, s_dev_2)
        t_node_number_, count_, s_dev_ = instance.get_entry(ftable_index_2)

        assert ftable_index != ftable_index_2
        assert t_node_number == t_node_number_
        assert count_ == 1
        assert s_dev_2 == s_dev_


    def test_del_entry(self, instance):
        pass
