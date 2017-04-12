import sys
import time
import threading
from GUI.gui import start_gui


def command_listener(stop_command):
    while True:
        command = sys.stdin.readline().rstrip()
        if command == stop_command:
            sys.exit(0)


class App:
    def __init__(self, ports, delimiter):
        self.port_names = ports.split(delimiter)

    def run(self):
       start_gui()


if __name__ == '__main__':
    app = App(
        sys.argv[1],
        sys.argv[2]
    )
    app_thread = threading.Thread(target=app.run, args=())
    app_thread.daemon = True
    app_thread.start()
    command_listener(sys.argv[3])


