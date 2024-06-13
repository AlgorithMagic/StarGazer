"""
Returns the players resources.
    Usage: Resources
"""

from commands.command import Command
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdResources(Command):
    """Resources command:                 

    The resources command will return your ships resources.
        Usage: Resources
        
    """
    key = "Resources"
    
    
    def func(self):
        resources = self.caller.get_resources()
        resources_message = "\n".join([f"|055{resource.capitalize()}: |050{value}" for resource, value in resources.items()])
        self.caller.msg(f"|025{self.caller.key}'s Resource Log")
        self.caller.msg("-" * (len(self.caller.key) + 12))
        self.caller.msg(resources_message)