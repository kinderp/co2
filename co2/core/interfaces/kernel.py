from co2.ipc.messages import CO2Messages
from co2.system_calls import IOSystemCalls

CALL_VEC = {
        CO2Messages.CO2_INSMOD: None,
        CO2Messages.CO2_RMOD: None,
        CO2Messages.CO2_MKNOD: IOSystemCalls.mknod,
        CO2Messages.CO2_MOUNT: IOSystemCalls.mount,
        CO2Messages.CO2_UMOUNT: IOSystemCalls.umount,
        CO2Messages.CO2_TOUCH: IOSystemCalls.open,
        CO2Messages.CO2_RM: IOSystemCalls.unlink,
        CO2Messages.CO2_MKDIR: IOSystemCalls.mkdir,
        CO2Messages.CO2_RMDIR: IOSystemCalls.rmdir,
}

def _SYSCALL(num, args):
    return CALL_VEC[num](**args)

