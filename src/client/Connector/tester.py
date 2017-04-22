from package import Package
from frame import Frame
import random
import sys
import time

def callback_out(is_error, mes):
    print('Call callback OUT')
    print('Status ' + str(is_error))
    print('Message ' + str(mes))


def callback_in(data):
    print('Call Callback IN')
    print(data)


def test_1():

    time_from = time.time()

    for i in range(1):
        k = 100
        simple_data = 'Hello Casin, iam simple data' * k
        simple_data += '***'
        simple_data = '***' + simple_data

        pack_out = Package(simple_data, callback_out)

        frame_out = pack_out.next_frame()

        raw = frame_out.raw()

        print(raw)

        pack_in = Package(raw, callback_in)

        flag = True

        while flag:

            frame_in = pack_in.next_frame()

            raw = frame_in.raw()

            print(raw)

            pack_out.extend_bytes(raw)

            frame_out = pack_out.next_frame()

            if frame_out.is_last_frame():
                flag = False

            raw = frame_out.raw()

            print(raw)

            if not frame_out.is_internal():
                pack_in.extend_bytes(raw)

        time_to = time.time()
        print(time_to - time_from)
        print(sys.getsizeof(simple_data))


if __name__ == '__main__':
    test_1()


