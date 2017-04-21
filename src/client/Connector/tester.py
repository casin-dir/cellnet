from package import Package


def callback_out():
    print('Call callback OUT')


def callback_in():
    print('Call Callback IN')


def test_1():

    for i in range(1):
        simple_data = 'Hello Casin, iam simple data'

        pack_out = Package(simple_data, callback_out)
        frame_out = pack_out.next_frame()

        raw = frame_out.raw()

        pack_in = Package(raw, callback_in)

        frame_in = pack_in.next_frame()

        raw = frame_in.raw()

        pack_out.extend_bytes(raw)

        frame_out = pack_out.next_frame()

        raw = frame_out.raw()

        pack_in.extend_bytes(raw)

        frame_in = pack_in.next_frame()

        raw = frame_in.raw()

        pack_out.extend_bytes(raw)

        frame_out = pack_out.next_frame()

        print(frame_out.cmd())




if __name__ == '__main__':
    test_1()


