import logging

import socket

from socketserver import BaseRequestHandler, UDPServer


class Server(UDPServer):
    def __init__(self, map_name, *args, **kwargs):
        from zombie.common import map_file_path, udp_socket
        from zombie.constants import CLIENT_CODES
        
        from blosc import compress
        
        super(Server, self).__init__(*args, **kwargs)
        
        self.map_name = map_name
        
        self.map_file_path = map_file_path(map_name)
        self.map_data = compress(open(self.map_file_path, 'rb').read(), 8)
        #self.map_data_send = bytes((len(self.map_data),)) + self.map_data
        
        self.client_socket = udp_socket()
        
        self.clients = {}
        self.client_id_counter = 1
        
        self.objects = {}
        self.object_id_counter = 0
        
        self.map_objects = {}
        
        self.zombies = {}
        self.zombie_id_counter = 0
        
        self.client_code_actions = {
            CLIENT_CODES['start_move_forwards']: self.start_move_forwards,
            CLIENT_CODES['end_move_forwards']: self.end_move,
            CLIENT_CODES['start_move_backwards']: self.start_move_backwards,
            CLIENT_CODES['end_move_backwards']: self.end_move,
            CLIENT_CODES['start_strafe_left']: self.start_strafe_left,
            CLIENT_CODES['end_strafe_left']: self.end_strafe,
            CLIENT_CODES['start_strafe_right']: self.start_strafe_right,
            CLIENT_CODES['end_strafe_right']: self.end_strafe,
            CLIENT_CODES['start_attack']: self.start_attack,
            CLIENT_CODES['end_attack']: self.end_attack,
            CLIENT_CODES['start_use']: self.start_use,
            CLIENT_CODES['end_use']: self.end_use,
            CLIENT_CODES['throw_equipped_item']: self.throw_equipped_item,
            CLIENT_CODES['drop_equipped_item']: self.drop_equipped_item,
            CLIENT_CODES['cursor_motion']: self.cursor_motion,
        }
        
        self.setup_physics()
    
    def start_move_forwards(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.y = 5
        body.SetLinearVelocity(velocity)
    
    def start_move_backwards(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.y = -5
        body.SetLinearVelocity(velocity)
        
    def end_move(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.y = 0
        body.SetLinearVelocity(velocity)
    
    def start_strafe_left(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.x = -5
        body.SetLinearVelocity(velocity)
    
    def start_strafe_right(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.x = 5
        body.SetLinearVelocity(velocity)
    
    def end_strafe(self, data):
        body = self.clients[data[0]]['body']
        velocity = body.GetLinearVelocity()
        velocity.x = 0
        body.SetLinearVelocity(velocity)
    
    def update_physics(self):
        self.world.Step(self.physics_update_time, self.vel_iters, self.pos_iters)
        static_body.x
    
    def setup_physics(self):
        from threading import Timer
        from Box2D import b2World

        self.physics_update_time = 1 / 10.0
        self.vel_iters = 6
        self.pos_iters = 2
        self.world = b2World(gravity=(0, 0), doSleep=True)
        
        Timer(self.physics_update_time, self.update_physics)
    
    #def update_physics(self):
        #for client in self.clients.values():
            #if client['move_forwards']
    
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
    
    def broadcast_client_action(self, network_code, client_object_id, equipped):
        from struct import pack
        
        data = bytes(network_code) + pack('HH', client_object_id, equipped)
        
        for client_id, client in self.clients.items():
            if client_object_id in client['local_objects']:
                self.send_client(client_id, data)
    
    def start_attack(self, data):
        from time import time
        from zombie.constants import SERVER_CODES
        
        # TODO: attack damage
        
        client = self.clients[data[0]]
        
        client_object_id = client['object_id']
        equipped = client['equipped']
        
        self.broadcast_client_action(SERVER_CODES['start_attack'], client_object_id, equipped)
    
    def end_attack(self, data):
        from time import time
        
        # TODO: stop attack
        
        client = self.clients[data[0]]
        
        object_id = client['object_id']
        client_object_id = client['object_id']
        equipped = client['equipped']
        
        self.broadcast_client_action(SERVER_CODES['end_attack'], client_object_id, equipped)
    
    def start_use(self, data):
        from time import time
        
        # TODO: start use
        
        client = self.clients[data[0]]
        client_object_id = client['object_id']
        equipped = client['equipped']
        
        self.broadcast_client_action(SERVER_CODES['start_use'], client_object_id, equipped)
    
    def end_use(self, data):
        from time import time
        
        client = self.clients[data[0]]
        client_object_id = client['object_id']
        equipped = client['equipped']
        
        self.broadcast_client_action(SERVER_CODES['end_use'], client_object_id, equipped)
    
    def cursor_motion(self, data):
        client = self.clients[data[0]]
        
        client['mouse_x'] = data[2]
        client['mouse_y'] = data[3]
    
    def equip_slot(self, data):
        from zombie.constants import EQUIP_SLOT_CODES
        
        # TODO
        self.client[data[0]].inventory[EQUIP_SLOT_CODES[data[1]]]
    
    def turn_around(self, data):
        # TODO
        
        self.client[data[0]]['rotation'] = (self.client[data[0]]['rotation'] + 180) % 360
    
    def add_client(self, data):
        from struct import unpack
        from Box2D import b2PolygonShape
        from zombie.common import unpack_ip
        from zombie.constants import CLIENT_CODES, SERVER_CODES
        
        if data[1] not in (CLIENT_CODES['connect_ip'], CLIENT_CODES['connect_hostname']):
            logging.warning('Unknown connect message: %s', data)
            return
        
        icon = data[2]
        color = data[3:6]
        red, green, blue  = color
        nickname_stop = 7 + data[6]
        
        nickname = data[7:nickname_stop]
        
        ip_hostname = data[nickname_stop:-2]
        if data[1] == CLIENT_CODES['connect_ip']:
            ip_hostname = unpack_ip(*ip_hostname)
        
        port = unpack('H', data[-2:])[0]
        
        client_id = self.client_id_counter
        body = self.world.CreateStaticBody(position=(0,-10),
                                           shapes=b2PolygonShape(box=(50,10)))
        client = {
            'x': 0,
            'y': 0,
            'mouse_x': 0,
            'mouse_y': 0,
            'ip_hostname': ip_hostname,
            'port': port,
            'inventory': {},
            'nickname': nickname,
            'equipped': 0,
            'body': body,
            'object_id': self.object_id_counter,
        }
        
        #from Box2D import b2BodyDef, b2FixtureDef, b2PolygonShape
        
        #player_body_def = b2BodyDef()
        #player_body_def.position = 0, 0
        #player_body = self.world.CreateBody(player_body_def)
        #player_box = b2PolygonShape(box=(50, 10))
        #player_box_fixture = b2FixtureDef(shape=player_box)
        #player_body.CreateFixture(player_body_fixture)
        
        self.send_clients(bytes((
            SERVER_CODES['player_connected'],
            client_id,
            icon,
            red,
            green,
            blue,
        )) + nickname)
        
        self.clients[client_id] = client
        
        #print('connected')
        self.send_client(client_id, bytes((
            SERVER_CODES['connected'],
            client_id,
        )) + self.map_data)
        
        self.objects[self.object_id_counter] = {
        }
        self.map_objects[self.object_id_counter] = {
            'body': body,
        }
        self.client_id_counter += 1
        self.object_id_counter += 1
        return client_id, client
    
    def send_connected(self, client_id):
        self.send_client(client_id, )
    
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
        print('sending to', client['ip_hostname'], client['port'])
        self.client_socket.sendto(data, (client['ip_hostname'], client['port']))
    
    def send_clients(self, data, exclude=None):
        for client_id in self.clients.keys():
            if exclude and client_id in exclude:
                continue
            self.send_client(client_id, data)
    
    def handle(self, data):
        
        print(data)
        
        from zombie.common import client_data_debug
        print(client_data_debug(data))
        
        client_id = data[0]
        if client_id in self.clients:
            self.client_code_actions[data[1]](data)
        elif client_id == 0:
            self.add_client(data)
        else:
            logging.warning('Unknown client id: %d', client_id)
        
        #if data[0] == ord(b'm'):
        #    x, y = unpack('xBB', data)
        #    print(x, y)
        #else:
        #    #
        #    print(data)
    
    def nearby_objects(self, client, x, y):
        client_range = self.client_range
        client_objects = client['objects']
        max_x = x + client_range
        min_x = x - client_range
        max_y = y + client_range
        min_y = y - client_range
        
        object_delete_ids = []
        objects_update = {}
        
        for object_id, obj in self.objects.iteritems():
            if not (min_x < obj['x'] < max_x and min_y < obj['y'] < max_y):
                if object_id in client_objects:
                    client_objects.remove(object_id)
                    object_delete_ids.append(object_id)
                continue
            
            if object_id in client_objects:
                if obj['modified_time'] >= client['update_time']:
                    objects_update[object_id] = obj
            else:
                objects_update[object_id] = obj
        
        return objects_update, object_delete_ids


class Handler(BaseRequestHandler):
        
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
    server = Server('map1', (host, port), Handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
