import random

EDIBILITY = 40
VALUE_FOOD = 20
SUPERFOOD_MULTIPLIER = 4

MAP_SIZE = 10
FOOD_SPAWN = 10
FOOD_SPAWN_AREAS = None
FOOD_COUNT_SPAWN = 20
BOT_SPAWN = 1
BOT_SPAWN_AREAS = None
BOT_COUNT_SPAWN = 1

POWER_POISON = 10
WASTE_LIFE = 10

CHANCE_MUTATE = 20
HP_BOT = 50
ATTACK_BOT = 40
OLD_BOT = 1
UNMOUNTING_BOT = 70


class Map:
    def __init__(self) -> None:
        self.field = [[Point(x, y, self) for y in range(MAP_SIZE)] for x in range(MAP_SIZE)]
        self.time = 0
        self.bots = []
        self.leads = []

    def update_bots_list(self, bot):
        for bot_ in self.bots:
            if bot_.x == bot.x and bot_.y == bot.y:
                return
        self.bots.append(bot)
        self.bots.sort(key=lambda x: x.score)
        if len(self.bots) >= 60:
            self.bots.pop(0)

    def add_leads(self, name, chromosome, color, score):

        bot = Bot(0, 0)
        bot.chromosome = chromosome
        bot.color = color
        bot.name = name
        bot.score = score
        self.leads.append(bot)

    def del_leads(self, name, score):
        for i, el in enumerate(self.leads):
            if el.name == name and el.score == score:
                self.leads.pop(i)
                break

    def food_destruction(self, x, y):
        self.field[x][y] = Waste(x, y, self)

    def waste_destruction(self, x, y):
        self.field[x][y] = Point(x, y, self)

    def bot_death(self, x, y):
        self.field[x][y] = SuperFood(x, y, self)

    def print(self):
        print()
        print(self.time)
        print(*self.field, sep="\n")

    def delete(self, x, y):
        p = self.field[x][y]
        self.field[x][y] = Point(x, y, self)
        return p

    def add(self, x, y, obj):
        obj.map_ = self
        obj.x = x
        obj.y = y
        self.field[x][y] = obj

    def relocate(self, x1, y1, x2, y2):
        self.add(x2, y2, self.delete(x1, y1))

    def get_bot_sees_all(self, x, y, alpha):
        if alpha == 0:
            return self.field[(x + 1) % MAP_SIZE][y], self.field[(x + 2) % MAP_SIZE][y]
        if alpha == 1:
            return self.field[x][(y + 1) % MAP_SIZE], self.field[x][(y + 2) % MAP_SIZE]
        if alpha == 2:
            return self.field[(x - 1) % MAP_SIZE][y], self.field[(x - 2) % MAP_SIZE][y]
        if alpha == 3:
            return self.field[x][(y - 1) % MAP_SIZE], self.field[x][(y - 2) % MAP_SIZE]

    def get_bot_sees_first(self, x, y, alpha):
        if alpha == 0:
            return self.field[(x + 1) % MAP_SIZE][y]
        if alpha == 1:
            return self.field[x][(y + 1) % MAP_SIZE]
        if alpha == 2:
            return self.field[(x - 1) % MAP_SIZE][y]
        if alpha == 3:
            return self.field[x][(y - 1) % MAP_SIZE]

    def step(self, is_leads=False):
        lst = [a for b in self.field for a in b]
        if FOOD_SPAWN_AREAS is None:
            count = 0
            for e in lst:
                if str(e.__class__.__name__) in ["Food", "SuperFood"]:
                    count += 1
            if count / (MAP_SIZE * MAP_SIZE) * 100 < FOOD_SPAWN:
                for _ in range(FOOD_COUNT_SPAWN):
                    random.shuffle(lst)
                    for e in lst:
                        if str(e.__class__.__name__) == "Point":
                            self.add(e.x, e.y, Food())
                            break

        else:
            ...  # доделать

        if BOT_SPAWN_AREAS is None:
            count = 0
            for e in lst:
                if str(e.__class__.__name__) == "Bot":
                    count += 1
            if count / (MAP_SIZE * MAP_SIZE) * 100 < BOT_SPAWN:
                for _ in range(BOT_COUNT_SPAWN):
                    random.shuffle(lst)
                    for e in lst:
                        if str(e.__class__.__name__) == "Point":
                            bot = Bot()
                            if is_leads and len(self.leads) > 0:
                                bot = random.choice(self.leads)
                                self.add(e.x, e.y, Bot(chromosome=bot.chromosome, color=bot.color))
                            else:
                                self.add(e.x, e.y, bot)
                            break

        else:
            ...  # доделать

        self.time += 1
        lst = [a for b in self.field for a in b]
        random.shuffle(lst)
        for e in lst:
            if str(e.__class__.__name__) in ["Point", "Wall"]:
                continue
            if str(e.__class__.__name__) in ["Food", "SuperFood"]:
                e.deteriorate()
                continue
            if str(e.__class__.__name__) == "Waste":
                # доделать яд
                e.deteriorate()
                continue
            if str(e.__class__.__name__) == "Bot":
                self.update_bots_list(e)
                if e.hp >= UNMOUNTING_BOT:
                    e.hp -= UNMOUNTING_BOT - HP_BOT
                    e.score += 50
                    lst_xy = [[(e.x + 1) % MAP_SIZE, e.y],
                              [(e.x - 1) % MAP_SIZE, e.y],
                              [e.x, (e.y + 1) % MAP_SIZE],
                              [e.x, (e.y - 1) % MAP_SIZE],
                              [(e.x + 1) % MAP_SIZE, (e.y + 1) % MAP_SIZE],
                              [(e.x - 1) % MAP_SIZE, (e.y + 1) % MAP_SIZE],
                              [(e.x + 1) % MAP_SIZE, (e.y - 1) % MAP_SIZE],
                              [(e.x - 1) % MAP_SIZE, (e.y - 1) % MAP_SIZE]]
                    random.shuffle(lst_xy)
                    for x, y in lst_xy:
                        if str(self.field[x][y].__class__.__name__) == "Point":
                            bot = Bot(chromosome=e.chromosome, color=e.color)
                            self.add(x, y, bot)
                            break
                    continue
                e.brain()
                if e.hp <= 0:
                    self.bot_death(e.x, e.y)


class Point:
    def __init__(self, x, y, map_: Map) -> None:
        self.x: int = x
        self.y: int = y
        self.map_ = map_

    def __str__(self) -> str:
        return str(self.__class__.__name__) + f": {self.x} ; {self.y} "

    def __repr__(self) -> str:
        return str(self.__class__.__name__) + f": {self.x} {self.y} "


class Food(Point):
    def __init__(self, x=0, y=0, map_: Map = None) -> None:
        super().__init__(x, y, map_)
        self.edibility = EDIBILITY

    def deteriorate(self):
        self.edibility -= 1
        if self.edibility <= 0:
            self.map_.food_destruction(self.x, self.y)


class SuperFood(Food):
    def __init__(self, x, y, map_: Map) -> None:
        super().__init__(x, y, map_)
        self.edibility *= SUPERFOOD_MULTIPLIER


class Waste(Point):
    def __init__(self, x, y, map_: Map) -> None:
        super().__init__(x, y, map_)
        self.power_poison = POWER_POISON
        self.waste_life = WASTE_LIFE

    def deteriorate(self):
        self.waste_life -= 1
        if self.waste_life <= 0:
            self.map_.waste_destruction(self.x, self.y)


class Bot(Point):
    @staticmethod
    def generate_chromosome():
        return [[random.randint(0, 49) for _ in range(6 ** 2)] for _ in range(50)]

    @staticmethod
    def mutate_chromosome(chromosome):
        new_chromosome = []
        for a in chromosome:
            n_a = []
            for ax in a:
                if random.randint(0, 100) <= CHANCE_MUTATE:
                    n_a.append(random.randint(0, 49))
                else:
                    n_a.append(ax)
            new_chromosome.append(n_a)
        return new_chromosome

    def __init__(self, x=0, y=0, map_: Map = None, chromosome=None, index=0, alpha=random.randint(0, 3),
                 hp=HP_BOT, color=None, id=None) -> None:
        super().__init__(x, y, map_)

        if chromosome is None:
            self.chromosome = self.generate_chromosome()
        else:
            self.chromosome = self.mutate_chromosome(chromosome)

        self.index = index
        self.alpha = alpha
        self.hp = hp
        self.score = 0
        self.name = ""

        if color is None:
            self.color = [random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)]
        else:
            r = random.randint(1, 3)
            if r == 1:
                self.color = [(color[0] + 1) % 255] + color[1:]
            elif r == 2:
                self.color = [color[0]] + [(color[1] + 1) % 255] + [color[2]]
            if r == 3:
                self.color = color[:-1] + [(color[2] + 1) % 255]

    def get_indexD(self): 
        s1, s2 = self.map_.get_bot_sees_all(self.x, self.y, self.alpha)
        s1 = str(s1.__class__.__name__)
        s2 = str(s2.__class__.__name__)
        if s1 == "Bot":
            if s2 == "Bot":
                return 0
            if s2 == "Food":
                return 1
            if s2 == "SuperFood":
                return 2
            if s2 == "Waste":
                return 3
            if s2 == "Point":
                return 4
            if s2 == "Wall":
                return 5
        if s1 == "Food":
            if s2 == "Bot":
                return 6
            if s2 == "Food":
                return 7
            if s2 == "SuperFood":
                return 8
            if s2 == "Waste":
                return 9
            if s2 == "Point":
                return 10
            if s2 == "Wall":
                return 11
        if s1 == "SuperFood":
            if s2 == "Bot":
                return 12
            if s2 == "Food":
                return 13
            if s2 == "SuperFood":
                return 14
            if s2 == "Waste":
                return 15
            if s2 == "Point":
                return 16
            if s2 == "Wall":
                return 17
        if s1 == "Waste":
            if s2 == "Bot":
                return 18
            if s2 == "Food":
                return 19
            if s2 == "SuperFood":
                return 20
            if s2 == "Waste":
                return 21
            if s2 == "Point":
                return 22
            if s2 == "Wall":
                return 23
        if s1 == "Point":
            if s2 == "Bot":
                return 24
            if s2 == "Food":
                return 25
            if s2 == "SuperFood":
                return 26
            if s2 == "Waste":
                return 27
            if s2 == "Point":
                return 28
            if s2 == "Wall":
                return 29
        if s1 == "Wall":
            if s2 == "Bot":
                return 30
            if s2 == "Food":
                return 31
            if s2 == "SuperFood":
                return 32
            if s2 == "Waste":
                return 33
            if s2 == "Point":
                return 34
            if s2 == "Wall":
                return 35

    def step(self):
        v = self.map_.get_bot_sees_first(self.x, self.y, self.alpha).__class__.__name__
        if not str(v) == "Point":
            if not str(v) == "Waste":
                return
            else:
                self.hp -= POWER_POISON

        if self.alpha == 0:
            self.map_.relocate(self.x, self.y, (self.x + 1) % MAP_SIZE, self.y)
        elif self.alpha == 1:
            self.map_.relocate(self.x, self.y, self.x, (self.y + 1) % MAP_SIZE)
        elif self.alpha == 2:
            self.map_.relocate(self.x, self.y, (self.x - 1) % MAP_SIZE, self.y)
        elif self.alpha == 3:
            self.map_.relocate(self.x, self.y, self.x, (self.y - 1) % MAP_SIZE)

    def turn(self, right=False):
        if right:
            self.alpha = (self.alpha - 1) % 4
        else:
            self.alpha = (self.alpha + 1) % 4

    def eat(self):
        def func_del_food():
            if self.alpha == 0:
                self.map_.delete((self.x + 1) % MAP_SIZE, self.y)
            elif self.alpha == 1:
                self.map_.delete(self.x, (self.y + 1) % MAP_SIZE)
            elif self.alpha == 2:
                self.map_.delete((self.x - 1) % MAP_SIZE, self.y)
            elif self.alpha == 3:
                self.map_.delete(self.x, (self.y - 1) % MAP_SIZE)

        v = str(self.map_.get_bot_sees_first(self.x, self.y, self.alpha).__class__.__name__)
        if v == "Food":
            self.hp += VALUE_FOOD
            func_del_food()

        elif v == "SuperFood":
            self.hp += VALUE_FOOD * SUPERFOOD_MULTIPLIER
            func_del_food()

    def attack(self):
        v = self.map_.get_bot_sees_first(self.x, self.y, self.alpha)
        if str(v.__class__.__name__) == "Bot":
            v.hp -= ATTACK_BOT
            if v.hp <= 0:
                self.map_.bot_death(v.x, v.y)

    def brain(self):
        self.index = self.chromosome[self.index][self.get_indexD()]

        if 0 <= self.index < 10:
            self.step()
        elif 10 <= self.index < 20:
            self.turn()
        elif 20 <= self.index < 30:
            self.turn(right=True)
        elif 30 <= self.index < 40:
            self.eat()
        elif 40 <= self.index < 50:
            self.attack()

        self.hp -= OLD_BOT
        self.score += 1


class Wall(Point):
    def __init__(self, x, y, map_: Map) -> None:
        super().__init__(x, y, map_)
