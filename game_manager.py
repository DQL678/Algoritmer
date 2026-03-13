# game_manager.py

class GameManager:
    def __init__(self):
        self.difficulty = "hard"
        self.level = 1
        self.creative_mode = False

        # Level data: step limit + max walls
        self.levels = {
            1: {"step_limit": 30, "walls": 25},
            2: {"step_limit": 40, "walls": 23},
            3: {"step_limit": 50, "walls": 20},
            4: {"step_limit": 60, "walls": 18},
            5: {"step_limit": 70, "walls": 15},
        }

    def set_difficulty(self, difficulty):
        if difficulty in ["easy", "hard"]:
            self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty

    def get_level(self):
        return self.level

    def get_step_limit(self):
        return self.levels[self.level]["step_limit"]

    def get_wall_limit(self):
        if self.creative_mode:
            return 999999
        return self.levels[self.level]["walls"]

    def next_level(self):
        if self.level < len(self.levels):
            self.level += 1
            return True
        return False

    def restart_game(self):
        self.level = 1

    def set_creative_mode(self, value):
        self.creative_mode = value

    def get_creative_mode(self):
        return self.creative_mode