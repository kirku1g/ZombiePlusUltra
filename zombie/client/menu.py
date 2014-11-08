from cocos.menu import ImageMenuItem


class MultipleImageMenuItem(ImageMenuItem):
    
    
    def __init__(self, images, *args):
        from pyglet import resource
        
        super(MultipleImageMenuItem, self).__init__(*args)
        self.images = {}
        
        for image in self.images:
            self.images[image] = resource.image(image)
            
    def generateWidgets (self, pos_x, pos_y, font_item, font_item_selected):
        anchors = {'left': 0, 'center': 0.5, 'right': 1, 'top': 1, 'bottom': 0}
        anchor=(anchors[font_item['anchor_x']] * self.image.width,
                anchors[font_item['anchor_y']] * self.image.height)
        
        self.items = {}
        for filename, image in self.images.items():
            item = Sprite(image, anchor=anchor, opacity=255,
                          color=font_item['color'][:3])
            item.scale = font_item['font_size'] / float(self.item.height)
            self.items[filename] = image
        
        self.item = 
        self.item.scale = 
        
        self.item.position = int(pos_x), int(pos_y)
        self.selected_item = Sprite(self.image, anchor=anchor,
                                    color=font_item_selected['color'][:3])
        self.selected_item.scale = (font_item_selected['font_size'] /
                                     float(self.selected_item.height))
        self.selected_item.position = int(pos_x), int(pos_y)    
    
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key
        
        if symbol == key.LEFT:
            self.item = 
