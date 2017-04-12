import sys
import config_main
import config_connections
from client import app


class CellNet:
    def __init__(self, cfg_main, cfg_connections):
        self.cfg_main = cfg_main
        self.cfg_connections = cfg_connections
        self.clients_ports = []
        self.clients = {}
        self.active = False
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
                sys.exit(0)
            elif command == self.cfg_main.COMMANDS['help']:
                self.print_help()
            elif command == '':
                pass
            else:
                print('ERROR: Unsupported command.')
                print('Use "{0}"'.format(self.cfg_main.COMMANDS['help']))

    def start(self):
        if self.active:
            print('ERROR: Network has already been started.')
            return

        print('Starting...')

    def stop(self):
        if not self.active:
            print('ERROR: Network has already been stopped.')
            return

        print('Stopping...')

    def restart(self):
        self.stop()
        self.start()

    def print_status(self):
        print('\nNetwork status: {0}'.format('Active' if self.active else 'Inactive'))
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

        print('Shutting down client...')

    def run_client(self, name):
        client = self.clients.get(name)
        if client is None:
            print('There is no such client like "{0}"'.format(name))
            return

        if client['online']:
            print('Client has already been online')
            return

        print('Running client...')

    def print_help(self):
        for command in self.cfg_main.COMMANDS:
            print(self.cfg_main.COMMANDS[command])







# def command_manager():
#     while True:
#         command = input('> ')
#         if command == 'stop':
#             sys.exit(0)
#         elif command == 'clients':
#             print('Clients will be here ...')
#         else:
#             print('ERROR: Unsupported command!')


if __name__ == '__main__':
    # print('Wellcome to CellNet!')
    #
    # port_prefix = config_connections.PORT_PREFIX
    # clients_ports = config_connections.CLIENTS_PORTS
    # arg_delimiter = config_main.ARG_DELIMITER
    #
    # for client_num, client_ports in enumerate(clients_ports):
    #
    #     def add_prefix(name):
    #         return port_prefix + name
    #
    #     user_message = '> Starting client {0} with ports: '.format(client_num)
    #     user_message += config_main.MESSAGE_DELIMITER.join(map(add_prefix, client_ports))
    #     print(user_message)
    #
    #     arg_ports = config_main.ARG_DELIMITER.join(map(add_prefix, client_ports))
    #     # print(arg_ports)
    #
    # command_manager()

    network = CellNet(
        config_main,
        config_connections
    )
    # network.start()


