# from connector import Connector
#
#

import serial


class Connector:
    def __init__(self):
        self.port_name_in = 'COM1'
        self.port_name_out = 'COM2'
        self.port_speed = 115200
        self.port_timeout = 3
        self.port_in = None
        self.port_out = None

    def connect(self):
        self.port_in = serial.Serial(
            self.port_name_in,
            timeout=self.port_timeout,
            baudrate=self.port_speed
        )
        self.port_out = serial.Serial(
            self.port_name_out,
            timeout=self.port_timeout,
            baudrate=self.port_speed
        )

    def disconnect(self):
        self.port_in.close()
        self.port_out.close()

    def send_data(self, data1, data2):
        encoded_data_1 = data1.encode('utf-8')
        encoded_data_2 = data2.encode('utf-8')

        self.port_in.write(encoded_data_1)
        self.port_out.write(encoded_data_2)
        res_in = self.port_in.readall()
        res_out = self.port_out.readall()

        print('Result in: ' + res_in.decode('utf-8'))
        print('Result out: ' + res_out.decode('utf-8'))




if __name__ == '__main__':
    connector = Connector()
    connector.connect()
    connector.send_data('Hello Casin!\n How are you?', 'Hello i\'m fine')
    connector.disconnect()


