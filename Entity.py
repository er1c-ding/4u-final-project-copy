import random

class Entity:
    def __init__(self, symbol):
        self.__symbol = symbol
    
    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def _symbol(self, new_symbol):
        self.__symbol = new_symbol

class Food(Entity):
    def __init__(self):
        self.__supply_max = random.randint(5, 10)
        self.__supply_left = self.__supply_max

        if self.__supply_max > 8:
            super().__init__("🍖")

        elif self.__supply_max > 6:
            super().__init__("🍈")

        else:
            super().__init__("🍎")
    
    def eat(self):
        """
        Adjusts food supply value to give resources to another object.
        
        Parameters:
        N/A

        Returns:
        int: Amount of food this object gave.
        """
        if self.__supply_left > 0:
            self.__supply_left -= 1
            return 1
        else:
            return 0

    def update_tick(self):
        """
        Regenerates resources.

        Parameters:
        N/A

        Returns:
        N/A
        """
        self.__supply_left += random.randint(2,4)
        if self.__supply_left > self.__supply_max:
            self.__supply_left = self.__supply_max

class Forest(Entity):
    def __init__(self):
        self.__wood_max = random.randint(10, 20)
        self.__wood_left = self.__wood_max

        if self.__wood_max > 16:
            super().__init__("🌲")
        
        elif self.__wood_max > 12:
            super().__init__("🌳")
        
        else:
            super().__init__("🌱")
    
    def chop(self):
        """
        Adjusts resource wood supply value to give resources to another object.

        Parameters:
        N/A

        Returns:
        int: Amount of wood this object gave.
        """
        rand_num = random.randint(2,3)
        original_wood_left = self.__wood_left
        self.__wood_left -= rand_num

        if self.__wood_left < 0:
            self.__wood_left = 0
            return original_wood_left
        
        return rand_num

    def update_tick(self):
        """
        Regenerates resources.

        Parameters:
        N/A

        Returns:
        N/A
        """
        self.__wood_left += random.randint(2,3)
        if self.__wood_left > self.__wood_max:
            self.__wood_left = self.__wood_max

class Mine(Entity):
    def __init__(self):
        self.__stone_max = random.randint(10, 20)
        self.__iron_max = random.randint(5, 10)
        self.__stone_left = self.__stone_max
        self.__iron_left = self.__iron_max

        if self.__stone_max > 16:
            super().__init__("💎")
        
        elif self.__stone_max > 12:
            super().__init__("⛏️ ")
        
        else:
            super().__init__("🪨 ")
    
    def mine(self):
        """
        Adjusts current resource stone and iron supply values to give resources to another object.

        Parameters:
        N/A

        Return:
        list: Amounts of stone and iron this object gave.
        """
        rand_num = random.randint(1,2)
        original_stone_left = self.__stone_left
        original_iron_left = self.__iron_left
        self.__stone_left -= rand_num * 2
        self.__iron_left -= rand_num

        if self.__stone_left < 0:
            self.__stone_left = 0
            first = original_stone_left
        else:
            first = rand_num * 2
        
        if self.__iron_left < 0:
            self.__iron_left = 0
            second = original_iron_left
        else:
            second = rand_num

        return [first, second]

    def update_tick(self):
        """
        Regenerates resource supply.

        Parameters:
        N/A

        Returns:
        N/A
        """
        self.__stone_left += random.randint(3,5)
        self.__iron_left += random.randint(1,2)

        if self.__stone_left > self.__stone_max:
            self.__stone_left = self.__stone_max
        if self.__iron_left > self.__iron_max:
            self.__iron_left = self.__iron_max

class Human(Entity):
    __population = 0

    def __init__(self):
        self.__hunger = 100
        self.__wood = 0
        self.__stone = 0
        self.__iron = 0
        self.__age = 0
        self.__moved = False # indicates whether this object has been moved this tick
        super().__init__("👶")

        randint = random.randint(1, 2)
        if randint == 1:
            self.__gender = "Female"
        if randint == 2:
            self.__gender = "Male"
        
        Human.__population += 1
    
    def will_survive(self):
        """
        Returns whether the Human object will survive this tick.

        Parameters:
        N/A

        Returns:
        boolean: Whether the Human object will survive this tick.
        """
        if self.__hunger == 0:
            Human.__population -= 1
            return False

        chance_disease = int(Human.__population/10)
        rand = random.randint(1,100)
        if rand < chance_disease:
            Human.__population -= 1
            return False
        
        chance_aging = int(self.__age / 2)
        rand = random.randint(1,100)
        if self.__age > 55 and rand < chance_aging:
            Human.__population -= 1
            return False
        
        return True

    def update_tick(self):
        """
        Ages the Human object by one tick and decreases hunger value to simulate aging and hunger.

        Parameters:
        N/A

        Returns:
        N/A
        """
        self.__age += 1
        self.__hunger -= 10

        if self.__gender == "Female":
            if self.__age == 6:
                self._symbol = "👧"
            if self.__age == 16:
                self._symbol = "👩"
            if self.__age == 60:
                self._symbol = "👵"
        
        if self.__gender == "Male":
            if self.__age == 6:
                self._symbol = "👦"
            if self.__age == 16:
                self._symbol = "👨"
            if self.__age == 60:
                self._symbol = "👴"

    def transfer_resources(self):
        """
        Adjusts current resource supply values to give resources to another object.

        Parameters:
        N/A

        Returns:
        list: Amounts of resources this Human object gave.
        """
        original_wood = self.__wood
        self.__wood = 0
        original_stone = self.__stone
        self.__stone = 0
        original_iron = self.__iron
        self.__iron = 0

        return [original_wood, original_stone, original_iron]

    def recieve_minerals(self, values):
        """
        Adjusts values of iron and stone supply to accept iron and stone.

        Parameters:
        values (list): Amounts of resources to accept.

        Returns:
        N/A
        """
        self.__stone += values[0]
        self.__iron += values[1]

    def recieve_wood(self, value):
        """
        Adjusts value of wood supply to accept wood.

        Parameters:
        value (int): Amount of wood this Human object is accepting.

        Returns:
        N/A
        """
        self.__wood += value

    def eat(self, num):
        """
        Adjusts hunger values to eat food. 

        Parameters:
        num (int): Amount of food this Human object has eaten.

        Returns:
        N/A
        """
        if num == 1:
            self.__hunger = 100

    def changed_moved(self):
        """
        Changes value of __moved to indicate whether this object has been moved this turn.
        
        Parameters:
        N/A

        Returns:
        N/A
        """
        self.__moved = not self.__moved
    
    @property
    def moved(self):
        return self.__moved
    
    @classmethod
    def get_population(cls):
        return cls.__population
    
class Settlement(Entity):
    def __init__(self):
        self.__curr_wood = 0
        self.__curr_stone = 0
        self.__curr_iron = 0
        self.__level = 0
        super().__init__("🔨")
    
    def recieve_resources(self, values):
        """
        Adjusts current resource supply values accordingly to accept resources.
        
        Parameters:
        values (list): Amounts of resources to accept.

        Returns:
        N/A
        """
        self.__curr_wood += values[0]
        self.__curr_stone += values[1]
        self.__curr_iron += values[2]

    def num_new_humans(self):
        """
        Returns the number of Human objects to be created by this Settlement object.
        
        Parameters:
        N/A

        Returns:
        int: Number of Human objects to be created by this Settlement object.
        """
        if Human.get_population() >= 100 or Human.get_population() < 2:
            return 0
        
        rand = random.randint(1,10)

        if self.__level == 0:
            if rand == 1:
                return 1
        if self.__level == 1:
            if rand < 3:
                return 1
        if self.__level == 2:
            if rand < 6:
                return 1
        if self.__level == 3:
            if rand == 1 and Human.get_population() < 99:
                return 2
            else:
                return 1
        if self.__level == 4:
            if rand < 3 and Human.get_population() < 99:
                return 2
            else:
                return 1
        if self.__level == 5:
            if rand < 6 and Human.get_population() < 99:
                return 2
            else:
                return 1
        
        return 0

    def upgrade(self):
        """
        Upgrades the Settlement object if it has sufficient resources.

        Parameters:
        N/A

        Returns:
        N/A
        """
        min_req = [[10, 0, 0], [15, 10, 0], [75, 50, 0], [75, 100, 25], [1000, 1000, 250]]
        emojis = ["🏠","🏡", "🏘️ ", "🏢", "🏙️ "]
        if (self.__level < 5 
            and self.__curr_wood >= min_req[self.__level][0] 
            and self.__curr_stone >= min_req[self.__level][1] 
            and self.__curr_iron >= min_req[self.__level][2]):
            self._symbol = emojis[self.__level]
            self.__level += 1 