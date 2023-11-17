from colorama import *
import random as rnd

from Item import *
from Weapons import *

class IEnemy:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 30
        
class Guard(IEnemy):
    def __init__(self):
        super(Guard, self).__init__('Охранник')
        self.health = 500
        self.attack = 30

class ICharacter:
    def __init__(self, name, level, strength):
        self.strength = strength
        
        self.name = name
        self.level = level
        self.health = 100
        self.inventory = Inventory()
        self.weapon = None
    
    def attack(self, enemy : IEnemy):
        enemy.health -= self.getAttack() * rnd.randint(0, 20)
    
    def addItem(self, item):
        self.inventory.addItem(item)
    
    def getMaxHealth(self):
        return int(self.strength) * self.level * 100
    
    def getAttack(self):
        if self.weapon == None:
            return self.strength * self.level
        else:
            return self.strength * self.level * self.weapon.damage
    
    def equip(self, itemName):
        item = self.getItem(itemName)
        if item == None:
            return
        
        if isinstance(item, IWeapon):
            self.weapon = item
    
    def getStatusColor(self, value, maxvalue):
        _temp = float(maxvalue) - value
        if _temp <= float(maxvalue) * 0.25:
            return Fore.GREEN
        elif _temp <= float(maxvalue) * 0.5:
            return Fore.YELLOW
        else:
            return Fore.RED
        
    def getHeaderColor(self):
        return Back.WHITE + Fore.BLACK
    
    def getOptionColor(self):
        return Back.BLUE + Fore.WHITE
    
    def showStats(self):        
        print(self.getHeaderColor() + f'[Статистика {self.name}]' + Style.RESET_ALL + ':', sep='')
        print('\t' + self.getOptionColor() + 'Уровень' + Style.RESET_ALL + f': {self.level}', sep='')
        print('\t' + self.getOptionColor() + 'Здоровье' + Style.RESET_ALL + ': ' + self.getStatusColor(self.health, self.getMaxHealth()) + Back.BLACK + f'{self.health}/{self.getMaxHealth()}' + Style.RESET_ALL, sep='')
        print('\t' + self.getOptionColor() + 'Атака' + Style.RESET_ALL + ': ' + str(self.getAttack()) + Style.RESET_ALL, sep='')
    
    def showInventory(self):
        print(self.getHeaderColor() + f'[Инвентарь {self.name}]' + Style.RESET_ALL + ':', sep='')
        for key, value in self.inventory.items.items():
            if value['count'] < 1:
                continue
            
            itemColor = None
            
            if value['item'].type == 'Медицина':
                itemColor = self.getStatusColor(100, 100)
            elif value['item'].type == 'Оружие':
                itemColor = self.getStatusColor(0, 100)
            
            print('\t' + self.getOptionColor() + f'{key}' + Style.RESET_ALL + ' ' + self.getStatusColor(100, 100) + f'x{value["count"]}' + f'\t{itemColor}{value['item'].type}' + Style.RESET_ALL, sep='')
    
    def getItem(self, itemName):
        if itemName not in self.inventory.items:
            print(f'Объекта \'{itemName}\' нет в инвентаре')
            return None
        
        currItem = self.inventory.items[itemName]['item']
        self.inventory.items[itemName]['count'] -= 1
        if self.inventory.items[itemName]['count'] < 1:
            del self.inventory.items[itemName]
        return currItem
    
    def delItem(self, itemName):
        if itemName not in self.inventory.items:
            print(f'Объекта \'{itemName}\' нет в инвентаре')
            return None
        
        self.inventory.items[itemName]['count'] -= 1
        if self.inventory.items[itemName]['count'] < 1:
            del self.inventory.items[itemName]
            
            
class MainCharacter(ICharacter):
    def __init__(self):
        super(MainCharacter, self).__init__(name='Олег', level=1, strength=5)
        self.health = self.getMaxHealth()
        