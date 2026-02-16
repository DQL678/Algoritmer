class Player:
    def __init__(self):
        self.flag_position = None

    def set_flag(self, position):
        self.flag_position = position

    def get_flag(self):
        return self.flag_position

    def draw_flag(self, surface, draw_tile_func, color):
        if self.flag_position is not None:
            draw_tile_func(surface, *self.flag_position, color)
