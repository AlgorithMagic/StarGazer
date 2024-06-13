from commands.command import Command
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdCheckTNL(Command):
    """Check TNL command:
    
    Usage:
      CheckTNL
    
    Displays the |wexperience points|035 needed to reach the next |wlevel|035.
    """
    
    key = "CheckTNL"

    def func(self):
        exp_needed = self.caller.db.tnl - self.caller.db.exp
        if exp_needed > 0:
            self.caller.msg(f"|035You need |500{exp_needed}|035 more experience points to level up.")
        else:
            self.caller.msg(f"|035You have enough experience to level up! Use the |050Levelup|035 command to increase your level.")