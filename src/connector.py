class Connector:
    def __init__(self):
        self.port = 'some port'
        devList = usb.core.find(find_all=True)
        print(devList)

    def connect(self, port_name):
        print('connecting...' + port_name)

    def find_ports(self):
        print('finding')