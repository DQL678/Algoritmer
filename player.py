# player.py

class Player:
    def __init__(self):
        self.flag_position = None
        self.walls = set()

        # Modes
        self.build_mode = False
        self.remove_mode = False
        self.move_flag_mode = True  # start med at kunne placere/flytte flag

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
    # MODES
    # -----------------
    def enable_build_mode(self):
        self.build_mode = True
        self.remove_mode = False
        self.move_flag_mode = False

    def enable_remove_mode(self):
        self.remove_mode = True
        self.build_mode = False
        self.move_flag_mode = False

    def enable_move_flag_mode(self):
        self.move_flag_mode = True
        self.build_mode = False
        self.remove_mode = False

    def disable_modes(self):
        self.build_mode = False
        self.remove_mode = False
        self.move_flag_mode = False

    def toggle_build_mode(self):
        if self.build_mode:
            self.disable_modes()
        else:
            self.enable_build_mode()

    def toggle_remove_mode(self):
        if self.remove_mode:
            self.disable_modes()
        else:
            self.enable_remove_mode()

    def toggle_move_flag_mode(self):
        if self.move_flag_mode:
            self.disable_modes()
        else:
            self.enable_move_flag_mode()

    # -----------------
    # WALLS
    # -----------------
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