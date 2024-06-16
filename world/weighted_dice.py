import random

class DiceWithWeight:
    """
    A class representing a weighted dice that allows for rolls with a desired median value.
    
    Attributes:
        min_size (int): The minimum value that can be rolled.
        max_size (int): The maximum value that can be rolled.
        desired_median (float): The desired median value for the dice rolls.
    """
    
    def __init__(self, min_size=1, max_size=6, desired_median=3.5) -> None:
        """
        Initializes a DiceWithWeight instance with the given minimum size, maximum size, and desired median.
        
        Args:
            min_size (int): The minimum value that can be rolled. Default is 1.
            max_size (int): The maximum value that can be rolled. Default is 6.
            desired_median (float): The desired median value for the dice rolls. Default is 3.5.
        """
        self.min_size = min_size
        self.max_size = max_size
        self.desired_median = desired_median
    
    def roll_dice(self):
        """
        Rolls the dice using a triangular distribution with the given minimum size, maximum size, and desired median.
        
        Returns:
            int: The result of the dice roll.
        """
        return int(random.triangular(self.min_size, self.max_size, self.desired_median))
