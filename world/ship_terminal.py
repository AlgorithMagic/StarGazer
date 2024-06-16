"""
Used for a basic terminal passive text script.
"""
import random
from typeclasses.scripts import Script

class TerminalMessages(Script):
    """
    A script that periodically sends random ambient messages to all characters present in the
    same location as the associated object. This script is not persistent and runs at a fixed interval.
    """
    messages_list = [
        "|bBeep|r Boop", 
        "|gDing|w whirl whirl whirl...", 
        "The sound of small fans and mechanical components fills the air.", 
        "A blanket of warm aroma smelling like electronic components lingers around you.", 
        "A whirring noise can be heard quietly nearby"
    ]
    
    def at_script_creation(self):
        """
        Called when the script is first created. Sets the interval for the script to run 
        and specifies that the script is not persistent.
        """
        self.interval = 1
        self.persistent = False
    
    def send_message(self):
        """
        Sends a random ambient message to all characters in the same location as the associated object.
        """
        location = self.location
        location.msg_contents(random.choice(self.messages_list))
        
    def at_repeat(self):
        """
        Called at each interval. Invokes the method to send a random ambient message.
        """
        self.send_message()
