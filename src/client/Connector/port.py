import serial
import threading
import os
import hashlib


class Connector:

    port_speed = 115200
    port_timeout = 3
    hash_len = 32
    queue_in = []
    queue_out = []
    active = False
    can_listen = False
    port = None
    thread_in = None
    thread_out = None

    def __init__(self, port_name, callback_in):
        self.port_name = port_name
        self.callback_in = callback_in

    def send(self, data, callback_out):
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
        self.thread_in = threading.Thread(target=self.listener)
        self.thread_in.daemon = True
        self.thread_in.start()


    def close(self):
        self.active = False
        self.can_listen = False
        self.port.close()

    def listener(self):
        while self.active:
            while self.can_listen:
                data = self.port.readall()
                print(data)




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
    filename = os.path.join('/', 'Users', 'Casin', 'Desktop', 'image.jpeg')

    mes = input('mes: ')

    hash = ''

    # with open(filename, 'rb') as file:
    #     m = hashlib.md5()
    #     while True:
    #         data = file.read(8192)
    #         if not data:
    #             break
    #         m.update(data)
    #     hash = m.hexdigest()
    #
    # print(hash)

    m = hashlib.md5()
    m.update(mes.encode('utf-8'))
    print(m.hexdigest())

    con = Connector('sdgfsdf', 'dfgdfg')
    print(con.port_name)
