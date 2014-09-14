FIRST_NAMES = (
    'Glen',
    'David',
    'Lee',
)

LAST_NAMES = (
    'Kirkup',
    'Stainer',
    'Neale',
    'Ingram',
)

class Character(object):
    def __init__(self, name, health, movement_speed, rotation_speed):
        self.name = name
        self.health = health
        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed


class BasicZombie(Character):
    def __init__(self, name):
        super(BasicZombie, self).__init__(name, health=20, movement_speed=0.1, rotation_speed=0.5)


def create_zombie(name=None, cls=BasicZombie):
    '''
    Factory function to fill out zombie names.
    '''
    if not name:
        name = '%s %s' % (random.choice(FIRST_NAMES), random.choice(LAST_NAMES))
    return cls(name)


class Player(Character):
    def __init__(self, name, health, movement_speed, rotation_speed, hunger=0, thirst=0):
        super(Player, self).__init__(name, health, movement_speed, rotation_speed)
        
        self.hunger = hunger
        self.thirst = thirst
        
        self.equipped = None
    
    def use(self):
        # TODO: Pick up nearby items, etc.
        pass