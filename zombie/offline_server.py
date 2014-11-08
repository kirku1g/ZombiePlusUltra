from items import Shotgun

Shotgun



class Server(object):
    def __init__(self):
        self.objects = {}
        self.object_id_counter = 0
        
        self.clients = {}
        self.client_id_counter = 0
        
        self.client_range = 10
        
        self.load()
        
        self.start_time = time.time()
    
    def add_client(self, x, y):
        self.clients[self.client_id_counter] = {
            'object_ids': set(),
            'update_time': time.time(),
            'x': x,
            'y': y,
        }
        self.client_id_counter += 1
    
    def add_object(self, obj, x, y, z):
        self.objects[self.object_id_counter] = {
            'object': obj,
            'x': x,
            'y': y,
        }
        self.object_id_counter += 1
    
    def load(self):
        obj = Apple()
        self.add_object(obj, 10, 10)
    
    def time(self):
        return time.time() - self.start_time
    

    
    def response(self, data, client_id):
        client = self.clients[client_id_counter]
        
        client['x'] = data['x']
        client['y'] = data['y']
        
        # TODO: send new map tiles.
        
        objects_update, object_delete_ids = self.nearby_objects(client)
        
        return {
            'objects_update': objects_update,
            'object_delete_ids': object_delete_ids,
        }
