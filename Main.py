from Game import *

init()

class DnD_Game(IGame):
    def onCreate(self):
        self.message = 'None'
        self.hasEnemy = False
        print('')
            
    def onUpdate(self):
        self.message = input('> ')
        
        if self.message == 'выход' or self.message == 'вых':
            self.isRunning = False
        elif self.message == 'помощь':
            print(self.mainCharacter.getHeaderColor() + '[Помощь]' + Style.RESET_ALL + ': ', sep='')
            print('\t' + self.mainCharacter.getOptionColor() + '\'помощь\'' + Style.RESET_ALL + ': Вывод этого окна')
            print('\t' + self.mainCharacter.getOptionColor() + '\'статистика\'' + Style.RESET_ALL + ' / ' + self.mainCharacter.getOptionColor() + '\'стат\'' + Style.RESET_ALL + ': Вывод статистики персонажа')
            print('\t' + self.mainCharacter.getOptionColor() + '\'инвентарь\'' + Style.RESET_ALL + ' / ' + self.mainCharacter.getOptionColor() + '\'инв\'' + Style.RESET_ALL + ': Открыть инвентарь')
            print('\t' + self.mainCharacter.getOptionColor() + '\'осмотреться\'' + Style.RESET_ALL + ' / ' + self.mainCharacter.getOptionColor() + '\'осм\'' + Style.RESET_ALL + ': Осмотреть локацию')
            print('\t' + self.mainCharacter.getOptionColor() + '\'выход\'' + Style.RESET_ALL + ' / ' + self.mainCharacter.getOptionColor() + '\'вых\'' + Style.RESET_ALL + ': Выход из игры')
            
        elif self.message == 'статистика' or self.message == 'стат':
            self.mainCharacter.showStats()
            
        elif self.message == 'инвентарь' or self.message == 'инв':
            self.mainCharacter.showInventory()
            
        elif self.message.split(' ')[0] == 'использовать' or self.message.split(' ')[0] == 'исп':
            itemName = ' '.join(self.message.split(' ')[1::1])
            item = self.mainCharacter.getItem(itemName)
            if item != None:
                if isinstance(item, IHeal):
                    self.mainCharacter.health += item.heal
                    self.mainCharacter.health = self.mainCharacter.getMaxHealth() if self.mainCharacter.health > self.mainCharacter.getMaxHealth() else self.mainCharacter.health
                    print(f'{self.mainCharacter.getStatusColor(100, 100)}{self.mainCharacter.name}{Style.RESET_ALL} использовал {self.mainCharacter.getOptionColor()}{item.name}{Style.RESET_ALL} и восполнил {item.heal} здоровья')
                    
        elif self.message == 'сделать шаг':
            self.location.step()

            self.hasEnemy = self.location.enemies.getItemsCount() > 0
            
            if self.location.curr_pos == 2:
                self.location.addItem(SmallHealPotion())
            if self.location.curr_pos == 5:
                self.location.addItem(HealPotion())
            if self.location.curr_pos == 8:
                self.location.addItem(SmallHealPotion())
            if self.location.curr_pos == 10:
                self.location.addItem(Knife())
            if self.location.curr_pos == 15 and self.hasEnemy == False:
                self.location.addEnemy(Guard())
                
        elif self.message == 'осмотреться' or self.message == 'осм':
            self.location.lookAround(self.mainCharacter)
            
        elif self.message.split(' ')[0] == 'подобрать' or self.message.split(' ')[0] == 'под':
            itemName = ' '.join(self.message.split(' ')[1::1])
            item = self.location.getItem(itemName)
            if item != None:
                self.mainCharacter.inventory.addItem(item)
                
        elif self.message.split(' ')[0] == 'экипировать' or self.message.split(' ')[0] == 'экип':
            itemName = ' '.join(self.message.split(' ')[1::1])
            self.mainCharacter.equip(itemName)
            
        elif self.message.split(' ')[0] == 'атаковать' or self.message.split(' ')[0] == 'атак':
            if self.location.enemies.getItemsCount() <= 0:
                print('Сейчас врагов нет')
                return
            
            itemName = ' '.join(self.message.split(' ')[1::1])
            currAttack = self.mainCharacter.getAttack() * rnd.randint(0, 10)
            currAttackEnemy = self.location.enemies.items[itemName]['item'].attack * rnd.randint(0, 10)
            self.location.enemies.attackEnemy(itemName, currAttack)
            self.mainCharacter.health -= currAttackEnemy
            
            print(f'{self.mainCharacter.getStatusColor(100, 100)}{self.mainCharacter.name}{Style.RESET_ALL} атаковал {self.mainCharacter.getStatusColor(0, 100)}{itemName}{Style.RESET_ALL} и нанес ему {self.mainCharacter.getStatusColor(0, 100)}{currAttack}{Style.RESET_ALL} урона')
            print(f'{self.mainCharacter.getStatusColor(0, 100)}{itemName}{Style.RESET_ALL} атаковал {self.mainCharacter.getStatusColor(100, 100)}{self.mainCharacter.name}{Style.RESET_ALL} и нанес ему {self.mainCharacter.getStatusColor(0, 100)}{currAttackEnemy}{Style.RESET_ALL} урона')
            
        else:
            print(f'{self.mainCharacter.getStatusColor(100, 100)}{self.mainCharacter.name}{Style.RESET_ALL} не понял что он должен делать и стоит в недоумении')
            
        if self.mainCharacter.health <= 0:
            print(f'{Fore.WHITE}{Back.RED}ВЫ ПОГИБЛИ{Style.RESET_ALL}')
            self.isRunning = False
            
game = DnD_Game()

game.run()