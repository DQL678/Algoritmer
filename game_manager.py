#Level, progression, regler
class GameManager:
    def __init__(self):
        self.difficulty = "hard"  # standard

    def set_difficulty(self, difficulty):
        if difficulty in ["easy", "hard"]:
            self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty