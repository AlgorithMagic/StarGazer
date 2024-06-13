from commands.command import Command
from evennia.utils import utils
from evennia.utils.search import search_object
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdResourceUpDown(Command):
    """
    Adjust the resources of a character.

    Usage:
        ResourceManager |wup/down <DBREF><RESOURCE_NAME> <VALUE>|035

    Increases or decreases the specified resource by the given value for the character with the specified dbref.
    """

    key = "ResourceManager"
    locks = "cmd:perm(Developer)"

    def parse(self):
        args = self.args.strip().split()
        if len(args) != 4:
            self.caller.msg("|rUsage: ResourceManager up/down <DBREF><RESOURCE_NAME> <VALUE>|n")
            return

        self.action, self.dbref, self.resource, self.value = args[0].lower(), args[1], args[2], args[3]

        # Check if the value is a valid number
        try:
            self.value = int(self.value)
        except ValueError:
            self.caller.msg("|rThe value must be a number.|n")
            return

        # Validate the dbref
        if not utils.dbref(self.dbref):
            self.caller.msg("|rThe dbref is not valid.|n")
            return

        # Search for the object
        self.character = search_object(self.dbref)
        if not self.character:
            self.caller.msg("|rNo object found with that dbref.|n")
            return

    def func(self):
        if not hasattr(self, 'action') or not hasattr(self, 'resource') or not hasattr(self, 'value') or not hasattr(self, 'character'):
            return

        character = self.character[0]  # search_object returns a list

        # Check if the resource exists in the character's resources
        if not hasattr(character.db, 'resources') or self.resource not in character.db.resources:
            self.caller.msg(f"|rThe resource {self.resource} does not exist for {character.key}.|n")
            return

        # Perform the action
        if self.action == "up":
            character.resource_up(self.resource, self.value)
            self.caller.msg(f"|gIncreased {self.resource} by {self.value} for {character.key}.|n")
        elif self.action == "down":
            character.resource_down(self.resource, self.value)
            self.caller.msg(f"|rDecreased {self.resource} by {self.value} for {character.key}.|n")
        else:
            self.caller.msg("|rInvalid action. Use 'up' or 'down'.|n")