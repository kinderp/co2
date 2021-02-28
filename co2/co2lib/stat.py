from co2.system_calls import IOSystemCalls
from co2.system_calls import ProcessSystemCalls


def mkdir(filename : str):
    file_table_number = IOSystemCalls.mkdir(filename)
    fd = ProcessSystemCalls.C_TASK.FDTABLE.add(file_table_number)
    return fd
