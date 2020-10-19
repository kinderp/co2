from abc import ABCMeta, abstractmethod
from co2.system_calls import IOSystemCalls

from co2.ipc import Client

class CO2Commands:
    CO2_INIT   = 0
    CO2_COMMIT = 1
    CO2_BUILD  = 2
    CO2_INSMOD = 3
    CO2_RMOD   = 4
    CO2_MOUNT  = 100
    CO2_TOUCH  = 1000
    CO2_RM     = 1001
    CO2_MKDIR  = 1002
    CO2_RMDIR  = 1003

    @classmethod
    def _to_dict(cls):
        data = {}
        class_properties = dict(vars(cls))
        return {class_properties[key] : key for key in class_properties if
                'CO2_' in key}

    @classmethod
    def look_up(cls, value):
        try:
            return cls._to_dict()[value]
        except KeyError:
            return None

class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def init(argsubparsers):
        pass

    @abstractmethod
    def execute(args):
        pass


