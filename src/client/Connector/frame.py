import hashlib
import time


class FrameBase:


    def __init__(self):
        self.type_info = None

        self.hash_info = {
            'val': None,
            'from': 0,
            'to': 32
        }

        self.cmd_info = {
            'val': None,
            'to': self.hash_info['to'] + 1,
            'from': self.hash_info['to']
        }

        self.time_info = {
            'val': None,
            'to': self.cmd_info['to'] + 17,
            'from': self.cmd_info['to']
        }

        self.data_str_info = {
            'val': None,
            'from': self.time_info['to']
        }

        self.data_bytes_info = {
            'val': None
        }

        self.raw_info = {
            'val': None,
            'len': None
        }

    def type(self, val=None):
        if val is not None:
            self.type_info = val
        return self.type_info

    def hash(self, val=None):
        if val is not None:
            self.hash_info['val'] = val
        return self.hash_info['val']

    def cmd(self, val=None):
        if val is not None:
            self.cmd_info['val'] = val
        return self.cmd_info['val']

    def time(self, val=None):
        if val is not None:
            self.time_info['val'] = val
        return self.time_info['val']

    def data_str(self, val=None):
        if val is not None:
            self.data_str_info['val'] = val
        return self.data_str_info['val']

    def data_bytes(self, val=None):
        if val is not None:
            self.data_bytes_info['val'] = val
        return self.data_bytes_info['val']

    def raw(self, val=None):
        if val is not None:
            self.raw_info['val'] = val
            self.raw_info['len'] = len(val)
        return self.raw_info['val']

    def size(self):
        return self.raw_info['len']

    @staticmethod
    def _bytes_to_hash(bytes_data):
        return hashlib.md5(bytes_data).hexdigest()

    @staticmethod
    def _convert(data):
        if isinstance(data, str):
            return data.encode('utf-8')

        if isinstance(data, bytes):
            return data.decode('utf-8')


class FrameIn(FrameBase):

    def __init__(self, frame_bytes):
        super().__init__()
        self.type('in')
        self.raw(frame_bytes)
        self.frame_bytes_decoded = self._convert(self.raw())
        self.__parse()

    def __parse(self):
        self.hash(self.frame_bytes_decoded[
            self.hash_info['from']:self.hash_info['to']
        ])
        self.cmd(self.frame_bytes_decoded[
            self.cmd_info['from']:self.cmd_info['to']
        ])
        self.time(float(self.frame_bytes_decoded[
            self.time_info['from']:self.time_info['to']
        ]))
        self.data_str(self.frame_bytes_decoded[
            self.data_str_info['from']:
        ])
        self.data_bytes(self._convert(self.data_str()))

    def is_correct(self):
        real_hash = self._bytes_to_hash(self._convert(
            self.cmd() + str(self.time()) + self.data_str()
        ))
        return real_hash == self.hash()


class FrameOut(FrameBase):

    def __init__(self, data_str, command):
        super().__init__()
        self.type('out')
        self.data_str(data_str)
        self.data_bytes(self._convert(self.data_str()))
        self.cmd(command)
        self.time(time.time())
        self.__is_last_frame = False
        frame_str_without_hash = self.cmd() + str(self.time()) + self.data_str()
        self.hash(self._bytes_to_hash(self._convert(
            frame_str_without_hash
        )))
        frame_str = self.hash() + frame_str_without_hash
        self.raw(self._convert(frame_str))

    def is_last_frame(self, val):
        if val is not None:
            self.__is_last_frame = val

        return self.__is_last_frame


def Frame(data, command='*'):
    if isinstance(data, bytes):
        return FrameIn(data)
    elif isinstance(data, str):
        return FrameOut(data, command)
    return None


if __name__ == '__main__':
    some_data = b'ac9323af97eff9f6c082906324968179*1492343468.174098iam vaper'
    some_data2 = 'iam vaper'
    pack = Frame(some_data)
    print(pack.cmd())
    print(pack.time())
    print(pack.hash())
    print(pack.data_str())
    print(pack.type())
    print(pack.is_correct())
    print(pack.raw())