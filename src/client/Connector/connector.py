import serial
import threading


class Connector:
    def __init__(self, port_name):
        self.port_name = port_name
        self.port_speed = 115200
        self.port_timeout = 3
        self.frame_size = 64
        self.active = False
        self.queue_in = []
        self.queue_out = []
        self.port = None
        self.listener_thread = None
        self.writer_thread = None

    def is_correct(self, frame):
        return True

    def fraction(self, data):
        frame_list = []
        return frame_list

    def join(self, frame_list):
        pass

    def send(self, data, callback):
        pass

    def get(self):
        if len(self.queue_in) == 0:
            return None

        return self.queue_in.pop(0)

    def open(self):
        self.port = serial.Serial(
            self.port_name,
            timeout=self.port_timeout,
            baudrate=self.port_speed
        )
        self.active = True
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        self.listener_thread = threading.Thread(target=self.writer)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def close(self):
        self.active = False
        self.port.close()

    def listener(self):
        while self.active:
            data = self.port.read(self.frame_size)
            if self.is_correct(data):
                pass



    def writer(self):
        while self.active:
            pass

    # encoded_data_1 = data1.encode('utf-8')
    # encoded_data_2 = data2.encode('utf-8')
    #
    # self.port_in.write(encoded_data_1)
    # self.port_out.write(encoded_data_2)
    # res_in = self.port_in.readall()
    # res_out = self.port_out.readall()
    #
    # print('Result in: ' + res_in.decode('utf-8'))
    # print('Result out: ' + res_out.decode('utf-8'))


if __name__ == '__main__':
    connector = Connector('COM1')
    connector.open()
