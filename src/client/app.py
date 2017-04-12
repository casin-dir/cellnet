import sys
import time
import threading


def command_listener(stop_command):
    while True:
        command = sys.stdin.readline().rstrip()
        if command == stop_command:
            print(command)
            sys.exit(0)


class App:
    def __init__(self, ports, delimiter):
        self.port_names = ports.split(delimiter)


if __name__ == '__main__':
    # command_listener_thread = threading.Thread(target=command_listener, args=(sys.argv[3],))
    # command_listener_thread.daemon = True
    # command_listener_thread.start()

    command_listener(sys.argv[3])

    app = App(
        sys.argv[1],
        sys.argv[2]
    )
