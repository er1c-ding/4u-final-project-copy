import Entity
import random
import os

class World:
    def __init__(self):
        self.__world = [[None for i in range(40)] for i in range(20)]
        self.__tick = 0

        prev = False
        for i in range(20):
            for j in range(40):
                if prev:
                    prev = False
                else:
                    rand = random.randint(1,100)
                    
                    # Random spawner. Fills the world.
                    if rand > 59:
                        if rand < 70:
                          self.__world[i][j] = Entity.Human()
                        elif rand < 80:
                            self.__world[i][j] = Entity.Food()
                        elif rand < 85:
                            self.__world[i][j] = Entity.Settlement()
                        elif rand < 90:
                            self.__world[i][j] = Entity.Mine()
                        else:
                            self.__world[i][j] = Entity.Forest()
                        prev = True
    
    def transfer_stuff(self, human, resource):
        """
        This function calculates the current score and blits it

        Parameters:
        human (Human): Human object accepting resources.
        resource (Entity): Food, Forest, or Mine object giving resources.

        Returns:
        N/A
        """
        if resource.symbol in ["🍖","🍈","🍎"]:
            human.eat(resource.eat())
        elif resource.symbol in ["🌲","🌳","🌱"]:
            human.recieve_wood(resource.chop())
        elif resource.symbol in ["💎","⛏️ ","🪨 "]:
            human.recieve_minerals(resource.mine())
    
    def settlement_transfers(self, human, settlement):
        """
        Transfers resources between Human objects and Settlement objects. Upgrades Settlement objects after
        transfer if needed.
        
        Parameters:
        human (Human): Human object that will give resources.
        settlement (Settlement): Settlement object that will accept resources.

        Returns:
        N/A
        """
        if settlement.symbol in ["🔨","🏠","🏡","🏘️ ","🏢","🏙️ "]:
            settlement.recieve_resources(human.transfer_resources())
            settlement.upgrade()

    def run(self):
        """
        Executes one tick.

        Parameters:
        N/A

        Returns:
        N/A
        """
        deaths = 0
        births = 0
        self.__tick += 1

        # Changes changed_moved into False for all humans so that they can be moved
        for arr in self.__world:
            for entity in arr:
                if entity != None and entity.symbol in ["👶","👦","👧","👨","👩","👴","👵"] and entity.moved == True:
                    entity.changed_moved()

        for i in range(20):
            for j in range(40):
                if self.__world[i][j] != None:
                    if self.__world[i][j].symbol in ["👶","👦","👧","👨","👩","👴","👵"] and self.__world[i][j].moved == False:
                        self.__world[i][j].changed_moved() # Ensures humans aren't moved twice
                        self.__world[i][j].update_tick()

                        # Resource transfer between resources and humans
                        if i != 0 and not self.__world[i - 1][j] == None:
                            self.transfer_stuff(self.__world[i][j], self.__world[i - 1][j])

                        if i != 19 and not self.__world[i + 1][j] == None:
                            self.transfer_stuff(self.__world[i][j], self.__world[i + 1][j])

                        if j != 0 and not self.__world[i][j - 1] == None:
                            self.transfer_stuff(self.__world[i][j], self.__world[i][j - 1])

                        if j != 39 and not self.__world[i][j + 1] == None:
                            self.transfer_stuff(self.__world[i][j], self.__world[i][j + 1])

                        # Resource transfer between humans and settlements
                        if i != 0 and not self.__world[i - 1][j] == None:
                            self.settlement_transfers(self.__world[i][j], self.__world[i - 1][j])

                        if i != 19 and not self.__world[i + 1][j] == None:
                            self.settlement_transfers(self.__world[i][j], self.__world[i + 1][j])

                        if j != 0 and not self.__world[i][j - 1] == None:
                            self.settlement_transfers(self.__world[i][j], self.__world[i][j - 1])

                        if j != 39 and not self.__world[i][j + 1] == None:
                            self.settlement_transfers(self.__world[i][j], self.__world[i][j + 1])

                        # Tests for human deaths
                        if self.__world[i][j].will_survive() == False:
                            self.__world[i][j] = None
                            deaths += 1
                            continue
                        
                        # Movement of humans
                        north = i != 0 and self.__world[i - 1][j] == None
                        south = i != 19 and self.__world[i + 1][j] == None
                        west = j != 0 and self.__world[i][j - 1] == None
                        east = j != 39 and self.__world[i][j + 1] == None
                        arr = ["North" if north == True else None, "South" if south == True else None, 
                            "West" if west == True else None, "East" if east == True else None]
                            
                        for k in range(arr.count(None)):
                            arr.remove(None)
                            
                        if len(arr) == 0:
                            continue

                        rand = random.randint(0, len(arr))

                        if rand == len(arr):
                            continue
                            
                        if arr[rand] == "North":
                            self.__world[i - 1][j] = self.__world[i][j]
                        elif arr[rand] == "South":
                            self.__world[i + 1][j] = self.__world[i][j]
                        elif arr[rand] == "West":
                            self.__world[i][j - 1] = self.__world[i][j]
                        else:
                            self.__world[i][j + 1] = self.__world[i][j]
                 
                        self.__world[i][j] = None

                    elif self.__world[i][j].symbol in ["🍖","🍈","🍎","🌲","🌳","🌱","💎","⛏️ ","🪨 "]:
                        self.__world[i][j].update_tick()

                    elif self.__world[i][j].symbol in ["🔨","🏠","🏡","🏘️ ","🏢","🏙️ "]:
                        north = i != 0 and self.__world[i - 1][j] == None
                        south = i != 19 and self.__world[i + 1][j] == None
                        west = j != 0 and self.__world[i][j - 1] == None
                        east = j != 39 and self.__world[i][j + 1] == None
                        arr = [north, south, west, east]
                        
                        for k in range(self.__world[i][j].num_new_humans()):
                            if len(arr) == 0 or arr.count(True) == 0:
                                continue
                            
                            births += 1
                            index = 0

                            while arr[index] == False:
                                index += 1

                            arr[index] = False

                            if index == 0:
                                self.__world[i - 1][j] = Entity.Human()
                                self.__world[i - 1][j].changed_moved()
                            elif index == 1:
                                self.__world[i + 1][j] = Entity.Human()
                                self.__world[i + 1][j].changed_moved()
                            elif index == 2:
                                self.__world[i][j - 1] = Entity.Human()
                                self.__world[i][j - 1].changed_moved()
                            else:
                                self.__world[i][j + 1] = Entity.Human()
                                self.__world[i][j + 1].changed_moved()
                            
        os.system('cls')
        self.__draw(deaths, births)

    def __draw(self, deaths, births):
        """
        Displays the world array in the command line UI, the population of Human objects, the current tick, 
        and the amount of deaths and births that occured that tick.
        
        Parameters:
        deaths (int): Number of deaths this tick
        births (int): Number of births this tick

        Returns:
        N/A
        """
        print(f"Tick: {self.__tick}")
        print(f"This turn, there was {deaths} death(s) and {births} birth(s).")
        print(f"Population of Humans: {Entity.Human.get_population()}")

        for i in range(20):
            for j in range(40):
                if self.__world[i][j] == None:
                    print(" -", end=" ")
                else:
                    print(self.__world[i][j].symbol, end=" ")
            print(" ")

    @property
    def tick(self):
        return self.__tick