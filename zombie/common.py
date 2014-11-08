# General

def reverse_dict(value):
    return {v: k for k, v in value.items()}


def distance_nested(obj1):
    
    def distance(obj2):
        return abs(obj1['x'] - obj2['x']) + abs(obj1['y'] - obj2['y'])
    
    return distance


def var_str(items):
    return ', '.join('%s: %s' % nv for nv in items)


def load_player_icons():
    from collections import OrderedDict
    
    from pyglet import resource
    
    filenames = resource._default_loader._index.keys()
    
    player_icons = OrderedDict()
    
    for index in range(256):
        filename = 'player-icon-%03d.png' % index
        if filename in filenames:
            player_icons[index] = filename
    
    return player_icons


def switch_layer(scene, layer_cls):
    scene.get_children()[0].switch_to(scene.layer_map[layer_cls])


# Paths

def map_file_path(map_name):
    from os.path import join
    from zombie.constants import MAP_DIR_PATH
    
    return join(MAP_DIR_PATH, '%s.tmx' % map_name)


# Input: Client

def get_keys():
    from inspect import getmembers
    
    from pyglet.window import key
    
    return dict(getmembers(key, lambda x: isinstance(x, int)))

def get_buttons():
    from inspect import getmembers
    
    from pyglet.window import mouse
    
    return dict(getmembers(mouse, lambda x: isinstance(x, int)))


# Networking

def client_data_debug(data):
    from zombie.constants import CLIENT_CODES_REVERSE_LOOKUP
    
    action = CLIENT_CODES_REVERSE_LOOKUP[data[1]]
    if action == 'connect':
        
        host_stop = 7 + data[6]
        contents = var_str((
            ('icon', data[2]),
            ('red', data[3]),
            ('green', data[4]),
            ('blue', data[5]),
            ('host length', data[6]),
            ('host', unpack_host(data[7:host_stop])),
            ('nickname', data[host_stop:]),
        ))
    elif action == 'cursor_motion':
        contents = '%d,%d' % tuple(data[2:])
    elif action in ('equip_slot', 'equip_item'):
        contents = data[2]
    else:
        contents = ''
    
    return 'Client %d: %s: %s' % (data[0], action, contents)


def server_data_debug(data):
    from zombie.constants import SERVER_CODES_REVERSE_LOOKUP
    
    action = SERVER_CODES_REVERSE_LOOKUP[data[0]]
    if action == 'update':
        # TODO: Parse update data.
        content = ''
    else:
        content = ''
    return '%s: %s' % (action, content)


# Networking: General

def validate_port(port):
    try:
        port = int(port)
    except ValueError:
        return None
    
    if 1 <= port <= 65535:
        return port
    else:
        return None


def udp_socket():
    import socket
    
    return socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP


def validate_ip_hostname(value):
    '''
    Validates an ip or hostname.
    '''
    import re
    
    from zombie.constants import REGEXS
    
    if isinstance(value, str):
        value = value.encode('ascii')
    
    if re.match(REGEXS['ip'], value) or re.match(REGEXS['hostname'], value):
        return value
    else:
        return None


def pack_host(ip, port):
    from re import match
    from struct import pack
    from zombie.constants import REGEXS
    
    if isinstance(ip, str):
        ip = ip.encode('ascii')
    
    port = pack(b'H', port)
    if match(REGEXS['ip'], ip):
        # IPv4 address
        return b'i' + bytes(int(x) for x in ip.split('.')) + port
    else:
        # hostname
        return b'h' + ip + b':' + port


def unpack_ip(*packed_ip):
    return '.'.join(str(x) for x in packed_ip)


def pack_ip(unpacked_ip):
    return bytes(int(x) for x in ip.split('.'))


def unpack_host(packed):
    from struct import unpack
    
    if packed[0] == ord(b'i'):
        parts = unpack(b'BBBBH', packed[1:])
        return '.'.join(parts[:-1]), parts[-1]
    elif packed[0] == ord(b'h'):
        hostname, port = packed[1:].split(b':')
        return hostname, unpack(b'H', port)[0]
    else:
        raise ValueError('Unknown host: %s' % packed)

'''
# Unused: Rotation

# TODO: opt: speed up var lookup
GRAD = pi / 2

def forward(rotation):
    return -sin(rotation * GRAD), -cos(rotation * GRAD)

def backward(rotation):
    return +sin(rotation * GRAD), +cos(rotation * GRAD)

def right(rotation):
    return +cos(rotation * GRAD), -sin(rotation * GRAD)

def left(rotation):
    return -cos(rotation * GRAD), +sin(rotation * GRAD)
'''