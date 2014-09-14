import socket
import struct
import sys

import cocos


cocos.director.director.init()


from pyglet.window import key, mouse


import socketserver
from struct import pack, unpack
import threading


class NetworkReceiver(socketserver.UDPServer):
    def __init__(self, network_client, *args, **kwargs):
        super(NetworkReceiver, self).__init__(*args, **kwargs)
        
        self.network_client = network_client


class NetworkHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        import struct
        from zombie.common import SERVER_CODES
        
        data = self.request[0]
        #socket = self.request[1]
        
        if data[0] == SERVER_CODES['update']:
            self.server.network_client.update(data)
        elif data[0] == SERVER_CODES['connected']:
            print('connected', data[1])
            self.server.network_client.client_id = data[1]
        elif data[0] == SERVER_CODES['kicked']:
            self.server.network_client.zombie_client.quit()
        
        
        #if data[0] == ord(b'a'):
            #client_id = struct.unpack('xB', data)
            #self.server.client_id_callback(client_id)
        #socket = self.request[1]
        #print('client', data)



class NetworkClient(object):
    def __init__(self, zombie_client, receive_ip, receive_port, server_ip, server_port, client_id=0):
        from threading import Thread
        from zombie.common import udp_socket
        
        self.zombie_client = zombie_client
        
        self.socket = udp_socket()
        
        self.receive_ip = receive_ip
        self.receive_port = receive_port
        self.server_ip = server_ip
        self.server_port = server_port
        
        self.client_id = client_id
        
        self.client_receiver = NetworkReceiver(self, (receive_ip, receive_port), NetworkHandler)
        receiver_thread = Thread(target=self.client_receiver.serve_forever)
        receiver_thread.start()
    
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
    
    def connect(self):
        from zombie.common import CLIENT_CODES, pack_host
        
        self.send(bytes((CLIENT_CODES['connect'],)) + pack_host(self.receive_ip, self.receive_port))
    
    def disconnect(self):
        if not self._client_id:
            raise ValueError('Cannot disconnect as client_id is not set.')
        self.send(data)
    
    def update(self):
        pass
    

class ZombieClient(cocos.layer.Layer):
    
    is_event_handler = True

    def __init__(self, config, client_ip, client_port, server_ip, server_port):
        from zombie.common import udp_socket
        
        super(ZombieClient, self).__init__()
        
        self.socket = udp_socket()
        
        self.key_lookup = self.load_key_config(config['input']['key'])
        self.mouse_lookup = self.load_mouse_config(config['input']['mouse'])
        
        self.width = 640
        self.height = 480
        
        self.x_divide = 640 / 255
        self.y_divide = 480 / 255
        
        self.x = 0
        self.y = 0
        self.cursor_changed = 0
        
        self.schedule_interval(self.cursor_update, 0.1)
        
        self.client = NetworkClient(self, client_ip, client_port, server_ip, server_port)
        self.client.connect()
    
    def quit(self):
        from zombie.common import CLIENT_CODES
        
        self.client.send(CLIENT_CODES['disconnect'])
        # TODO: exit cleanly and show credits
        sys.exit(0)
    
    def load_key_config(self, key_config):
        from zombie.common import CLIENT_CODES
        
        key_actions = {
            'forwards': {
                'press': bytes((CLIENT_CODES['start_move_forwards'],)),
                'release': bytes((CLIENT_CODES['end_move_forwards'],)),
            },
            'backwards': {
                'press': bytes((CLIENT_CODES['start_move_backwards'],)),
                'release': bytes((CLIENT_CODES['end_move_backwards'],)),
            },
            'strafe_left': {
                'press': bytes((CLIENT_CODES['start_strafe_left'],)),
                'release': bytes((CLIENT_CODES['end_strafe_left'],)),
            },
            'strafe_right': {
                'press': bytes((CLIENT_CODES['start_strafe_right'],)),
                'release': bytes((CLIENT_CODES['end_strafe_right'],)),
            },
            'attack': {
                'press': bytes((CLIENT_CODES['start_attack'],)),
                'release': bytes((CLIENT_CODES['end_attack'],)),
            },
            'use': {
                'press': bytes((CLIENT_CODES['start_use'],)),
                'release': bytes((CLIENT_CODES['end_use'],)),
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
        
        print('loaded key config', key_config)
        
        return key_lookup

    def load_mouse_config(self, mouse_config):
        from zombie.common import CLIENT_CODES
        mouse_actions = {
            'attack': {
                'press': bytes((CLIENT_CODES['start_attack'],)),
                'release': bytes((CLIENT_CODES['end_attack'],)),
            },
            'use': {
                'press': bytes((CLIENT_CODES['start_use'],)),
                'release': bytes((CLIENT_CODES['end_use'],)),
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
            self.client.send(value)
    
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
                self.client.send(value[change])
    
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
        
        from zombie.common import CLIENT_CODES
        
        x_scaled = int(self.x / self.x_divide) 
        y_scaled = int(self.y / self.y_divide)
        self.client.send(bytes((
            CLIENT_CODES['cursor_motion'],
            x_scaled,
            y_scaled,
        )))
        self.cursor_changed = False
    
    def _on_mouse_move(self, x, y):
        self.x = x
        self.y = y
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


def main():
    host = 'localhost'
    port = 9998
    #server = socketserver.UDPServer((host, port), UDPClient)
    #server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.start()
    import os
    from configobj import ConfigObj
    config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    config = ConfigObj(open(config_file_path, 'rb'))
    cocos.director.director.init()
    #scene = cocos.scene.Scene()
    #client = Client(config, '127.0.0.1', 5005)
    #layers = cocos.layer.MultiplexLayer(
        #client,
        ##TitleScreen(scene),
        ##MainMenu(),
    #)
    #scene.add(client)
    
    cocos.director.director.run(cocos.scene.Scene(ZombieClient(config, b'localhost', 9998, b'localhost', 9997)))


if __name__ == '__main__':
    main()
