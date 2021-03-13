from co2.drivers import Driver

class VPCDriver(Driver):
    def __init__(self):
        pass

    def read(self):
        print("Read")

    def write(self, buffer, count=1):
        for i in range(0,count):
            data = buffer[i]
            print(data)
        return count

