from commands.command import Command
from world import weighted_dice
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class WeightedDice(Command):
    """
    Roll the dice using a weighted bias to control what value the dice lands on.  The farther from the bias the more unlikely the roll is.

    Usage: Weighted Dice |wMIN MAX BIAS|035
        E.G. "Weighted Dice 1 20 10" for a dice between 1 and 20 that falls around the mean value.
        
    Additional Notes:  This dice is used heavily in game calculations.  It's available to you so that you too make make decisions with a bias - just like in real life.
    """
    key = "Weighted Dice"
    
    def parse(self):
        args = self.args.strip().split()
        if len(args) == 3:
            min_size, max_size, desired_median = map(int, args)
            self.dice = weighted_dice(min_size, max_size, desired_median)
        else:
            self.caller.msg("Usage: Weighted Dice <min_size> <max_size> <desired_median>")
    
    def func(self):
        if hasattr(self, 'dice'):
            roll_result = self.dice.roll_dice()
            self.caller.msg(f"The roll result is: {roll_result}")
        else:
            self.caller.msg("You must provide the correct arguments to roll the dice.")
