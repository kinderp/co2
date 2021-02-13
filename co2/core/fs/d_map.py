import importlib


class MAJOR:
    DT_AWS_VPC = 1000
    DT_AWS_SUBNET = 1001
    DT_AWS_S3 = 1002


DEVICE_MAPPING = {
    "vpc": MAJOR.DT_AWS_VPC,
    "vpcsub": MAJOR.DT_AWS_SUBNET,
    "s3": MAJOR.DT_AWS_S3,
}


class DMap:

    @classmethod
    def _load_dt(cls):
        cls.class_properties = dict(vars(MAJOR))

    def __init__(self):
        self._load_dt()
        self.dmap = {self.class_properties[key] : [key, None] for key in self.class_properties if
                'DT_' in key}

    def load_item(self, s_dev, abs_path):
        major = DEVICE_MAPPING.get(s_dev)
        #module = abs_path.replace("/", ".")
        splitted_path = abs_path.split(".")
        class_name = splitted_path[-1]
        module_name = '.'.join(splitted_path[:-1])
        if major:
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            self.dmap[major][1] = class_()
            return True
        return False

    def unload_item(self, s_dev):
        major = DEVICE_MAPPING.get(s_dev)
        if major:
            self.dmap[major][1] = None
            return True
        return False
