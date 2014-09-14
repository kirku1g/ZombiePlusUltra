


class Inventory(object):
    
    def __init__(self):
        self.items = []
    
    def load(self, data):
        from zombie.items import ITEM_CODES
        
        index = 0
        while True:
            
            self.items.append(ITEM_CODES[data[index]]())
            
            # TODO: Parse extra info about item.
            
            index += 1
        #for byte in data:
            
            #self.items.append(ITEM_CODES[byte]())
    
    def add_item(self, item):
        self.items.append(item)
    
    def move_item(self, source_index, target_index):
        if 0 > source_index or len(self.items) <= source_index:
            raise ValueError("Item index not in inventory: %d" % source_index)
        if source_index == target_index:
            return source_index
        
        item = self.items[source_index]
        
        if target_index >= len(self.items):
            self.items.append(item)
        else:
            self.items.insert(target_index, item)
        
        del self.items[source_index]
    
    def remove_item(self, index):
        del self.items[index]
