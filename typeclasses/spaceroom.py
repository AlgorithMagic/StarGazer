from typeclasses.rooms import Room
from commands.command import Command
from evennia import CmdSet
from typeclasses.spacehandler import SpaceDescHandler, SpaceRoomsProvider


class SpaceRoom(Room):
    """
    Spacerooms are the rooms made outside of the airhatch to simulate infinite and endless space.
    """

    def at_object_creation(self):
        self.tags.add("is_in_space", category="space_room")
        self.cmdset.add(SpaceCmdSet)
        
        
    def get_space(self, descr):
        spacedesc = SpaceDescHandler()
        spacereturn = spacedesc.return_spacemap()
        return spacereturn  if spacereturn != "" else descr


    def change_spacemap(self):
        """
        This method updates the space map description for the room.
        """
        spaceroom = SpaceRoomsProvider()
        self.db.desc = spaceroom.changespace()
        
class CmdSpaceMove(Command):
    """
    This command allows a player to move in space, updating the room's description.
    """
    key = "Space Search"

    def func(self):
        # Check if the player is in a room with the tag 'is_in_space'
        if self.caller.location.tags.has("is_in_space", category="space_room"):
            # Call the method to update the room header
            self.caller.location.change_spacemap()
            self.caller.execute_cmd("look")
            # Call the look command for the caller
        else:
            self.caller.msg("You are not in space.")


class SpaceCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSpaceMove)