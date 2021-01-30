class CO2Messages:
    CO2_ERROR   = -1
    CO2_SUCCESS = 0
    CO2_INIT    = 1
    CO2_COMMIT  = 2
    CO2_BUILD   = 3
    CO2_INSMOD  = 4
    CO2_RMOD    = 5
    CO2_MKNOD   = 6
    CO2_MOUNT   = 100
    CO2_UMOUNT  = 101
    CO2_TOUCH   = 1000
    CO2_RM      = 1001
    CO2_MKDIR   = 1002
    CO2_RMDIR   = 1003

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

class Message:
    def __init__(self, code, description, args):
        self.raw_data = vars(args)
        self.data = {k: self.raw_data[k] for k in self.raw_data if k != "command"}
        self.code = code
        self.description = description

    def to_dict(self):
        return {
            "code": self.code,
            "description": self.description,
            "data": self.data
        }

class MessageError(Message):
    pass

class MessageSuccess(Message):
    pass
