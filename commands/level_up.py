from commands.command import Command
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdLevelUp(Command):
  """
  Levelup command:

  |025Usage:
    |035Levelup

  Increases your |025level|035 if your |025experience|035 meets the next |025level|035 requirements |025(TNL)|035.
  """

  key = "Level up"

  def func(self):
    pos_tnl = "|050"
    neg_tnl = "|500"
    if self.caller.db.exp >= self.caller.db.tnl: 
        resources_gained = self.caller.level_up()
        self.caller.msg(f"|035Level increased to: |055{self.caller.db.level}|035, "
                        f"{pos_tnl}{self.caller.db.tnl}|035 EXP remaining to next level. "
                        f"|055Resources gained: {resources_gained}")
    else:
        self.caller.msg(f"|035Not enough experience to level up. |025Current: |050{self.caller.db.exp} "
                        f"|025Needed:{neg_tnl}{self.caller.db.tnl - self.caller.db.exp}")