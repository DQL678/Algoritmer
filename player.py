# player.py

class Player:
    def __init__(self):
        self.flag_position = None
        self.walls = set()
        self.wall_mode = False  # False = placer flag, True = placer vægge

    # -------------------------
    # FLAG
    # -------------------------
    def set_flag(self, position):
        if position not in self.walls:  # Flag må ikke placeres på væg
            self.flag_position = position

    def get_flag(self):
        return self.flag_position

    def draw_flag(self, surface, draw_tile_func, color):
        if self.flag_position:
            draw_tile_func(surface, *self.flag_position, color)

    # -------------------------
    # WALLS
    # -------------------------
    def toggle_wall_mode(self):
        self.wall_mode = not self.wall_mode

    def add_wall(self, position):
        if position != self.flag_position:
            if position in self.walls:
                self.walls.remove(position)  # klik igen fjerner væg
            else:
                self.walls.add(position)

    def get_walls(self):
        return self.walls

    def draw_walls(self, surface, draw_tile_func):
        for wall in self.walls:
            draw_tile_func(surface, *wall, (90, 90, 90))
