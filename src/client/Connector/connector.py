import serial
from package import Package
import threading
import time


class Connector:

    def __init__(self, port_name, callback_in, callback_port_status):

        self.__next_priority_direction = 'in'

        self.__current_direction = None
        self.__current_package = None

        self.__port_speed = 115200
        self.__port_timeout = 3
        self.__sleep_time = 0.2

        self.__active = False
        self.__is_open = False
        self.__port = None

        self.__array_out = []

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

    def send(self, data, callback_out):
        if self.status() is True:
            package = Package(data, callback_out)
            self.__array_out.append(package)
        else:
            callback_out(False)

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
            if not self.status():
                time.sleep(self.__sleep_time)
                continue
            try:
                self.__read()
            except:
                self.__connection_error()

    def __sender(self, frame):
        if self.status():
            try:
                self.__port.write(frame.raw())
                return True
            except:
                self.__connection_error()

    def __read(self):

        if self.__current_direction is None:
            self.__start_connection()
            return
        else:
            self.__continue_connection()

    def __read_in(self):
        if self.status():
            try:
                bytes_data = self.__port.readall()
                return bytes_data if len(bytes_data) > 0 else None
            except:
                self.__connection_error()

    def __read_out(self):
        return self.__array_out[0] if len(self.__array_out) > 0 else None

    def __read_priority(self, direction):

        if direction == 'in':
            bytes_data = self.__read_in()
            if bytes_data is not None:
                return Package(bytes_data, self.__callback_in)

            package = self.__read_out()
            if package is not None:
                return package

        if direction == 'out':
            package = self.__read_out()
            if package is not None:
                return package

            bytes_data = self.__read_in()
            if bytes_data is not None:
                return Package(bytes_data, self.__callback_in)

        return None

    def __connection_error(self):
        self.__callback_port_status(False)
        self.close()
        self.open()
        self.__current_direction = None
        self.__current_package = None

    def __start_connection(self):
        package = self.__read_priority(self.__next_priority_direction)

        if package is None:
            return package

        if package.type() == 'in':
            self.__next_priority_direction = 'out'

        if package.type() == 'out':
            self.__next_priority_direction = 'in'

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

        if frame_to_send is None or frame_to_send.is_last_frame():
            self.__close_conenction()

        if frame_to_send is not None:
            self.__sender(frame_to_send)

    def __close_conenction(self):
        if self.__current_direction == 'out':
            self.__array_out.pop(0)
        self.__current_direction = None
        self.__current_package = None


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





