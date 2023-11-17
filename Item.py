# Интерфейс предмета
class IItem:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.info = 'None'
    
# Интерфейс лечащего предмета
class IHeal(IItem):
    def __init__(self, name, heal):
        super(IHeal, self).__init__(name, 'Медицина')
        self.heal = heal
        
# Предметы
class SmallHealPotion(IHeal):
    def __init__(self):
        super(SmallHealPotion, self).__init__(name = 'Маленькое лечащее зелье', heal = 10)
        
class HealPotion(IHeal):
    def __init__(self):
        super(HealPotion, self).__init__(name = 'Лечащее зелье', heal = 25)

# Инвентарь
class Inventory:
    def __init__(self):
        self.items = {}
    
    def getItemsCount(self):
        return len(self.items)
    
    def delItem(self, itemName):
        if itemName not in self.items:
            print(f'Не найден объект \'{itemName}\'')
            return None
        
        self.items[itemName]['count'] -= 1
        if self.items[itemName]['count'] < 1:
            del self.items[itemName]
    
    def addItem(self, item):
        if isinstance(item, IItem):
            if item.name not in self.items:
                self.items[item.name] = {}
                self.items[item.name]['item'] = item
                self.items[item.name]['count'] = 1
            else:
                self.items[item.name]['count'] += 1
        else:
            print('Не удалось добавить объект (item != IItem)')
            
    def getItem(self, itemName):
        if itemName not in self.items:
            print(f'Не найден объект \'{itemName}\'')
            return None
        
        currItem = self.items[itemName]['item']
        self.items[itemName]['count'] -= 1
        if self.items[itemName]['count'] < 1:
            del self.items[itemName]
        return currItem