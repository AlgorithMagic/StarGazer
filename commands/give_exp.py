from commands.command import Command
from evennia.utils.search import search_object
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdAdjustEXP(Command):
    """
    AdjustEXP command:

    Usage:
      AdjustEXP |w<PlayerRef> add <Amount>|035
      AdjustEXP |w<PlayerRef> remove <Amount>|035

    Adds or removes a specified amount of EXP from a player.
    """
    
    key = "AdjustEXP"
    locks = "cmd:perm(Developer)" 
    
    def parse(self):
        self.valid = False  # Assume parsing will fail
        args = self.args.strip().split()
        if len(args) != 3 or args[1] not in ('add', 'remove'):
            self.caller.msg("Usage: AdjustEXP <PlayerRef> add/remove <Amount>")
            return

        # Search for the player object
        player = search_object(args[0])
        if not player or len(player) != 1:
            self.caller.msg("|500Player not found.|n")
            return

        try:
            self.amount = int(args[2])
        except ValueError:
            self.caller.msg("|500Amount must be a number.|n")
            return

        # Ensure we have a single object, not a list
        self.player = player[0]
        self.action = args[1]
        self.valid = True  # Parsing was successful

    def func(self):
        # Check if parsing was successful
        if not self.valid:
            return  # Exit if parsing failed

        # Check if the player object has a 'db' attribute and 'exp' attribute within it
        if not hasattr(self.player, 'db') or not hasattr(self.player.db, 'exp'):
            self.caller.msg(f"|500{self.player.key} does not have any EXP attribute to adjust.|n")
            return

        # Adjust the player's EXP
        if self.action == 'add':
            self.player.db.exp += self.amount
            change = "increased"
            color = "|050"
        else:
            self.player.db.exp -= self.amount
            change = "decreased"
            color = "|500"

        self.caller.msg(f"|050{self.player.key}'s|n EXP {change} by {color}{self.amount}.")
