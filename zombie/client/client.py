from socketserver import BaseRequestHandler, UDPServer

from cocos.layer import Layer
from cocos.menu import Menu, MenuItem


class Config(object):
    '''
    Config class which validates config values.
    '''
    
    def __init__(self, config_file_path=None):
        from configobj import ConfigObj
        
        if not config_file_path:
            from zombie.constants import CONFIG_FILE_PATH
            config_file_path = CONFIG_FILE_PATH
        
        self.config = ConfigObj(open(config_file_path, 'rb'))
        self.config.filename = config_file_path
        
        self.validate_config(self.config)
    
    @classmethod
    def validate_config(cls, config):
        cls.validate_player(config)
        cls.validate_network(config)
        cls.validate_input(config)
        
        config.write()
    
    @staticmethod
    def validate_player(config):
        from random import choice
        
        from zombie.common import load_player_icons
        from zombie.constants import COLORS, DEFAULT_CONFIG, VALID_IP_HOSTNAME_CHARS
        
        section_name = 'player'
        default = DEFAULT_CONFIG[section_name]
        
        # Section: player
        if section_name not in config:
            config[section_name] = {}
        
        player = config[section_name]
        
        # player/nickname
        if 'nickname' in player:
            nickname = player['nickname']
            if isinstance(nickname, str):
                nickname = nickname.encode('ascii')
            for nickname_stop_index, char in enumerate(nickname, start=1):
                if nickname_stop_index == 10:
                    break
                elif char not in VALID_IP_HOSTNAME_CHARS:
                    break
            
            player['nickname'] = nickname[:nickname_stop_index]
        
        else:
            player['nickname'] = default['nickname']
        
        # player/icon
        player_icons = load_player_icons()
        
        if 'icon' not in player or int(player['icon']) not in player_icons:
            player['icon'] = next(iter(player_icons.keys()))
        else:
            player['icon'] = int(player['icon'])
        
        # player/color
        
        #random_light = lambda: randint(0, 255)
        #random_color = lambda: (random_light(), random_light(), random_light())
        color_options = tuple(COLORS.values())
        if 'color' not in player or player['color'] not in color_options:
            #color = player['color']
            #if not isinstance(color, tuple) or not len(color) == 3 or not all(0 <= int(x) <= 255 for x in color):
            player['color'] = choice(color_options)
    
    @staticmethod
    def validate_network(config):
        from zombie.common import validate_ip_hostname, validate_port
        from zombie.constants import DEFAULT_CONFIG
        
        section_name = 'network'
        default = DEFAULT_CONFIG[section_name]
        
        if section_name not in config:
            config[section_name] = default
            return
        
        network = config[section_name]
        
        if 'ip' not in network or not validate_ip_hostname(network['ip']):
            network['ip'] = DEFAULT_IP
        
        if 'port' not in network or not validate_port(network['port']):
            network['port'] = DEFAULT_PORT
    
    @classmethod
    def validate_input(cls, config):
        from zombie.common import get_buttons, get_keys
        from zombie.constants import DEFAULT_CONFIG
        
        section_name = 'input'
        default = DEFAULT_CONFIG[section_name]
        
        if section_name not in config:
            config[section_name] = default
            return
        
        input = config[section_name]
        
        # input/key
        cls.validate_input_type(input, 'key', default, get_keys)
        
        # input/mouse
        cls.validate_input_type(input, 'mouse', default, get_buttons)
    
    @staticmethod
    def validate_input_type(input, section_name, default, input_values_func):
        default_section = default[section_name]
        
        if section_name not in input:
            # Configure with defaults.
            input[section_name] = default_section
            return
        
        input_values = input_values_func()
        
        section = input[section_name]
        
        for action in default_section:
            if action not in section or section[action] not in input_values:
                section[action] = default_section[action]


class TitleScreen(Layer):

    is_event_handler = True
    
    def __init__(self, scene):
        from cocos.text import Label
        from cocos.actions import FadeIn
        from zombie.constants import VERSION
        
        super(TitleScreen, self).__init__()
        
        self.scene = scene
        
        title_label = Label(
            'Zombie+ Ultra',
            font_name='Extrude',
            font_size=48,
            anchor_x='center',
            anchor_y='center',
        )
        
        version_label = Label(
            VERSION,
            font_name='TinyUnicode',
            font_size=32,
            anchor_x='center',
        )
        
        title_label.position = 320, 240
        version_label.position = 320, (240 / 4) * 3
        title_label.do(FadeIn(duration=10))
        version_label.do(FadeIn(duration=10))
        
        self.add(title_label)
        self.add(version_label)
    
    def on_key_press(self, key, modifiers):
        from pyglet.window.key import ENTER
        
        from zombie.common import switch_layer
        
        if key == ENTER:
            switch_layer(self.scene, MainMenu)
    
    def on_quit(self):
        from zombie.common import switch_layer
        
        switch_layer(self.scene, QuitScreen)


class MessageScreen(Layer):
    
    is_event_handler = True
    
    def __init__(self, scene, message, next_layer=None):
        from cocos.text import Label
        
        super(MessageScreen, self).__init__()
        
        self.scene = scene
        self.next_layer = next_layer
        
        label = Label(
            message,
            font_name='TinyUnicode',
            font_size=32,
            anchor_x='center',
            anchor_y='center',
        )
        
        label.position = 320, 240
        self.add(label)
    
    def on_key_press(self, *args):
        if self.next_layer:
            from zombie.common import switch_layer
            switch_layer(self.scene, self.next_layer)
        else:
            from sys import exit
            exit(0)


class ConnectScreen(MessageScreen):
    
    def __init__(self, scene, connect, is_connected, **kwargs):
        super(ConnectScreen, self).__init__(scene, 'Connecting...', **kwargs)
        
        self._connect = connect
        self._is_connected = is_connected
    
    def connect(self, server_ip, server_port):
        from time import time
        self._connect(server_ip, server_port)
        
        self.connect_start_time = time()
        self.schedule_interval(self.is_connected, 0.5)
    
    def is_connected(self, delta):
        from zombie.common import switch_layer
        
        connected = self._is_connected()
        
        if connected:
            
            switch_layer(self.scene, Client)
        
        from time import time
        
        if (time() - self.connect_start_time) > 10:
            self.unschedule(self.is_connected)
            switch_layer(self.scene, ConnectFailedScreen)
    
    def on_key_press(self, key, modifiers):
        from pyglet.window.key import ESCAPE
        if key == ESCAPE:
            self.unschedule(self.is_connected)
            super(ConnectScreen, self).on_key_press(key, modifiers)


class ConnectFailedScreen(MessageScreen):
    def __init__(self, scene):
        super(ConnectFailedScreen, self).__init__(scene, 'Connection Failed!', next_layer=JoinGameMenu)


class QuitScreen(MessageScreen):
    def __init__(self, scene, **kwargs):
        super(QuitScreen, self).__init__(scene, 'Thanks for playing!', **kwargs)


class KickScreen(MessageScreen):
    def __init__(self, scene, **kwargs):
        super(KickScreen, self).__init__(scene, 'You have been kicked!', **kwargs)


class ZombieMenu(Menu):
    '''
    Menu superclass setting up the theme and providing access to the scene.
    '''
    
    def __init__(self, scene, title,
                 title_font_name='Extrude',
                 title_font_size=48,
                 title_color=(204,164,164,255),
                 item_font_name='TinyUnicode',
                 item_font_size=36,
                 item_color=(128,128,128,255),
                 selected_font_name='TinyUnicode',
                 selected_font_size=42,
                 selected_color=(255,255,255,255)):
        super(ZombieMenu, self).__init__(title)
        
        self.scene = scene
        
        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = title_font_name
        self.font_title['font_size'] = title_font_size
        self.font_title['color'] = title_color

        self.font_item['font_name'] = item_font_name
        self.font_item['font_size'] = item_font_size
        self.font_item['color'] = item_color
        
        self.font_item_selected['font_name'] = selected_font_name
        self.font_item_selected['font_size'] = selected_font_size
        self.font_item_selected['color'] = selected_color
    
    def create_animated_menu(self, items):
        from cocos.menu import shake, shake_back
        
        self.create_menu(items, selected_effect=shake(), unselected_effect=shake_back())
    
    def create_image_menu(self, items):
        from math import floor
        
        from cocos.menu import ImageMenuItem
        
        menu_items = []
        item_positions = []
        for index, item in enumerate(items):
            menu_items.append(ImageMenuItem(item, self.new_game))
            #print(((index % self.columns) * self.item_width) + (self.item_width / 2), height - ((floor(index / self.rows) + 1) * self.item_height) - (self.item_height / 2))
            item_positions.append((
                ((index % self.columns) * self.item_width) + (self.item_width / 2),
                height - ((floor(index / self.columns) + 1) * self.item_height) - (self.item_height / 2),
            ))
        
        self.create_menu(menu_items)


class SettingsMenu(ZombieMenu):
    def __init__(self, config, scene):
        from zombie.constants import COLORS
        
        from cocos.director import director
        from cocos.menu import ColorMenuItem, EntryMenuItem, ImageMenuItem, MenuItem, MultipleMenuItem
        
        super(SettingsMenu, self).__init__(scene, 'Settings')
        
        self.nickname = EntryMenuItem('Nickname:', self.validate_nickname, config['player']['nickname'], max_length=10)
        color_options = tuple(COLORS.values())
        color_index = color_options.index(config['player']['color'])
        self.color = ColorMenuItem('Color: ', self.select_color, color_options, default_item=color_index)
        self.player_icon = ImageMenuItem('player-icon-001.png', self.select_player_icon)
        # XXX: MultipleMenuItems requires a space?
        
        self.resolutions = [(320, 240), (640, 480), (800, 600)]
        resolution_index = self.resolutions.index(director.get_window_size())
        resolution_options = ['%dx%d' % (w, h) for w, h in self.resolutions]
        self.resolution = MultipleMenuItem('Resolution: ', self.change_resolution, resolution_options, default_item=resolution_index)
        # TODO: Handle unknown resolution.
        apply = MenuItem('Apply', self.apply)
        cancel = MenuItem('Cancel', self.cancel)
        
        items = (self.nickname, self.color, self.player_icon, self.resolution, apply, cancel)
        
        self.create_animated_menu(items)
        
        # Handle escape.
        self.on_quit = self.cancel
        
        self.config = config
    
    def change_resolution(self, value):
        from cocos.director import director
        
        resolution = self.resolutions[value]
        director.window.set_size(*resolution)
        self.config['video']['resolution'] = resolution
    
    def select_color(self, value):
        pass
    
    def select_player_icon(self):
        print('select_face')
    
    def validate_nickname(self, value):
        if not value:
            return
        
        from zombie.constants import VALID_IP_HOSTNAME_CHARS
        
        if value[-1] not in VALID_IP_HOSTNAME_CHARS:
            self.nickname._value.pop()
        
        self.config['player']['nickname'] = self.nickname.value

    def apply(self):
        from zombie.common import switch_layer
        # TODO: validate settings
        self.config.write()
        switch_layer(self.scene, MainMenu)
        
    def cancel(self):
        from zombie.common import switch_layer
        
        switch_layer(self.scene, MainMenu)


class JoinGameMenu(ZombieMenu):
    def __init__(self, config, scene, connect_screen):
        from cocos.menu import EntryMenuItem, MenuItem
        
        super(JoinGameMenu, self).__init__(scene, 'Join Game')
        
        self.ip = EntryMenuItem('IP/Hostname:', self.validate_ip, config['network']['ip'], max_length=256)
        self.port = EntryMenuItem('Port:', self.validate_port, str(config['network']['port']), max_length=5)
        connect = MenuItem('Connect', self.connect)
        cancel = MenuItem('Cancel', self.cancel)
        items = (self.ip, self.port, connect, cancel)
        self.create_animated_menu(items)
        
        # Handle escape
        self.on_quit = self.cancel
        
        self.config = config
        self.connect_screen = connect_screen
    
    def validate_ip(self, value):
        '''
        Validate last entered ip/hostname character is correct.
        '''
        if not value:
            return
        
        from zombie.constants import VALID_IP_HOSTNAME_CHARS
        
        if not self.ip._value[-1] in VALID_IP_HOSTNAME_CHARS:
            self.ip._value.pop()
        
        self.config['network']['ip'] = self.ip.value
    
    def validate_port(self, value):
        '''
        Validate port number.
        '''
        if not value:
            return
        
        from zombie.common import validate_port
        
        if not validate_port(value):
            self.port._value.pop()
        
        self.config['network']['port'] = self.port.value
    
    def connect(self):
        from zombie.common import validate_ip_hostname, validate_port
        
        ip = validate_ip_hostname(self.ip.value.encode('ascii'))
        
        if not ip:
            # TODO: error message
            return
        
        port = validate_port(self.port.value)
        
        if not port:
            #TODO: error message
            return
        
        from zombie.common import switch_layer
        ## TODO: Switch to client layer.
        #print('Connecting to', ip, port)
        self.connect_screen.connect(ip, port)
        switch_layer(self.scene, ConnectScreen)
    
    def cancel(self):
        '''
        Switches back to the MainMenu.
        '''
        from zombie.common import switch_layer
        
        switch_layer(self.scene, MainMenu)


class MainMenu(ZombieMenu):
    def __init__(self, config, scene):
        from cocos.menu import MenuItem, shake, shake_back
        
        super(MainMenu, self).__init__(scene, 'Zombie+ Ultra')
        
        self.config = config

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = [
            MenuItem('Join Game', self.join_game),
            MenuItem('Settings', self.settings),
            MenuItem('Quit', self.on_quit),
        ]

        #self.volumes = ['Mute','10','20','30','40','50','60','70','80','90','100']

        #items.append( MultipleMenuItem(
                        #'SFX volume: ', 
                        #self.on_sfx_volume,
                        #self.volumes,
                        #int(soundex.sound_vol * 10) )
                    #)
        #items.append( MultipleMenuItem(
                        #'Music volume: ', 
                        #self.on_music_volume,
                        #self.volumes,
                        #int(soundex.music_player.volume * 10) )
                    #)
        #items.append( ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        #items.append( MenuItem('Fullscreen', self.on_fullscreen) )
        #items.append( MenuItem('Back', self.on_quit) )
        self.create_animated_menu(items)
    
    def join_game(self):
        from zombie.common import switch_layer
        
        switch_layer(self.scene, JoinGameMenu)
    
    def settings(self):
        from zombie.common import switch_layer
        # TODO: Switch
        switch_layer(self.scene, SettingsMenu)
    
    def on_quit(self):
        from zombie.common import switch_layer
        
        self.config.write()
        switch_layer(self.scene, QuitScreen)


class Inventory(object):
    def __init__(self, max_weight=100):
        self.items = []
        self.weight = 0
        self.max_weight = max_weight
    
    def add(self, item):
        new_weight = self.weight + item.weight
        
        if new_weight > max_weight:
            return False
        
        self.weight = new_weight
        self.items.append(item)
        return True
    
    def remove(self, item):
        self.weight -= item.weight
        self.items.remove(item)


#class PlayerIconMenu(ZombieMenu):
    
    #def __init__(self, scene):
        #from zombie.common import load_player_icons

        #super(ZombieMenu, self).__init__(scene, 'Player Icon')
        
        #for index, value in enumerate(load_player_icons().values()):
            
            
    


class InventoryMenu(Menu):
    def __init__(self):
        from cocos.director import director
        from cocos.menu import ImageMenuItem, fixedPositionMenuLayout
        from math import floor
        from pyglet.resource import location
        
        super(InventoryMenu, self).__init__('Inventory')
        #self.select_sound = soundex.load('move.mp3')
        
        width, height = director.window.get_size()
        
        self.rows = 8
        self.columns = 10
        self.item_width = width / self.columns
        self.item_height = height / self.rows

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 32
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman'
        self.font_item['color'] = (128,128,128,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (255,255,255,255)
        self.font_item_selected['font_size'] = 32

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'
        
        items = ['colt_45.png'] * 70
        menu_items = []
        item_positions = []
        
        for index, item in enumerate(items):
            menu_items.append(ImageMenuItem(item, self.new_game))
            #print(((index % self.columns) * self.item_width) + (self.item_width / 2), height - ((floor(index / self.rows) + 1) * self.item_height) - (self.item_height / 2))
            item_positions.append((
                ((index % self.columns) * self.item_width) + (self.item_width / 2),
                height - ((floor(index / self.columns) + 1) * self.item_height) - (self.item_height / 2),
            ))
        
        #print(menu_items)
        #print(item_positions)
        
        

        #self.volumes = ['Mute','10','20','30','40','50','60','70','80','90','100']

        #items.append( MultipleMenuItem(
                        #'SFX volume: ', 
                        #self.on_sfx_volume,
                        #self.volumes,
                        #int(soundex.sound_vol * 10) )
                    #)
        #items.append( MultipleMenuItem(
                        #'Music volume: ', 
                        #self.on_music_volume,
                        #self.volumes,
                        #int(soundex.music_player.volume * 10) )
                    #)
        #items.append( ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        #items.append( MenuItem('Fullscreen', self.on_fullscreen) )
        #items.append( MenuItem('Back', self.on_quit) )
        self.create_menu(menu_items, shake(), shake_back(),
                         layout_strategy=fixedPositionMenuLayout(item_positions))
    
    def new_game(self):
        print('New Game')
    
    def quit(self):
        from sys import exit
        
        exit(0)


#class Client(Layer):
    
    #is_event_handler = True
    
    #def __init__(self, x, y):
        #self.objects = {}
        #self.inventory = []
        #self.x = x
        #self.y = y
        #self.rotation = rotation
        #self.inventory = Inventory()
        
        ## grad - used for rotated movement trigonometry
        #self.grad
    
    #def request(self):
        ## TODO: Send changes
        ## TODO: Make UDP request.
        ##data = simplejson.loads(request)
        #self.objects.update(data['objects_update'])
        #for object_id in data['object_delete_ids']:
            #del self.objects[object_id]
    
    #def on_key_press(self, key, modifiers):
        #movement = {
            #UP: forward,
            #DOWN: backward,
            #LEFT: left,
            #RIGHT: right,
        #}[key]
        #x_diff, y_diff = movement(self.rotation)
        
        #self.x = x_diff * self.speed
        
        #self.y = y_diff * self.speed

def setup_resources():
    from pyglet import font, resource
    
    from zombie.constants import RESOURCES_DIR_PATH, FONT_DIR_PATH
    
    # Need to override path as '.' entry causes problems.
    resource.path = [RESOURCES_DIR_PATH]
    resource.reindex()
    font.add_directory(RESOURCES_DIR_PATH)
    font.add_directory(FONT_DIR_PATH)


class ClientReceiver(UDPServer):
    def __init__(self, client, *args, **kwargs):
        super(ClientReceiver, self).__init__(*args, **kwargs)
        
        self.client = client


class ClientHandler(BaseRequestHandler):
    
    def handle(self):
        from zombie.constants import SERVER_CODES
        
        data = self.request[0]
        #socket = self.request[1]
        
        if data[0] == SERVER_CODES['update']:
            self.server.client.update(data)
        elif data[0] == SERVER_CODES['connected']:
            print('connected', data[1])
            self.server.client.sender.client_id = data[1]
        elif data[0] == SERVER_CODES['kicked']:
            self.server.client.quit()
        
        
        #if data[0] == ord(b'a'):
            #client_id = struct.unpack('xB', data)
            #self.server.client_id_callback(client_id)
        #socket = self.request[1]
        #print('client', data)


class ClientSender(object):
    def __init__(self, client, receive_ip, receive_port, client_id=0):
        from threading import Thread
        from zombie.common import udp_socket
        
        self.client = client
        
        self.socket = udp_socket()
        
        if isinstance(receive_ip, str):
            receive_ip = receive_ip.encode('ascii')
        self.receive_ip = receive_ip
        self.receive_port = receive_port
        
        self.client_id = client_id
    
    @property
    def client_id(self):
        return self._client_id[0]
    
    @client_id.setter
    def client_id(self, value):
        self._client_id = bytes((value,))
    
    def send(self, data):
        from zombie.common import client_data_debug
        print(data)
        print(client_data_debug(self._client_id + data))
        
        self.socket.sendto(self._client_id + data, (self.server_ip, self.server_port))
    
    def connect(self, server_ip, server_port):
        from zombie.constants import CLIENT_CODES, REGEXS
        from zombie.common import pack_ip
        from re import match
        from struct import pack
        
        self.server_ip = server_ip
        self.server_port = server_port
        
        if match(REGEXS['ip'], self.receive_ip):
            network_code = 'connect_ip'
            ip_hostname = pack_ip(self.receive_ip)
        else:
            network_code = 'connect_hostname'
            ip_hostname = self.receive_ip
        
        #host = pack_host(self.receive_ip, self.receive_port)
        
        color = self.client.config['player']['color']
        
        nickname = self.client.config['player']['nickname']
        
        if isinstance(nickname, str):
            nickname = nickname.encode('ascii')
        
        self.send(
            bytes((
                CLIENT_CODES[network_code],
                self.client.config['player']['icon'],
                color[0],
                color[1],
                color[2],
                len(nickname))) +
            nickname +
            ip_hostname + 
            pack('H', self.receive_port)
        )
    
    def disconnect(self):
        if not self._client_id:
            raise ValueError('Cannot disconnect as client_id is not set.')
        self.send(data)



class CharacterBody(Layer):
    
    def __init__(self, skin_red, skin_green, skin_blue, clothes_red, clothes_green, clothes_blue):
        
        super(CharacterBody, self).__init__()
        
        from cocos.layer.util_layers import ColorLayer
        #red, green, blue = self.config['player']['color']
        body_width = 48
        body_height = 16
        body = ColorLayer(clothes_red, clothes_green, clothes_blue, 255, body_width, body_height)
        half_body_width = body_width / 2
        half_body_height = body_height / 2
        body.position = -half_body_width, -half_body_height
        
        self.add(body)
        
        head_size = 18
        half_head_size = head_size / 2
        head = ColorLayer(skin_red, skin_green, skin_blue, 255, head_size, head_size)
        head.position = -half_head_size, -half_head_size
        
        self.body_width = body_width
        self.body_height = body_height
        self.head_size = head_size
        
        self.skin_red = skin_red
        self.skin_green = skin_green
        self.skin_blue = skin_blue
        
        self.clothes_red = clothes_red
        self.clothes_green = clothes_green
        self.clothes_blue = clothes_blue
        
        self.add(head)

        self.anchor = 0, 0


class Player(CharacterBody):
    
    def __init__(self, *args):
        from cocos.layer.util_layers import ColorLayer
        super(Player, self).__init__(*args)
        
        hand_size = 10
        half_hand_size = hand_size / 2
        
        left_hand = ColorLayer(self.skin_red, self.skin_green, self.skin_blue, 255, hand_size, hand_size)
        left_hand.position = -self.body_width/2, self.head_size/2
        
        right_hand = ColorLayer(self.skin_red, self.skin_green, self.skin_blue, 255, hand_size, hand_size)
        right_hand.position = self.body_width/2 - hand_size, self.head_size/2
        
        self.add(left_hand)
        self.add(right_hand)


class Zombie(CharacterBody):
    
    def __init__(self, *args):
        from cocos.layer.util_layers import ColorLayer
        
        super(Zombie, self).__init__(0, 255, 0, *args)
        arm_width = 10
        arm_height = 2 * arm_width
        
        left_arm = ColorLayer(self.skin_red, self.skin_green, self.skin_blue, 255, arm_width, arm_height)
        left_arm.position = -self.body_width/2, self.head_size/2
        
        right_arm = ColorLayer(self.skin_red, self.skin_green, self.skin_blue, 255, arm_width, arm_height)
        right_arm.position = self.body_width/2 - arm_width, self.head_size/2
        
        self.add(left_arm)
        self.add(right_arm)

class Client(Layer):
    
    is_event_handler = True

    def __init__(self, config, client_ip, client_port):
        from threading import Thread
        from cocos.director import director
        from zombie.common import udp_socket
        
        super(Client, self).__init__()
        
        self.socket = udp_socket()
        
        self.key_lookup = self.load_key_config(config['input']['key'])
        self.mouse_lookup = self.load_mouse_config(config['input']['mouse'])
        
        width, height = director.window.get_size()
        
        self.x_divide = width / 255
        self.y_divide = height / 255
        
        self.player_x = 0
        self.player_y = 0
        self.cursor_changed = 0
        
        self.schedule_interval(self.cursor_update, 0.1)
        
        self.sender = ClientSender(self, client_ip, client_port)
        self.send = self.sender.send
        
        # TODO
        receive_ip = 'localhost'
        receive_port = 9998
        
        self.receiver = ClientReceiver(self, (receive_ip, receive_port), ClientHandler)
        receiver_thread = Thread(target=self.receiver.serve_forever)
        receiver_thread.start()
        
        self.config = config
        
        #from cocos.layer.util_layers import ColorLayer
        player = Player(255, 200, 200, *self.config['player']['color'])
        player.position = width / 2, height / 2
        self.add(player)
        from cocos.actions import RotateBy
        player.do(RotateBy(360, duration=10))
        #body_width = 60
        #body_height = 20
        #body = ColorLayer(red, green, blue, 255, body_width, body_height)
        
        
        #body.position = (width / 2) - (body_width / 2), (height / 2) - (body_height / 2)
        #body.anchor = body_width / 2, body_height / 2
        #self.add(body)
        #head_width = 22
        #head_height = 22
        #head = ColorLayer(255, 200, 200, 255, head_width, head_height)
        #head.position = (width / 2) - (head_width / 2), (height / 2) - (head_height / 2)
        #head.anchor = head_width / 2, head_height / 2
        #self.add(player)
        #from cocos.actions import RotateBy
        #body.do(RotateBy(360, duration=10))
    
    def update(self, data):
        from struct import unpack
        
        (player_x,
         player_y,
         player_rotation,
         new_objects_length,
         delete_objects_length) = unpack('3fH', data[1:15])
        new_objects_stop = 15 + (new_objects_length * 15)
        new_objects = unpack('HB3f' * new_objects_length, data[15:new_objects_stop])
        # TODO: Iterate over objects.
        update_objects_data = data[new_objects_stop:]
        update_objects = unpack('H3f' * (len(update_objects_data) / 14), update_objects_data)
    
    def quit(self):
        from sys import exit
        from zombie.constants import CLIENT_CODES_BYTES
        
        self.send(CLIENT_CODES_BYTES['disconnect'])
        # TODO: exit cleanly and show credits
        exit(0)
    
    def load_key_config(self, key_config):
        from pyglet.window import key
        from zombie.constants import CLIENT_CODES_BYTES
        
        key_actions = {
            'forwards': {
                'press': CLIENT_CODES_BYTES['start_move_forwards'],
                'release': CLIENT_CODES_BYTES['end_move_forwards'],
            },
            'backwards': {
                'press': CLIENT_CODES_BYTES['start_move_backwards'],
                'release': CLIENT_CODES_BYTES['end_move_backwards'],
            },
            'strafe_left': {
                'press': CLIENT_CODES_BYTES['start_strafe_left'],
                'release': CLIENT_CODES_BYTES['end_strafe_left'],
            },
            'strafe_right': {
                'press': CLIENT_CODES_BYTES['start_strafe_right'],
                'release': CLIENT_CODES_BYTES['end_strafe_right'],
            },
            'run': {
                'press': CLIENT_CODES_BYTES['start_run'],
                'release': CLIENT_CODES_BYTES['end_run'],
            },
            'attack': {
                'press': CLIENT_CODES_BYTES['start_attack'],
                'release': CLIENT_CODES_BYTES['end_attack'],
            },
            'use': {
                'press': CLIENT_CODES_BYTES['start_use'],
                'release': CLIENT_CODES_BYTES['end_use'],
            },
            'throw_equipped_item': {
                'press': CLIENT_CODES_BYTES['throw_equipped_item'],
                'release': None,
            },
            'drop_equipped_item': {
                'press': CLIENT_CODES_BYTES['drop_equipped_item'],
                'release': None,
            },
            'turn_around': {
                'press': CLIENT_CODES_BYTES['turn_around'],
                'release': None,
            },
            'equip_slot_1': {
                'press': CLIENT_CODES_BYTES['equip_slot_1'],
                'release': None,
            },
            'equip_slot_2': {
                'press': CLIENT_CODES_BYTES['equip_slot_2'],
                'release': None,
            },
            'equip_slot_3': {
                'press': CLIENT_CODES_BYTES['equip_slot_3'],
                'release': None,
            },
            'equip_slot_4': {
                'press': CLIENT_CODES_BYTES['equip_slot_4'],
                'release': None,
            },            
            'equip_slot_5': {
                'press': CLIENT_CODES_BYTES['equip_slot_5'],
                'release': None,
            },            
            'equip_slot_6': {
                'press': CLIENT_CODES_BYTES['equip_slot_6'],
                'release': None,
            },
            'equip_slot_7': {
                'press': CLIENT_CODES_BYTES['equip_slot_7'],
                'release': None,
            },
            'equip_slot_8': {
                'press': CLIENT_CODES_BYTES['equip_slot_8'],
                'release': None,
            },
            'equip_slot_9': {
                'press': CLIENT_CODES_BYTES['equip_slot_9'],
                'release': None,
            },
            'inventory': {
                'press': self.inventory,
                'release': None,
            },
            'quit': {
                'press': self.quit,
                'release': None,
            },
        }
        
        key_lookup =  {}
        for action, key_name in key_config.items():
            key_value = getattr(key, key_name)
            key_lookup[key_value] = key_actions[action]
        
        return key_lookup

    def load_mouse_config(self, mouse_config):
        from pyglet.window import mouse
        from zombie.constants import CLIENT_CODES_BYTES
        
        mouse_actions = {
            'attack': {
                'press': CLIENT_CODES_BYTES['start_attack'],
                'release': CLIENT_CODES_BYTES['end_attack'],
            },
            'use': {
                'press': CLIENT_CODES_BYTES['start_use'],
                'release': CLIENT_CODES_BYTES['end_use'],
            },
        }
        
        mouse_lookup = {}
        for action, button_name in mouse_config.items():
            button_value = getattr(mouse, button_name)
            mouse_lookup[button_value] = mouse_actions[action]
        
        return mouse_lookup
    
    # Input: keyboard
    
    def _on_key(self, change, key, modifiers):
        '''
        SPEED: 2.52 microseconds for mapped key (Glen work)
        SPEED: 1.07 microseconds for unmapped key (Glen work)

        :param change: 'press' or 'release'
        '''
        if key not in self.key_lookup:
            return
        value = self.key_lookup[key][change]
        if not value:
            return
        elif callable(value):
            value()
        else:
            # Strings should be sent to the server.
            self.send(value)
    
    def on_key_press(self, key, modifiers):
        self._on_key('press', key, modifiers)
    
    def on_key_release(self, key, modifiers):
        self._on_key('release', key, modifiers)
    
    # Input: mouse
    
    def _on_mouse_button(self, change, x, y, buttons):
        '''
        SPEED: 2.39 microseconds for mapped button (Glen work)
        SPEED: 1.93 microseconds for unmapped button (Glen work)
        
        :param change: 'press' or 'release'
        '''
        for button, value in self.mouse_lookup.items():
            if buttons & button:
                self.send(value[change])
    
    #def _on_mouse_move(self, x, y):
        ## XXX: Could send dx and dy to reduce bandwidth?
        #x_scaled = int(x / self.x_divide)
        #y_scaled = int(y / self.y_divide)
        #if x_scaled != self.x_scaled or y_scaled != self.y_scaled:
            #self.x_scaled = x_scaled
            #self.y_scaled = y_scaled
            #self.client.send(
                #CODES['cursor_motion'] +
                #struct.pack('B', x_scaled) +
                #struct.pack('B', y_scaled)
            #)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self._on_mouse_button('press', x, y, buttons)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._on_mouse_button('release', x, y, buttons)
    
    def cursor_update(self, time):
        if not self.cursor_changed:
            return
        
        from zombie.constants import CLIENT_CODES
        
        x_scaled = int(self.player_x / self.x_divide) 
        y_scaled = int(self.player_y / self.y_divide)
        self.send(bytes((
            CLIENT_CODES['cursor_motion'],
            x_scaled,
            y_scaled,
        )))
        self.cursor_changed = False
    
    def _on_mouse_move(self, x, y):
        self.player_x = x
        self.player_y = y
        self.cursor_changed = True
    
    def on_mouse_motion(self, x, y, dx, dy):
        self._on_mouse_move(x, y)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        '''
        Event replaces on_mouse_motion when a button is pressed.
        '''
        self._on_mouse_move(x, y)
        # XXX: We could increase accuracy for drag (attacks).
        #self._on_mouse_move(x, y)

    def inventory(self):
        pass


def main():
    
    #from pyglet.gl import Config as GLConfig
    from cocos.director import director
    from cocos.layer import MultiplexLayer
    from cocos.scene import Scene
    
    #gl_config = GLConfig(sample_buffers=1, samples=4)
    
    setup_resources()
    #import time
    #a = time.time()
    config = Config()
    director.init()
    scene = Scene()
    
    # TODO: Fetch.
    client_ip = 'localhost'
    client_port = 9998
    
    client = Client(config.config, client_ip, client_port)
    connect = ConnectScreen(scene, client.sender.connect, lambda: client.sender.client_id, next_layer=JoinGameMenu)
    
    layers = (
        TitleScreen(scene),
        MainMenu(config.config, scene),
        JoinGameMenu(config.config, scene, connect),
        SettingsMenu(config.config, scene),
        QuitScreen(scene),
        KickScreen(scene),
        ConnectFailedScreen(scene),
        connect,
        client,
    )
    
    scene.layer_map = {l.__class__: i for i, l in enumerate(layers)}
    
    layers = MultiplexLayer(*layers)
    scene.add(layers)
    #b = time.time()
    #print(b-a)
    director.run(scene) 


if __name__ == '__main__':
    main()