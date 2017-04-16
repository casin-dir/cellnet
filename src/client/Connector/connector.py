import serial
from frame import Frame
from package import Package
import threading
import time


class Connector:

    __cmd = {
        'open request': 'o',
        'accept': 'y',
        'cancel': 'n',
        'close request': 'c',
        'data': 'd',
        'repeat': 'r',
        'hard break': 'b',
        'resolve': '?'
    }

    __next_direction = 'in'

    __current_direction = None
    __current_package = None

    __port_speed = 115200
    __port_timeout = 3
    __sleep_time = 0.2

    __active = False
    __is_open = False
    __port = None

    __array_out = []

    def __init__(self, port_name, callback_in, callback_port_status):
        self.__port_name = port_name
        self.__callback_in = callback_in
        self.__callback_port_status = callback_port_status

        self.__opener_thread = threading.Thread(target=self.__opener, args=())
        self.__opener_thread.daemon = True
        self.__opener_thread.start()

        self.__listener_thread = threading.Thread(target=self.__listener, args=())
        self.__listener_thread.daemon = True
        self.__listener_thread.start()

    def open(self):
        self.__active = True
        self.__callback_port_status(False)

    def close(self):
        self.__active = False
        self.__is_open = False
        try:
            self.__port.close()
            self.__callback_port_status(False)
        except:
            pass
        self.__port = None

    def send(self, data, callback_status):
        if self.status() is True:
            package = Package(data, callback_status)
            self.__array_out.append(package)
        else:
            callback_status(False)

    def status(self):
        return self.__active and self.__is_open

    def __opener(self):
        while True:
            if not self.__active:
                continue

            if self.__is_open:
                continue

            try:
                self.__port = serial.Serial(
                    self.__port_name,
                    timeout=self.__port_timeout,
                    baudrate=self.__port_speed
                )
                self.__is_open = True
                self.__callback_port_status(True)
            except:
                self.__is_open = False
                self.__port = None

            time.sleep(self.__sleep_time)

    def __listener(self):
        while True:
            if not self.__active or not self.__is_open:
                time.sleep(self.__sleep_time)
                continue
            try:
                self.__read()
            except:
                pass

    def __sender(self, frame):
        if self.__active and self.__is_open:
            try:
                self.__port.write(frame.raw())
                return True
            except:
                return False

        return False

    def __read(self):

        if self.__current_direction is None:
            self.__start_connection()
            return

        if self.__current_direction == 'in':
            self.__continue_connection()

        if self.__current_direction == 'out':
            self.__continue_connection()

    def __read_in(self):
        if self.__active and self.__is_open:
            try:
                bytes_data = self.__port.readall()
                return bytes_data if len(bytes_data) > 0 else None
            except:
                pass
        self.__connection_error()

    def __read_out(self):
        return self.__array_out.pop(0) if len(self.__array_out) > 0 else None

    def __read_priority(self, direction):
        if direction == 'in':
            bytes_data = self.__read_in()
            if bytes_data is not None:
                package = Package()
                package.extend_bytes(bytes_data)
                return package

        if direction == 'out':
            package = self.__read_out()
            if package is not None:
                return package

        return None

    def __connection_error(self):
        self.__callback_port_status(False)
        self.close()
        self.open()
        self.__current_direction = None
        self.__current_package = None

    def __start_connection(self):
        package = self.__read_priority(self.__next_direction)

        if package is None:
            return package

        if package.type() == 'in':
            self.__next_direction = 'out'

        if package.type() == 'out':
            self.__next_direction = 'in'

        self.__current_package = package
        self.__current_direction = package.type()
        frame_to_send = self.__current_package.next_frame()
        self.__sender(frame_to_send)

    def __continue_connection(self):
        bytes_data = self.__read_in()
        if bytes_data is None:
            return

        self.__current_package.extend_bytes(bytes_data)
        frame_to_send = self.__current_package.next_frame()
        if frame_to_send is None:
            self.__current_direction = None
            self.__current_package = None
        else:
            self.__sender(frame_to_send)

if __name__ == '__main__':

    test_data = '192.168.0.1#Hello Casin, how are you?'

    def callback_in_test(package):
        data = package.data()
        time_s = package.time()
        print('Incoming package:\n{0}\nTime: {1}'.format(data, time_s))

    def callback_status_test(package):
        data = package.data()
        time_s = package.time()
        print('Package sent with status: {0}\nTime: {1}'.format(data, time_s))

    connector = Connector('COM1', callback_in_test)
    connector.send(test_data, callback_status_test)

    while True:
        # print('waiting')
        time.sleep(1)





