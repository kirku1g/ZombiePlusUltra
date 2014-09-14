import logging

import socket
import socketserver


def attack(item, local_objects, x, y, mouse_x, mouse_y):
    


class Server(socketserver.UDPServer):
    def __init__(self, *args, **kwargs):
        from zombie.common import CLIENT_CODES, udp_socket
        
        super(Server, self).__init__(*args, **kwargs)
        
        self.client_socket = udp_socket()
        
        self.clients = {}
        self.client_id_counter = 1
        
        self.zombies = {}
        self.zombie_id_counter = 0
        
        self.client_code_actions = {
            CLIENT_CODES['start_move_forwards']: self.client_action('move_forwards', True),
            CLIENT_CODES['end_move_forwards']: self.client_action('move_forwards', False),
            CLIENT_CODES['start_move_backwards']: self.client_action('move_backwards', True),
            CLIENT_CODES['end_move_backwards']: self.client_action('move_backwards', False),
            CLIENT_CODES['start_strafe_left']: self.client_action('strafe_left', True),
            CLIENT_CODES['end_strafe_left']: self.client_action('strafe_left', False),
            CLIENT_CODES['start_strafe_right']: self.client_action('strafe_right', True),
            CLIENT_CODES['end_strafe_right']: self.client_action('strafe_right', False),
            CLIENT_CODES['start_attack']: self.start_attack,
            CLIENT_CODES['end_attack']: self.end_attack,
            CLIENT_CODES['start_use']: self.start_use,
            CLIENT_CODES['end_use']: self.end_use,
            CLIENT_CODES['cursor_motion']: self.cursor_motion,
        }
    
    def update_local_objects(client):
        
    
    def update(self):
        from zombie.common import distance_nested
        
        # Update client.
        for client in self.clients.values():
            if client['move_forwards']:
                pass
            if client['move_backwards']:
                pass
            if client['strafe_left']:
                pass
            if client['strafe_right']:
                pass
        
        # Update zombie positions.
        for zombie in self.zombies.values():
            # TODO: Move (towards player)
            distance = distance_nested(zombie)
            client = min(self.clients.values(), key=distance_nested)
            # TODO: Move zombie towards player.
            zombie['zombie'].speed
    
    def client_action(self, action, value):
        def handler(data):
            self.clients[data[0]][action] = value
        return handler
    
    def start_attack(self, data):
        from time import time
        
        client = self.clients[data[0]]
        
        
        client['events'].append((data[1], time()))
    
    def end_attack(self, data):
        from time import time
        
        client = self.clients[data[0]]
        client['attacks'].append(('end', time()))
    
    def start_use(self, data):
        from time import time
        
        client = self.clients[data[0]]
        client['uses'].append(('start', time()))
    
    def end_use(self, data):
        from time import time
        
        client = self.clients[data[0]]
        client['uses'].append(('end', time()))
    
    def cursor_motion(self, data):
        client = self.clients[data[0]]
        
        client['mouse_x'] = data[2]
        client['mouse_y'] = data[3]
    
    def add_client(self, data):
        from zombie.common import CLIENT_CODES, SERVER_CODES, unpack_host
        
        if data[1] != CLIENT_CODES['connect']:
            logging.warning('Unknown connect message: %s', data)
            return
        
        ip, port = unpack_host(data[2:])
        
        client_id = self.client_id_counter
        client = {
            'x': 0,
            'y': 0,
            'mouse_x': 0,
            'mouse_y': 0,
            'ip': ip,
            'port': port,
            'move_forwards': False,
            'move_backwards': False,
            'strafe_left': False,
            'strafe_right': False,
            'events': [],
            'player': Player(),
        }
        self.clients[client_id] = client
        
        print('connected')
        self.send_client(client_id, bytes((SERVER_CODES['connected'], client_id)))
        
        self.client_id_counter += 1
        return client_id, client
    
    def add_zombie(self, zombie_cls, x, y):
        zombie_id = self.zombie_id_counter
        self.zombies[zombie_id] = {
            'x': x,
            'y': y,
            'zombie': zombie_cls(),
        }
        self.zombie_id_counter += 1
        return zombie_id
    
    def send_client(self, client_id, data):
        print(data)
        client = self.clients[client_id]
        print('sending to', client['ip'], client['port'])
        self.client_socket.sendto(data, (client['ip'], client['port']))
    
    def handle(self, data):
        
        print(data)
        
        from zombie.common import client_data_debug
        print(client_data_debug(data))
        
        client_id = data[0]
        if client_id in self.clients:
            self.client_code_actions[data[1]](data)
        elif client_id == 0:
            self.add_client(data)
            return
        else:
            logging.warning('Unknown client id: %d', client_id)
            return
        
        #if data[0] == ord(b'm'):
        #    x, y = unpack('xBB', data)
        #    print(x, y)
        #else:
        #    #
        #    print(data)
        


class Handler(socketserver.BaseRequestHandler):
        
    '''
    def __init__(self):
        # Fix
        self.clients = {}
        # Starts from 1 as 0 is a special case to setup connection.
        self.client_id_counter = 1
    '''
        
    def handle(self):
        #socket = self.request[1]
        self.server.handle(self.request[0])
        
        #s = socket.socket(socket.AF_INET, # Internet
        #                  socket.SOCK_DGRAM) # UDP
        #s.sendto(data, ('localhost', 9998))


def main():
    host = 'localhost'
    port = 9997
    server = Server((host, port), Handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
