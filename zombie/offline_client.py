import random

import pyglet
from pyglet import font, resource
from pyglet.window.key import DOWN, ENTER, UP

import cocos

from cocos.actions import *

import sys


from math import pi

from cocos.menu import Menu, MenuItem, shake, shake_back


def get_resources_dir():
    from os.path import dirname, join, realpath
    
    return join(dirname(realpath(__file__)), 'resources')


class TitleScreen(cocos.layer.Layer):

    is_event_handler = True
    
    def __init__(self, scene):
        super(TitleScreen, self).__init__()
        self.scene = scene
        label = cocos.text.Label(
            'Zombie',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center',
            anchor_y='center',
        )
        
        label.position = 320, 240
        self.add(label)
    
    def on_key_press(self, key, modifiers):
        if key == ENTER:
            self.scene.get_children()[0].switch_to(1)


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Zombie')
        #self.select_sound = soundex.load('move.mp3')

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 32
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman'
        self.font_item['color'] = (128,128,128,255)
        self.font_item['font_size'] = 16
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (255,255,255,255)
        self.font_item_selected['font_size'] = 24

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = []
        
        items.append(MenuItem('New Game', self.new_game))
        items.append(MenuItem('Quit', self.quit))

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
        self.create_menu(items, shake(), shake_back())
    
    def new_game(self):
        print('New Game')
    
    def quit(self):
        print('Thanks for playing!')
        sys.exit(0)





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
            print(((index % self.columns) * self.item_width) + (self.item_width / 2), height - ((floor(index / self.rows) + 1) * self.item_height) - (self.item_height / 2))
            item_positions.append((
                ((index % self.columns) * self.item_width) + (self.item_width / 2),
                height - ((floor(index / self.columns) + 1) * self.item_height) - (self.item_height / 2),
            ))
        
        print(menu_items)
        print(item_positions)
        
        

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
        print('Thanks for playing!')
        sys.exit(0)



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



class Client(cocos.layer.Layer):
    
    is_event_handler = True
    
    def __init__(self, x, y):
        self.objects = {}
        self.inventory = []
        self.x = x
        self.y = y
        self.rotation = rotation
        self.inventory = Inventory()
        
        # grad - used for rotated movement trigonometry
        self.grad
    
    def request(self):
        # TODO: Send changes
        # TODO: Make UDP request.
        #data = simplejson.loads(request)
        self.objects.update(data['objects_update'])
        for object_id in data['object_delete_ids']:
            del self.objects[object_id]
        
    
    
    def on_key_press(self, key, modifiers):
        movement = {
            UP: forward,
            DOWN: backward,
            LEFT: left,
            RIGHT: right,
        }[key]
        x_diff, y_diff = movement(self.rotation)
        
        self.x = x_diff * self.speed
        
        self.y = y_diff * self.speed
            




def setup_resources():
    from pyglet import font, resource
    
    resources_dir = get_resources_dir()
    # Need to override path as '.' entry causes problems.
    resource.path = [resources_dir]
    resource.reindex()
    font.add_directory(resources_dir)


def main():
    
    setup_resources()
    
    cocos.director.director.init()
    scene = cocos.scene.Scene()
    layers = cocos.layer.MultiplexLayer(
        TitleScreen(scene),
        InventoryMenu(),
    )
    scene.add(layers)
    cocos.director.director.run(scene)


#def main():
    #pyglet.resource.path.append('data')
    #pyglet.resource.reindex()
    #font.add_directory('data')

    #director.init( resizable=True, width=600, height=720 )
    #scene = Scene()
    #scene.add(cocos.MultiplexLayer(
                    #MainMenu(), 
                    #OptionsMenu(),
                    #ScoresLayer(),
                    #),
                #z=1 ) 
    #scene.add(BackgroundLayer(), z=0)
    #director.run(scene)    


if __name__ == '__main__':
    main()