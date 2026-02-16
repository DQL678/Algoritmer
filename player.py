# player.py

class Player:
    def __init__(self):
        self.flag_position = None
        self.walls = set()

        # Modes
        self.build_mode = False
        self.remove_mode = False

    # -----------------
    # FLAG
    # -----------------
    def set_flag(self, position):
        if position not in self.walls:
            self.flag_position = position

    def get_flag(self):
        return self.flag_position

    def draw_flag(self, surface, draw_tile_func, color):
        if self.flag_position:
            draw_tile_func(surface, *self.flag_position, color)

    # -----------------
    # WALLS
    # -----------------
    def enable_build_mode(self):
        self.build_mode = True
        self.remove_mode = False

    def enable_remove_mode(self):
        self.remove_mode = True
        self.build_mode = False

    def disable_modes(self):
        self.build_mode = False
        self.remove_mode = False

    def add_wall(self, position):
        if position != self.flag_position:
            self.walls.add(position)

    def remove_wall(self, position):
        if position in self.walls:
            self.walls.remove(position)

    def get_walls(self):
        return self.walls

    def draw_walls(self, surface, draw_tile_func):
        for wall in self.walls:
            draw_tile_func(surface, *wall, (90, 90, 90))
