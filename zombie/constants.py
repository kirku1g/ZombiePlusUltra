from collections import OrderedDict
from os.path import abspath, dirname, join
from string import ascii_letters, digits

from zombie.common import reverse_dict


VERSION = 'pre-alpha'

# Paths

ZOMBIE_DIR_PATH = abspath(dirname(__file__))
CONFIG_FILE_PATH = join(ZOMBIE_DIR_PATH, 'config.ini')
RESOURCES_DIR_PATH = join(ZOMBIE_DIR_PATH, 'resources')
FONT_DIR_PATH = join(RESOURCES_DIR_PATH, 'fonts')
MAP_DIR_PATH = join(RESOURCES_DIR_PATH, 'map')


# Colors

COLORS = OrderedDict((
    ('red', (204, 0, 0)),
    ('orange', (204, 102, 0)),
    ('yellow', (204, 204, 0)),
    ('green', (102, 0, 0)),
    ('teal', (0, 204, 204)),
    ('blue', (0, 102, 204)),
    ('violet', (102, 0, 204)),
    ('purple', (204, 0, 204)),
    ('pink', (204, 0, 102)),
    ('black', (0, 0, 0)),
    ('gray', (96, 96, 96)),
    ('white', (255, 255, 255)),
))


# Config


DEFAULT_CONFIG = {
    'player': {
        'nickname': b'Player',
    },
    'network': {
        'ip': b'localhost',
        'port': 9999,
    },
    'input': {
        'key': {
            'forwards': 'W',
            'backwards': 'S',
            'strafe_left': 'A',
            'strafe_right': 'D',
            
            'run': 'MOD_SHIFT',
            
            'throw_equipped_item': 'E',
            'drop_equipped_item': 'F',
            
            'turn_around': 'Q',
            
            'inventory': 'TAB',
            
            'equip_slot_1': 'NUM_1',
            'equip_slot_2': 'NUM_2',
            'equip_slot_3': 'NUM_3',
            'equip_slot_4': 'NUM_4',
            'equip_slot_5': 'NUM_5',
            'equip_slot_6': 'NUM_6',
            'equip_slot_7': 'NUM_7',
            'equip_slot_8': 'NUM_8',
            'equip_slot_9': 'NUM_9',
            
            'quit': 'ESCAPE',
        },
        'mouse': {
            'attack': 'LEFT',
            'use': 'RIGHT',
        },
    },
    'video': {
        'resolution': (640, 480),
    },
}


# Networking

# Networking: Client

SERVER_CODES = {
    'connected': 0,
    'update': 10,
    
    'player_connected': 20,
    'player_disconnected': 21,
    'player_kicked': 22,
    
    'start_attack': 30,
    'start_use': 31,
    
    'end_attack': 40,
    'end_use': 41,
    
    'kicked': 255,
}


# 0-255
CLIENT_CODES = {
    'connect_ip': 0,
    'connect_hostname': 1,
    'disconnect': 2,
    'received': 5,
    'chat_message': 6,
    
    'turn_around': 10,
    
    'start_move_forwards': 20,
    'start_move_backwards': 21,
    'start_strafe_left': 22,
    'start_strafe_right': 23,
    'start_run': 24,
    
    'start_attack': 25,
    'start_use': 26,
    
    'end_move_forwards': 30,
    'end_move_backwards': 31,
    'end_strafe_left': 32,
    'end_strafe_right': 33,
    'end_run': 34,
    
    'end_attack': 35,
    'end_use': 36,
    
    'cursor_motion': 40,
    
    'equip_slot_1': 51,
    'equip_slot_2': 52,
    'equip_slot_3': 53,
    'equip_slot_4': 54,
    'equip_slot_5': 55,
    'equip_slot_6': 56,
    'equip_slot_7': 57,
    'equip_slot_8': 58,
    'equip_slot_9': 59,
    
    'equip_clothes_torso': 60,
    'equip_clothes_legs': 61,
    'equip_clothes_hands': 62,
    'equip_clothes_feet': 63,
    'equip_clothes_head': 64,
    
    'throw_equipped_item': 70,
    'drop_equipped_item': 71,
    'drop_inventory_item': 72,
    'inventory_switch': 73,
}

# OPT: Create bytes in advance for concatenation.
CLIENT_CODES_BYTES = {k: bytes((v,)) for k, v in CLIENT_CODES.items()}

EQUIP_SLOT_CODES = {
    CLIENT_CODES['equip_slot_1']: 1,
    CLIENT_CODES['equip_slot_2']: 2,
    CLIENT_CODES['equip_slot_3']: 3,
    CLIENT_CODES['equip_slot_4']: 4,
    CLIENT_CODES['equip_slot_5']: 5,
    CLIENT_CODES['equip_slot_6']: 6,
    CLIENT_CODES['equip_slot_7']: 7,
    CLIENT_CODES['equip_slot_8']: 8,
    CLIENT_CODES['equip_slot_9']: 9,
}

SERVER_CODES_REVERSE_LOOKUP = reverse_dict(SERVER_CODES)
CLIENT_CODES_REVERSE_LOOKUP = reverse_dict(CLIENT_CODES)


# Validation

# Networking

VALID_IP_HOSTNAME_CHARS = set(ascii_letters) | set(digits) | {'-', '.'}


# ip and hostname regexes sourced from http://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
REGEXS = {
    'ip': b"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
    'hostname': b"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$",
}