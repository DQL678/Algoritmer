class Player:
    def __init__(self):
        self.flag_position = None
        self.walls = set()
        self.wall_mode = False

    # -------- FLAG --------
    def set_flag(self, position):
        self.flag_position = position

    def get_flag(self):
        return self.flag_position

    def draw_flag(self, surface, draw_tile_func, color):
        if self.flag_position is not None:
            draw_tile_func(surface, *self.flag_position, color)

    # -------- WALLS --------
    def toggle_wall_mode(self):
        self.wall_mode = not self.wall_mode

    def add_wall(self, position):
        # Man må ikke placere væg ovenpå flag
        if position != self.flag_position:
            self.walls.add(position)

    def get_walls(self):
        return self.walls

    def draw_walls(self, surface, draw_tile_func):
        for wall in self.walls:
            draw_tile_func(surface, *wall, (70, 70, 70))  # mørkegrå vægge
