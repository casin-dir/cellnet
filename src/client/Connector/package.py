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
            'hard break error': '!',
            'empty': '*'
        }

        self._frames_data = []
        self._expected_cmds = []

        self._type = None

        self._next_frame = None
        self._last_frame = None

        self._max_frame_size = 1024
        self._service_data_size = 50
        self._max_data_size = self._max_frame_size - self._service_data_size

        self._creation_time = round(time.time())

    def type(self, val=None):
        if val is not None:
            self._type = val

        return self._type

    def next_frame(self):
        self._last_frame = self._next_frame
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

    def extend_bytes(self, bytes_data):
        frame = Frame(bytes_data)
        self._frame_handler(frame)

    def _frame_handler(self, frame):
        pass


class PackageOut(PackageBase):

    def __init__(self, data, callback_out):
        super().__init__()
        self.type('out')
        self.__port_rank = str(random.random())
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
            next_frame = Frame('', self._cmd['hard break error'])
            next_frame.is_last_frame(True)
            self.__call_error('Unexpected command')
            self._set_next_frame(next_frame)
            return

        # OPEN REQUEST
        if cmd == self._cmd['open request']:
            request_rank = float(frame.data_str())
            if self.__port_rank < request_rank:
                self._set_next_frame(Frame('', self._cmd['accept']))
                self._update_expected([
                    self._cmd['data'], self._cmd['repeat']
                ])
            elif self.__port_rank > request_rank:
                next_frame = Frame('', self._cmd['empty'])
                next_frame.is_internal()
                self._set_next_frame(next_frame)
                self._update_expected([
                    self._cmd['accept'], self._cmd['repeat']
                ])

            elif self.__port_rank == request_rank:
                self.__port_rank = str(random.random())
                next_frame = Frame(self.__port_rank, self._cmd['repeat'])
                self._set_next_frame(next_frame)
                self._update_expected([
                    self._cmd['open request']
                ])

        # ACCEPT
        elif cmd == self._cmd['accept']:

            if self._last_frame.cmd() == self._cmd['open request'] or \
                            self._last_frame.cmd() == self._cmd['data']:

                next_frame = self._frames_data.pop(0) if len(self._frames_data) > 0 else \
                    Frame('', self._cmd['close request'])
                self._set_next_frame(next_frame)
                self._update_expected([
                    self._cmd['accept'],
                    self._cmd['cancel'],
                    self._cmd['repeat'],
                ])
                return

            if self._last_frame.cmd() == self._cmd['close request']:
                self.__call_end()
                self.__call_success()
                return

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

    def __call_end(self):
        next_frame = Frame('', self._cmd['empty'])
        next_frame.is_last_frame(True)
        next_frame.is_internal(True)
        self._set_next_frame(next_frame)

    def __call_success(self):
        self.__callback_out(True, None)

    def __call_error(self, error_mes='Unknown error'):
        self.__callback_out(True, error_mes)


class PackageIn(PackageBase):
    def __init__(self, bytes_data, callback_in):
        super().__init__()
        self.type('in')
        self.__callback_in = callback_in
        self._update_expected([
            self._cmd['open request'],
        ])
        self.extend_bytes(bytes_data)

    def _frame_handler(self, frame):

        # REPEAT REQUEST
        if not frame.is_correct():
            self._set_next_frame(Frame('', self._cmd['repeat']))
            return

        # CHECK CORRECT
        cmd = frame.cmd()
        if cmd not in self._expected_cmds:
            self._set_next_frame(Frame('', self._cmd['hard break error']).is_last_frame(True))
            return

        # OPEN REQUEST
        if cmd == self._cmd['open request']:
            self._update_expected([
                self._cmd['data'],
                self._cmd['repeat']
            ])
            next_frame = Frame('', self._cmd['accept'])
            self._set_next_frame(next_frame)

        # ACCEPT
        elif cmd == self._cmd['accept']:
            pass

        # CANCEL
        elif cmd == self._cmd['cancel']:
            pass

        # CLOSE
        elif cmd == self._cmd['close request']:
            next_frame = Frame('', self._cmd['accept'])
            next_frame.is_last_frame(True)
            self._set_next_frame(next_frame)
            self._call_incoming()

        # DATA
        elif cmd == self._cmd['data']:
            self._update_expected([
                self._cmd['data'],
                self._cmd['close request'],
                self._cmd['repeat']
            ])
            self._frames_data.append(frame)
            next_frame = Frame('', self._cmd['accept'])
            self._set_next_frame(next_frame)

        # REPEAT
        elif cmd == self._cmd['repeat']:
            pass

        # HARD BREAK ERROR
        elif cmd == self._cmd['hard break error']:
            next_frame = Frame('', self._cmd['empty'])
            next_frame.is_last_frame(True)
            next_frame.is_internal(True)

        # ???
        else:
            pass

    def _call_incoming(self):
        result = ''
        for frame in self._frames_data:
            result += frame.data_str()

        self.__callback_in(result)


def Package(data=None, callback=None):
    if isinstance(data, bytes):
        return PackageIn(data, callback)
    if isinstance(data, str):
        return PackageOut(data, callback)
