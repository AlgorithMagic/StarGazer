import random

class DiceWithWeight():
    def __init__(self, min_size=1, max_size=6, desired_median=3.5) -> None:
        self.min_size = min_size
        self.max_size = max_size
        self.desired_median = desired_median
    
    def roll_dice(self):
        return int(random.triangular(self.min_size, self.max_size, self.desired_median))