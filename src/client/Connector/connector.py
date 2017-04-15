import serial
from package import Package
import threading
import time


class Connector:

    cmd = {
        'open request': 'o',
        'accept': 'y',
        'cancel': 'n',
        'close request': 'c',
        'data': 'd',
        'repeat': 'r',
        'hard break': 'b',
        'resolve': '?'
    }

    last_direction = None

    port_speed = 115200
    port_timeout = 3
    sleep_time = 0.2

    active = False
    is_open = False
    port = None

    buffer_in = None
    buffer_out = None

    def __init__(self, port_name):
        self.port_name = port_name

        self.opener_thread = threading.Thread(target=self.opener, args=())
        self.opener_thread.daemon = True
        self.opener_thread.start()

        self.listener_thread = threading.Thread(target=self.listener, args=())
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def open(self):
        self.active = True

    def opener(self):
        while True:
            if not self.active:
                continue

            if self.is_open:
                continue

            try:
                self.port = serial.Serial(
                    self.port_name,
                    timeout=self.port_timeout,
                    baudrate=self.port_speed
                )
                self.is_open = True
            except:
                self.is_open = False
                self.port = None

            time.sleep(self.sleep_time)

    def close(self):
        self.active = False
        self.port = None
        self.is_open = None

    def listener(self):
        while True:
            if not self.active or not self.is_open:
                time.sleep(self.sleep_time)
                continue

            try:
                bytes_data = self.port.readall()
                package = Package(bytes_data)
                self.package_handler(package)
            except:
                pass

    def package_handler(self, package):
        cmd = package.cmd()

        if cmd == self.cmd['open request']:
            if self.buffer_in is None and self.buffer_out is None:
                self.buffer_in = ''
        elif cmd == self.cmd['accept']:
            pass
        elif cmd == self.cmd['cancel']:
            pass
        elif cmd == self.cmd['close request']:
            pass
        elif cmd == self.cmd['data']:
            pass
        elif cmd == self.cmd['repeat']:
            pass
        elif cmd == self.cmd['hard break']:
            pass
        else:
            pass




    def sender(self, package):
        if self.active and self.is_open:
            try:
                self.port.write(package.raw())
            except:
                pass


    def send(self, data, callback_out):
        pass

    def get(self):
        if len(self.array_in) == 0:
            return None

        return self.array_out.pop(0)




if __name__ == '__main__':
    pass




