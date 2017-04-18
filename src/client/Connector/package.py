from frame import Frame, FrameIn
import random
import time


class PackageBase:

    def __init__(self):
        self._cmd = {
            'open request': 'o',
            'accept': 'y',
            'cancel': 'n',
            'close request': 'c',
            'data': 'd',
            'repeat': 'r',
            'hard break error': '!'
        }

        self._frames_cmd = []

        self._frames_data = []
        self._expected_cmds = []

        self._type = None

        self._next_frame = None
        self._last_frame = None

        self._max_frame_size = 1024
        self._service_data_size = 50
        self._max_data_size = self._max_frame_size - self._service_data_size

        self._creation_time = time.time()

    def type(self, val=None):
        if val is not None:
            self._type = val

        return self._type

    def next_frame(self):
        return self._next_frame

    def _update_expected(self, arr):
        self._expected_cmds = []
        self._expected_cmds.extend(arr)
        self._expected_cmds.append(
            self._cmd['hard break error']
        )

    def _set_next_frame(self, frame):
        self._last_frame = self._next_frame
        self._next_frame = frame

    def time(self, val=None):
        if val is not None:
            self._creation_time = val
        return self._creation_time


class PackageOut(PackageBase):

    def __init__(self, data, callback_out):
        super().__init__()
        self.type('out')
        self.__port_rank = random.random()
        self.__data = data
        self.__callback_out = callback_out
        self._update_expected([
            self._cmd['open request'],
            self._cmd['accept'],
            self._cmd['cancel']
        ])
        self._split_data()
        self._set_next_frame(
            Frame(self.__port_rank, self._cmd['open request'])
        )

    def _split_data(self):

        frame_count = (len(self.__data) // self._max_data_size) + 1
        data_cmd = self._cmd['data']
        data_chunk = ''

        for i in range(frame_count):
            from_index = i * self._max_data_size
            to_index = from_index + self._max_data_size

            if i == frame_count - 1:
                data_chunk = self.__data[from_index:]
            else:
                data_chunk = self.__data[from_index:to_index]

            self._frames_data.append(Frame(data_chunk, data_cmd))

    def _frame_handler(self, frame):

        if not frame.is_correct():
            self._set_next_frame(Frame('', self._cmd['repeat']))
            return

        cmd = frame.cmd()

        if cmd not in self._expected_cmds:
            self._set_next_frame(Frame('', self._cmd['hard break error']).is_last_frame(True))
            return

        if cmd == self._cmd['open request']:
            request_rank = float(frame.data_str())
            if self.__port_rank < request_rank:
                self._set_next_frame(Frame('', self._cmd['accept']))
                self._update_expected([
                    self._cmd['data'], self._cmd['repeat']
                ])
            elif self.__port_rank > request_rank:
                self._set_next_frame(Frame('', self._cmd['cancel']))

            elif self.__port_rank == request_rank:
                self._set_next_frame(Frame('', self._cmd['repeat']))


        elif cmd == self._cmd['accept']:
            pass
        elif cmd == self._cmd['cancel']:
            pass
        elif cmd == self._cmd['close request']:
            pass
        elif cmd == self._cmd['data']:
            pass
        elif cmd == self._cmd['repeat']:
            pass
        elif cmd == self._cmd['hard break error']:
            pass
        else:
            pass

    def _call_success(self):
        pass

    def _call_error(self):
        pass

    def extend_bytes(self, bytes_data):
        frame = Frame(bytes_data)
        self._frame_handler(frame)


class PackageIn(PackageBase):
    def __init__(self, bytes_data, callback_in):
        super().__init__()
        self.type('in')
        self.__callback_in = callback_in


def Package(data=None, callback=None):
    if isinstance(data, bytes):
        return PackageIn(data, callback)
    if isinstance(data, str):
        return PackageOut(data, callback)









if __name__ == '__main__':
    pack = PackageOut('#'*3265, lambda x: print(x))


