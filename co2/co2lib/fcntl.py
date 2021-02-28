from co2.system_calls import IOSystemCalls
from co2.system_calls import ProcessSystemCalls


def open(filename : str, flags : int):
    file_table_number = IOSystemCalls.open(filename, flags)
    fd = ProcessSystemCalls.C_TASK.FDTABLE.add(file_table_number)
    return fd
