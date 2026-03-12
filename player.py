# player.py

class Player:
    def __init__(self):
        self.flag_position = None
        self.walls = set()

        self.build_mode = False
        self.remove_mode = False
        self.move_flag_mode = False

        self.max_walls = 25

    # FLAG
    def set_flag(self, position):
        if position not in self.walls:
            self.flag_position = position

    def get_flag(self):
        return self.flag_position

    def draw_flag(self, surface, draw_tile_func, color):
        if self.flag_position:
            draw_tile_func(surface, *self.flag_position, color)

    # MODES
    def toggle_build_mode(self):
        self.build_mode = not self.build_mode
        self.remove_mode = False
        self.move_flag_mode = False

    def toggle_remove_mode(self):
        self.remove_mode = not self.remove_mode
        self.build_mode = False
        self.move_flag_mode = False

    def toggle_move_flag_mode(self):
        self.move_flag_mode = not self.move_flag_mode
        self.build_mode = False
        self.remove_mode = False

    def disable_modes(self):
        self.build_mode = False
        self.remove_mode = False
        self.move_flag_mode = False

    # WALLS
    def add_wall(self, position, start=None):
        if len(self.walls) >= self.max_walls:
            return

        if position == self.flag_position:
            return

        if start and position == start:
            return

        self.walls.add(position)

    def remove_wall(self, position):
        if position in self.walls:
            self.walls.remove(position)

    def get_walls(self):
        return self.walls

    def draw_walls(self, surface, draw_tile_func):
        for wall in self.walls:
            draw_tile_func(surface, *wall, (90, 90, 90))