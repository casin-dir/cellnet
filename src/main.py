from connector import Connector


if __name__ == '__main__':
    print('Welcome CellNet!')
    connector = Connector()
    connector.connect()
    connector.send_data('Hello Casin!')
    connector.disconnect()

