from Item import *
from Character import *
from Game import *
from random import *
    
class Enemies(Inventory):
    def __init__(self):
        super(Enemies, self).__init__()
    
    def attackEnemy(self, enemyName, damage):
        if enemyName not in self.items:
            print(f'Не найден враг \'{enemyName}\'')
            return None
        
        self.items[enemyName]['item'].health -= damage
        if self.items[enemyName]['item'].health <= 0:
            del self.items[enemyName]
    
    def addItem(self, item):
        if not isinstance(item, IEnemy):
            print('Не удалось добавить врага (item != IEnemy)')
            return 
            
        if item.name not in self.items:
            self.items[item.name] = {}
            self.items[item.name]['item'] = item
            self.items[item.name]['count'] = 1
        else:
            self.items[item.name]['count'] += 1
            
    def getItem(self, itemName):
        if itemName not in self.items:
            print(f'Не найден враг \'{itemName}\'')
            return None
        
        currItem = self.items[itemName]['item']
        return currItem

class ILocation:
    def __init__(self, name, width):
        self.name = name
        self.width = width
        self.curr_pos = 0
        self.messages = []
        self.message_start = 'Интерфейс'
        self.is_entered = False
        self.inventory = Inventory()
        self.enemies = Enemies()
        
    def step(self):
        pass
    
    def addEnemy(self, enemy):
        self.enemies.addItem(enemy)
    
    def addItem(self, item):
        self.inventory.addItem(item)
    
    def getItem(self, itemName):
        return self.inventory.getItem(itemName)
    
    def lookAround(self, character : ICharacter):
        print(character.getHeaderColor() + f'[Найденные вещи]' + Style.RESET_ALL + ':', sep='')
        for key, value in self.inventory.items.items():
            if value['count'] < 1:
                continue
            
            itemColor = None
            
            if value['item'].type == 'Медицина':
                itemColor = character.getStatusColor(100, 100)
            elif value['item'].type == 'Оружие':
                itemColor = character.getStatusColor(0, 100)
            
            print('\t' + character.getOptionColor() + f'{key}' + Style.RESET_ALL + ' ' + character.getStatusColor(100, 100) + f'x{value["count"]}' + f'\t{itemColor}{value['item'].type}' + Style.RESET_ALL, sep='')
            
        if self.enemies.getItemsCount() <= 0:
            return
        
        print('\n' + character.getStatusColor(0, 100) + f'[Враги]' + Style.RESET_ALL + ':', sep='')
        for key, value in self.enemies.items.items():
            if value['count'] < 1:
                continue
            
            print('\t' + character.getOptionColor() + f'{key}' + Style.RESET_ALL + ' ' + character.getStatusColor(100, 100) + f'x{value["count"]}' + f'\t{Fore.RED} Здоровье: {value["item"].health}' + Style.RESET_ALL, sep='')
    
class Event:
    def __init__(self, description, func):
        self.description = description
        self.func = func
    
class StartLocation(ILocation):
    def __init__(self, game):
        super(StartLocation, self).__init__('Начальная локация', 25)
        
        self.message_start = f'{game.mainCharacter.getStatusColor(100, 100)}{game.mainCharacter.name}{Style.RESET_ALL} очнулся в незнакомом месте.'
        self.messages.append(f'{game.mainCharacter.getStatusColor(100, 100)}{game.mainCharacter.name}{Style.RESET_ALL} замечает, что на полу светится какой-то объект')
        self.messages.append(f'{game.mainCharacter.getStatusColor(100, 100)}{game.mainCharacter.name}{Style.RESET_ALL} проходит, и ничего не замечает')
        self.messages.append(f'{game.mainCharacter.getStatusColor(100, 100)}{game.mainCharacter.name}{Style.RESET_ALL} встречает незнакомца')
        
    def step(self): 
        if self.is_entered:
            if self.enemies.getItemsCount() > 0:
                print(f'{Fore.WHITE}{Back.RED}ДВИЖЕНИЕ ОГРАНИЧЕНО{Style.RESET_ALL}')
                return
                
            if self.inventory.getItemsCount() > 0:
                print(self.messages[0])
            else:
                print(self.messages[randint(1, len(self.messages)-1)])
        else:
            print(self.message_start)
            self.is_entered = True
            
        self.curr_pos += 1