import sys
import config_main
import config_connections
import os
import subprocess


class CellNet:
    def __init__(self, cfg_main, cfg_connections):
        self.cfg_main = cfg_main
        self.cfg_connections = cfg_connections
        self.clients_ports = []
        self.clients = {}
        self.count_active = 0
        for name, ports in enumerate(self.cfg_connections.CLIENTS_PORTS):
            client_ports = list(map(lambda x: self.cfg_connections.PORT_PREFIX + x, ports))
            client = {
                'name': str(name),
                'online': False,
                'ports': client_ports,
                'process': None
            }
            self.clients[str(name)] = client

        self.command_manager()

    def command_manager(self):
        print('Welcome to CellNet!')
        while True:
            command = input('> ').strip()
            if command == self.cfg_main.COMMANDS['start']:
                self.start()
            elif command == self.cfg_main.COMMANDS['stop']:
                self.stop()
            elif command == self.cfg_main.COMMANDS['restart']:
                self.restart()
            elif command == self.cfg_main.COMMANDS['status']:
                self.print_status()
            elif command == self.cfg_main.COMMANDS['shutdown client']:
                client_name = input('client to shutdown > ')
                self.shutdown_client(client_name)
            elif command == self.cfg_main.COMMANDS['run client']:
                client_name = input('client to run > ')
                self.run_client(client_name)
            elif command == self.cfg_main.COMMANDS['exit']:
                print('Goodbye!')
                self.stop()
                sys.exit(0)
            elif command == self.cfg_main.COMMANDS['help']:
                self.print_help()
            elif command == '':
                pass
            else:
                print('ERROR: Unsupported command.')
                print('Use "{0}"'.format(self.cfg_main.COMMANDS['help']))

    def start(self):
        if self.count_active > 0:
            print('ERROR: Network has already been started.')
            return
        for client_name in self.clients:
            self.run_client(client_name)

    def stop(self):
        if not self.count_active > 0:
            print('ERROR: Network has already been stopped.')
            return

        for client_name in self.clients:
            self.shutdown_client(client_name)

    def restart(self):
        self.stop()
        self.start()

    def print_status(self):
        print('\nNetwork status: {0}'.format('Active' if self.count_active > 0 else 'Inactive'))
        print('Count active clients: {0}'.format(str(self.count_active)))
        print('Clients:')
        for client_name in self.clients:
            client = self.clients[client_name]
            print('Client "{0}", status: {1}, ports: {2}'.format(
                client['name'],
                'Online' if client['online'] else 'Offline',
                client['ports']
            ))
        print('\n')

    def shutdown_client(self, name):
        client = self.clients.get(name)
        if client is None:
            print('There is no such client like "{0}"'.format(name))
            return

        if not client['online']:
            print('Client has already been offline')
            return

        print('Shutting down client "{0}" ...'.format(name))
        client['process'].stdin.write(
            self.cfg_main.STOP_PROCESS_COMMAND.encode('utf-8') + b'\n'
        )
        client['process'].stdin.close()
        # client['process'] = None
        client['online'] = False
        self.count_active -= 1

    def run_client(self, name):
        client = self.clients.get(name)
        if client is None:
            print('There is no such client like "{0}"'.format(name))
            return

        if client['online']:
            print('Client has already been online')
            return

        print('Starting client "{0}" ...'.format(name))
        path = os.path.relpath(
            self.cfg_main.PROCESS_FILE_PATH,
            start=os.getcwd()
        )
        ports = self.cfg_main.ARG_DELIMITER.join(client['ports'])
        command = [
            sys.executable,
            path,
            ports,
            self.cfg_main.ARG_DELIMITER,
            self.cfg_main.STOP_PROCESS_COMMAND
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        client['process'] = pipe
        client['online'] = True
        self.count_active += 1

    def print_help(self):
        for command in self.cfg_main.COMMANDS:
            print(self.cfg_main.COMMANDS[command])


if __name__ == '__main__':
    network = CellNet(config_main, config_connections)


