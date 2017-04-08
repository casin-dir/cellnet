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

    def send_data(self, data):
        encoded_data = data.encode('utf-8')
        print('Data will be send: ' + encoded_data)
        bytes_in = self.port_in.write(encoded_data)
        print('Bytes has been sent: ' + bytes_in.decode('utf-8'))
        res = self.port_out.read()
        print('Result: ' + res.decode('utf-8'))






