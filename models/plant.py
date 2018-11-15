import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1
        self.map = map
        self.max_hp = config['plants'].getint('max_hp')
        self.current_hp = self.max_hp
        self.max_level = config['plants'].getint('max_level')
        self.hp_increment = self.max_level

    def update(self):
        self.level_up()

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        # Check if the plant levels up
        do_level_up = 0

        level_up_chance = random.randint(0,self.max_level*10)
        if level_up_chance > self.level:
            level_up_chance = random.randint(0,self.max_level*10)
            if level_up_chance > self.level:
                level_up_chance = random.randint(0,self.max_level*2)
                if level_up_chance > self.level:
                    do_level_up = 1

        # If the plant levels up do the following
        if do_level_up:
            self.level += 1

            # Change max hp on level up
            self.max_hp += self.hp_increment

<<<<<<< HEAD
            # Add hp on level up
            self.current_hp += self.max_hp//2
            if self.current_hp >= self.max_hp:
                self.current_hp = self.max_hp

    def seed_check(self):
        # Check if the plant is level 20
        if self.level == self.max_level:
            self.ready_to_seed = 1
            print("plant",self.id,"is ready to seed ;)")

=======
            # Add hp on level up, not exceeding max
            self.current_htp = min(self.current_hp + self.max_hp//2, self.max_hp)
>>>>>>> 406deaf0033b25333692e814d5b15408b855c949

    def ready_to_seed(self):
        return self.level == self.max_level
