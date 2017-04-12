import sys
import time
import threading


def command_listener(stop_command):
    while True:
        command = sys.stdin.readline().rstrip()
        if command == stop_command:
            sys.exit(0)


class App:
    def __init__(self, ports, delimiter):
        self.port_names = ports.split(delimiter)

    def run(self):
        while True:
            print('Running app')
            time.sleep(1)


if __name__ == '__main__':
    app = App(
        sys.argv[1],
        sys.argv[2]
    )
    app_thread = threading.Thread(target=app.run, args=())
    app_thread.daemon = True
    app_thread.start()
    command_listener(sys.argv[3])


