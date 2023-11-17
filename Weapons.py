from Item import *

class IWeapon(IItem):
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        self.type = "Оружие"
        
class Knife(IWeapon):
    def __init__(self):
        super(Knife, self).__init__(name = 'Нож',damage = 10)