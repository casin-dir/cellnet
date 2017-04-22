import sys
import time
import threading
from GUI.gui import start_gui
from Connector.connector import Connector


def command_listener(stop_command):
    while True:
        command = sys.stdin.readline().rstrip()
        if command == stop_command:
            sys.exit(0)


class App:
    def __init__(self, ports, delimiter):
        self.port_names = ports.split(delimiter)

    def port_status(self,status):
        print("portstatus " + str(status))

    def run(self):
        print(self.port_names[0])
        res = start_gui()
        con = Connector(self.port_names[0], res[1].myfunc, self.port_status)
        res[1].add_button_listener(con.send)
        con.open()
        sys.exit(res[0].exec_())





if __name__ == '__main__':
    app = App(
        sys.argv[1],
        sys.argv[2]
    )
    app_thread = threading.Thread(target=app.run, args=())
    app_thread.daemon = True
    app_thread.start()
    command_listener(sys.argv[3])


