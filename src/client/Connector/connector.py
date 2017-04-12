import serial


class Connector:
    def __init__(self, port_name):
        self.port_name = port_name
        self.port_speed = 115200
        self.port_timeout = 3
        self.active = False
        self.queue_in = []
        self.queue_out = []


