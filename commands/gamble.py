from commands.command import Command
from random import randint
from math import comb
from commands.util_tools import docstring_prefix

@docstring_prefix("|035")
class CmdGamble(Command):
    """
    |500 PLEASE NOTE THIS COMMAND IS BROKEN AND YOU WILL ALWAYS LOSE|035
    Gamble command:

    |025Usage:
        |035Gamble |w<amount>

    |035Wager |w<amount>|035 of matter.  This command is only available when visiting a valid Orbital Odds Terminal.
    """


    key = "Gamble"


    def parse(self):
        args = self.args.strip().split()
        self.valid = len(args) == 1
        if self.valid: self.wager = int(args[0])
        
    
    def func(self):
        
        
        
        
        
        
        self.caller.msg("|500 PLEASE NOTE THIS COMMAND IS BROKEN AND YOU WILL ALWAYS LOSE")
        
        
        
        
        
        
        self.set_mult = 2
        if self.valid:
            matter = self.caller.db.resources["Matter"]
            if self.give_or_take():
                big_payout = True if randint(0,self.caller.db.level) == 1 else False # Bias towards newer players
                if not big_payout: payout = int(self.wager * self.payout_multiplier)
                else:  payout = int(self.wager * self.payout_multiplier) * randint(2,randint(5,20))
                matter += payout
                if not big_payout: self.caller.msg(f"|500C|050O|005N|505G|550R|555A|055T|345S|522!|255!|314!|035 You have won a payout of |050{payout}|035 and now have {matter} |055Matter")
                if big_payout: self.caller.msg(f"|500C|050O|005N|505G|550R|555A|055T|345S|522!|255!|314!|035 You have won with a |500BIG|035 payout of |050{payout}|035 and now have {matter} |055Matter")
            else:
                matter -= self.wager
                self.caller.msg(f"|500Better luck next time!/n You have lost {self.wager} |055Matter and now have {matter}")
            self.caller.db.resources["Matter"] = matter 
        else:
            self.caller.msg("|035Please contact |505Orbital Odds|035 Customer Service or try |wGamble <Value>|035 with a real number input.  Unfortunately at this time we are not accepting imaginary numbers nor theoretical ones.  For all complaints, please contact |505Orbital Odds|035 Terminal Customer Complaints.")
    
    
    def give_or_take(self) -> bool:
        player_luck = self.caller.db.stats["luck"]
        player_level = self.caller.db.level

        # Set 'p' to 100 times the player's level, capped at 10000
        p = min(100 * player_level, 100000)

        self.caller.msg(f"p set to {p}")

        # Generate a random number for the house between 1 and 'p'
        house = randint(1, p)

        # Calculate the player's chance based on level, failed rolls, and luck
        player = (player_level * self.caller.db.failed_rolls + player_luck 
                if player_level <= self.caller.db.max_level and self.wager > 1000 
                else player_level + player_luck)

        self.caller.msg(f"player is {player} and {house} is house.")

        # Calculate the payout multiplier based on the house's chance
        self.payout_multiplier = ((house / 100) + 1) * self.set_mult

        # Determine if the player wins or loses
        are_we_generous = player >= house
        
        return are_we_generous


