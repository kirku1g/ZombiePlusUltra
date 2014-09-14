'''
# Item ideas:
# * Tacks
# * Mine
# * Chainsaw
# * Weapon Durability / Repair
# * Descriptions
# * Gun Upgrades
# * Food
# * Drink
# * Energy
# * Lockpicks
# * Surveillance
# * Nails
# * Food going off
'''

from zombie.common import reverse_dict


class Item(object):
    def __init__(self, name, image, stackable, weight):
        self.name = name
        # image - image filename for item (on ground and in inventory)
        self.image = image
        # stackable - stackable in player's inventory
        self.stackable = stackable
        # weight - weight in player's inventory
        self.weight = weight
        
    
    def use(self):
        pass


# Items: Drink

class Drink(Item):
    
    def __init__(self, name, image, weight, quenching):
        super(Drink, name, image, stackable=True, weight=weight)
        # quenching - amount thirst is quenched by drinking
        self.quenching = quenching
    
    def use(self):
        '''
        Quench player's thirst.
        '''
        # TODO
        pass


class ColaCan(Drink):
    CODE = 20
    def __init__(self):
        super(Drink, self).__init__('Cola Can', 'cola_can.png', weight=weight, quenching=10)


# Items: Food

class Food(Item):
    def __init__(self, name, image, weight, filling):
        super(Food, self).__init__(name, image, stackable=True, weight=weight)
        # filling - amount hunger is reduced by after eating
        self.filling = filling


# Items: Food: Canned

class BakedBeans(Item):
    CODE = 40
    def __init__(self):
        super(BakedBeans, self).__init__('Baked Beans', 'baked_beans.png', weight=0.5, filling=10)


# Items: Food: Fruit

class Apple(Food):
    CODE = 50
    def __init__(self):
        super(Seed, self).__init__('Apple', 'apple.png', weight=0.2, filling=10)


# Plants

class Plant(object):
    def __init__(self, name, growth_speed, fruit_speed, fruit):
        self.name = name
        # growth speed - length of time it takes for the plant to grow
        self.growth_speed = growth_speed
        # fruit speed - length of time it takes for the fruit to regenerate
        self.fruit_speed = fruit_speed
        # fruit - fruit which grows on the plant
        self.fruit = fruit


class ApplePlant(Plant):
    def __init__(self):
        super(ApplePlant, self).__init__('Apple Plant', 1, Apple)


# Items: Seeds

class Seed(Item):
    def __init__(self, name, plant):
        super(Seed, self).__init__(name, image, stackable=True, weight=0.1)
        self.plant = plant
    
    def use(self):
        # TODO: Plant seed.
        self.plant


class AppleSeed(Seed):
    CODE = 70
    def __init__(self):
        super(AppleSeed, self).__init__('Apple Seed', 'apple_seed.png', ApplePlant)


# Items: Phone
        
class Phone(Item):
    '''
    Phone is used for viewing the map and sending messages.
    '''
    CODE = 0
    
    def __init__(self):
        super(Item, self).__init__('Phone', 'phone.png', stackable=False, weight=0.2)
    
    def use(self):
        '''
        '''
        # TODO
        pass


class Planks(Item):
    '''
    '''
    CODE = 1
    
    def __init__(self):
        super(Item, self).__init__('Planks', 'planks.png', stackable=True, weight=5)
    
    def use(self):
        '''
        Hold against door or window if nearby.
        '''
        # TODO
        pass


# Items: Armour

class Armour(Item):
    '''
    Armour is the superclass for wearable armour.
    '''
    def __init__(self, name, image, weight, defense):
        super(Armour, self).__init__(name, image, stackable=False, weight=weight)
        self.defense = defense


class KevlarVest(Armour):
    CODE = 100
    
    def __init__(self):
        super(Armour, self).__init__('Kevlar Vest', 'kevlar_vest.png', weight=20, defense=1)


# Items: Weapons

class Weapon(Item):
    
    def __init__(self, name, image, stackable, weight, damage, attack_speed, range):
        super(Weapon, self).__init__(name, image, stackable, weight)
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range

    def use(self):
        # TODO: Attack
        pass


# Items: Weapons: Melee Weapons / Tools


class Crowbar(Weapon):
    
    CODE = 120
    
    def __init__(self):
        super(Crowbar, self).__init__(
            'Crowbar',
            'crowbar.png',
            stackable=False, 
            weight=10,
            damage=7,
            attack_speed=20,
            range=1,
        )
    
    def use(self):
        # TODO: Remove barricades if nearby
        pass
    

class Hammer(Weapon):
    
    CODE = 121
    
    def __init__(self):
        super(Crowbar, self).__init__(
            'Hammer',
            'hammer.png',
            stackable=False,
            weight=7,
            damage=7,
            attack_speed=20,
            range=0.5,
        )
    
    def use(self):
        # TODO: Remove barricades if nearby
        # TODO: Setup barricade if nearby
        pass
    
        
# Items: Weapons: Melee Weapons

class Knife(Weapon):
    
    ITEM_CODE = 122
    
    def __init__(self):
        super(Knife, self).__init__(
            'Knife',
            'knife.png',
            stackable=False,
            weight=4,
            damage=3,
            attack_speed=10,
            range=0.5,
        )


class BaseballBat(Weapon):
    
    ITEM_CODE = 123
    
    def __init__(self):
        super(BaseballBat, self).__init__(
            'Baseball Bat',
            'baseball_bat.png',
            stackable=False,
            weight=10,
            damage=10,
            attack_speed=20,
            range=1.2,
        )


class Pipe(Weapon):
    
    ITEM_CODE = 124
    
    def __init__(self):
        super(Pipe, self).__init__(
            'Pipe',
            'pipe.png',
            stackable=False,
            weight=8,
            damage=10,
            attack_speed=20,
            range=1.2,
        )
        


# Items: Ammo

class Ammo(Item):
    def __init__(self, name, weight):
        super(Ammo, self).__init__(name, stackable=True, weight=weight)


class Ammo9mm(Ammo):
    
    ITEM_CODE = 140
    
    def __init__(self):
        super(Ammo9mm, self).__init__('9mm Ammo', 'ammo_9mm.png', weight=0.05)

class Ammo45(Ammo):
    
    ITEM_CODE = 141
    
    def __init__(self):
        super(Ammo45, self).__init__('45 Ammo', 'ammo_45.png', weight=0.1)

class Ammo3006(Ammo):
    
    ITEM_CODE = 142
    
    def __init__(self):
        super(Ammo3006, self).__init__('30.06 Ammo', 'ammo_3006.png', weight=0.2)


class Ammo762(Ammo):
    
    ITEM_CODE = 143
    
    def __init__(self):
        super(Ammo762, self).__init__('7.62 Ammo', 'ammo_762.png', weight=0.3)



# Items: Weapons: Guns


class Gun(Weapon):
    
    def __init__(self, name, image, weight, damage, attack_speed, range, spray, ammo, reload_speed):
        super(Gun, self).__init__(name, image, False, weight, damage, attack_speed, range)
        # spray - inaccuracy increased by firing
        self.spray = spray
        # ammo - type of ammo the gun accepts
        self.ammo = ammo
        self.reload_speed = reload_speed

##class Shotgun(Gun):
    ##def __init__(self, name, image, weight, damage, attack_speed, range, spread, ammo, reload_speed):
        ##super(Shotgun, self).__init__(...)
        ##self.spread = spread


##class Buckshot(Shotgun):
    
    


# Items: Weapons: Guns: Pistols

class Pistol(Gun):
    pass


class M1911A1(Pistol): #7
    
    ITEM_CODE = 160
    
    def __init__(self):
        super(M1911A1, self).__init__(
            'M1911A1',
            'm1911a1.png',
            weight=12,
            damage=8,
            attack_speed=10,
            range=15,
            spray=0,
            ammo=Ammo45,
            reload_speed=1,
        )


class Glock17(Pistol): #17
    
    ITEM_CODE = 161
    
    def __init__(self):
        super(Glock17, self).__init__(
            'Glock 17',
            'glock_17.png',
            weight=10,
            damage=5,
            attack_speed=7,
            range=15,
            spray=1,
            ammo=Ammo9mm,
            reload_speed=0.8,
        )


class Colt45(Pistol): # 6
    
    ITEM_CODE = 162
    
    def __init__(self):
        super(Colt45, self).__init__(
            'Colt 45',
            'colt_45.png',
            weight=14,
            damage=10,
            attack_speed=15,
            range=20,
            spray=0,
            ammo=Ammo45,
            reload_speed=2,
        )


# Items: Weapons: Guns: Submachine Guns

class Uzi(Gun):
    
    ITEM_CODE = 170
    
    def __init__(self): #32
        super(Uzi, self).__init__(
            'Uzi',
            'uzi.png',
            stackable=False,
            weight=20,
            damage=3,
            attack_speed=2,
            range=10,
            spray=10,
            ammo=Ammo9mm,
            reload_speed=4,
        )


# Items: Weapons: Guns: Rifles

class M1903Springfield(Gun):
    
    ITEM_CODE = 180
    
    def __init__(self): #5
        super(M1903Springfield, self).__init__(
            'M1903 Springfield',
            'm1903_springfield.png',
            stackable=False,
            weight=30,
            damage=15,
            attack_speed=20,
            range=40,
            spray=0,
            ammo=Ammo3006,
            reload_speed=5,
        )



# Items: Weapons: Guns: Automatic Rifles

class AK47(Gun):
    
    ITEM_CODE = 181
    
    def __init__(self): #30
        super(AK47, self).__init__(
            'AK47',
            'ak47.png',
            weight=35,
            damage=8,
            attack_speed=4,
            range=25,
            spray=3,
            ammo=Ammo762,
            reload_speed=5,
        )


# Items: Magazines


class Magazine(Item):
    def __init__(self, name, weight, ammo, weapon_class):
        super(Magazine, self).__init__(name, stackable=False, weight=weight)
        self.ammo = ammo
        self.weapon_class = weapon_class
        
class Pistol9mmMagazine(Magazine):
    
    ITEM_CODE = 121
    
    def __init__(self):
        super(Pistol9mmMagazine, self).__init__(
            'Pistol 9mm Magazine',
            weight=0.5,
            ammo=Ammo9mm,
            weapon_class=Pistol,
        )


# Items: Weapons: Grenades

class Projectile(Item):
    def __init__(self, name, image, weight, range):
        super(Projectile, self).__init__(name, image, stackable=True, weight=weight)
        self.range = range
    
    def use(self):
        # TODO: throw
        pass


class Flare(Projectile):
    
    ITEM_CODE = 200
    
    def __init__(self):
        super(Flare, self).__init__('Flare', 'flare.png', weight=3, range=15)
    
    def use(self):
        # TODO: light flare, attract zombies
        pass

class Flashbang(Weapon):
    
    ITEM_CODE = 201
    
    def __init__(self):
        super(Flashbang, self).__init__('Flashbang', 'flashbang.png', weight=4, range=10)
    
    def explode(self):
        # TODO: Flash
        pass
    
class SmokeGrenade(Weapon):
    
    ITEM_CODE = 202
    
    def __init__(self):
        super(SmokeGrenade, self).__init__('Smoke Grenade', 'smoke_grenade.png', weight=6, range=10)
    
    def explode(self):
        # TODO: Smoke
        pass


class Grenade(Projectile):
    def __init__(self, name, image, damage, splash_damage):
        super(Gun, self).__init__(name, image, weight, damage, 5, 10)
        self.splash_damage = splash_damage
    
    def explode(self):
        pass



class FragGrenade(Grenade):
    
    ITEM_CODE = 210
    
    def __init__(self):
        super(Grenade, self).__init__('Frag Grenade', 'frag_grenade.png', 8, 20, 15)
    
    def explode(self):
        # TODO: Blast radius.
        pass


ITEMS = (
    Phone,
)

ITEM_CODES = {item.ITEM_CODE for item in ITEMS}

ITEM_CODES_REVERSE_LOOKUP = reverse_dict(ITEM_CODES)