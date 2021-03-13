from co2.system_calls import IOSystemCalls

def close(fd : int):
    f_table_index  = ProcessSystemCalls.C_TASK.FDTABLE.get(fd)
    t_node_number, count, s_dev = IOSystemCalls.file_table.get_entry(f_table_index)
    IOSystemCalls.file_table.del_entry(f_table_index)
    t_node = IOSystemCalls.super_table[s_dev].superblock.get_entry(t_node_number)
    t_node.count += 1


def read():
    pass

def write(fd : int, buffer : object, count : int = 1):
    return IOSystemCalls.write(fd, buffer, count)
