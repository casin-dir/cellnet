# up virtual ports on mac
# $ socat -d -d pty,raw,echo=0 pty,raw,echo=0

# PORT_PREFIX = 'COM'
PORT_PREFIX = '/dev/ttys00'

CLIENTS_PORTS = [
    ['4'],
    ['5']
]