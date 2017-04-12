import sys
import time
import threading


class App:
    def __init__(self, ports, delimiter, stop_command):
        self.port_names = ports.split(delimiter)
        self.stop_command = stop_command
        self.command_listener()
        # self.command_listener_thread = threading.Thread(target=self.command_listener)
        # self.command_listener_thread = True
        # self.command_listener_thread.start()

    def command_listener(self):
        while True:
            command = sys.stdin.readline().rstrip()
            if command == self.stop_command:
                print(command)
                sys.exit(0)


if __name__ == '__main__':
    app = App(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
