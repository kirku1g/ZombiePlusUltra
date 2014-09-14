# General

def reverse_dict(value):
    return {v: k for k, v in value.items()}


def distance_nested(obj1):
    
    def distance(obj2):
        return abs(obj1['x'] - obj2['x']) + abs(obj1['y'] - obj2['y'])
    
    return distance


# Networking

# Networking: Client


SERVER_CODES = {
    'connected': 0,
    'update': 10,
    'kicked': 255,
}


# 0-255
CLIENT_CODES = {
    'connect': 0,
    'disconnect': 1,
    'received': 5, 
    
    'start_move_forwards': 20,
    'start_move_backwards': 21,
    'start_strafe_left': 22,
    'start_strafe_right': 23,
    
    'start_attack': 24,
    'start_use': 25,
    
    'end_move_forwards': 30,
    'end_move_backwards': 31,
    'end_strafe_left': 32,
    'end_strafe_right': 33,
    
    'end_attack': 34,
    'end_use': 35,
    
    'cursor_motion': 40,
    
    'equip_slot': 50,
    'equip_item': 51,
}

SERVER_CODES_REVERSE_LOOKUP = reverse_dict(SERVER_CODES)
CLIENT_CODES_REVERSE_LOOKUP = reverse_dict(CLIENT_CODES)


def client_data_debug(data):
    action = CLIENT_CODES_REVERSE_LOOKUP[data[1]]
    if action == 'connect':
        ip, port = unpack_host(data[2:])
        contents = b':'.join((ip, str(port).encode('ascii')))
    elif action == 'cursor_motion':
        contents = '%d,%d' % tuple(data[2:])
    elif action in ('equip_slot', 'equip_item'):
        contents = data[2]
    else:
        contents = b''
    
    return 'Client %d: %s: %s' % (data[0], action, contents)


def server_data_debug(data):
    action = SERVER_CODES_REVERSE_LOOKUP[data[0]]
    if action == 'update':
        # TODO: Parse update data.
        content = ''
    else:
        content = ''
    return '%s: %s' % (action, content)


# Networking: General

def udp_socket():
    import socket
    
    return socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP


def pack_host(ip, port):
    import re, struct
    
    port = struct.pack(b'H', port)
    if re.match(b'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ip):
        # IPv4 address
        return b'i' + b'.'.join(struct.pack('B', int(x)) for x in ip.split('.')) + port
        #return struct.pack()
    else:
        # hostname
        return b'h' + ip + b':' + port


def unpack_host(packed):
    import struct
    
    if packed[0] == ord(b'i'):
        parts = struct.unpack(b'BBBBH', packed[1:])
        return '.'.join(parts[:-1]), parts[-1]
    elif packed[0] == ord(b'h'):
        hostname, port = packed[1:].split(b':')
        return hostname, struct.unpack(b'H', port)[0]
    else:
        raise ValueError('Unknown host: %s' % packed)