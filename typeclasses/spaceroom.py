from typeclasses.rooms import Room
from commands.command import Command
from evennia import CmdSet
from typeclasses.spacehandler import SpaceDescHandler, SpaceRoomsProvider, SpaceSearchHandler


class SpaceRoom(Room):
    """
    Spacerooms are the rooms made outside of the airhatch to simulate infinite and endless space.
    """

    def at_object_creation(self):
        self.tags.add("is_in_space", category="space_room")
        self.cmdset.add(SpaceCmdSet)
        
        
    def get_space(self, descr):
        spacedesc = SpaceDescHandler()
        spacereturn = spacedesc.return_spacemap(spacemap_in="")
        return spacereturn  if spacereturn != "" else descr


    def change_spacemap(self):
        """
        This method updates the space map description for the room.
        """
        spaceroom = SpaceRoomsProvider()
        new_desc, special_event_occurred = spaceroom.changespace()
        self.db.desc = new_desc
        return special_event_occurred
        
class CmdSpaceMove(Command):
    """
    This command allows a player to move in space, updating the room's description and handling special events.
    """
    key = "Space Search"

    def func(self):
        # Check if the player is in a room with the tag 'is_in_space'
        if self.caller.location.tags.has("is_in_space", category="space_room"):
            # Call the method to update the room header
            special_event_occurred = self.caller.location.change_spacemap()
            # If a special event occurred, handle the resources and message
            if special_event_occurred:
                self.caller.db.resources["Singularities"] += 1
                self.caller.msg("|055You stumble upon a strange and magnificent space field.\n|500+1 Gravity Wells")

            # Perform a space search and update resources
            space_search_handler = SpaceSearchHandler()
            spacemap = self.caller.location.get_space(self.caller.location.db.desc)
            search_message, matter_value = space_search_handler.search_space(spacemap)
            self.caller.db.resources["Matter"] += matter_value
            self.caller.msg(search_message)

            # Call the look command for the caller
            self.caller.execute_cmd("look")
        else:
            self.caller.msg("You are not in space.")



class SpaceCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSpaceMove)