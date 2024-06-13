"""
Used for a basic terminal passive text script.
"""
import random
from typeclasses.scripts import Script

class TerminalMessages(Script):
    messages_list = ["|bBeep|r Boop", "|gDing|w whirl whirl whirl...", "The sound of small fans and mechanical components fills the air.", "A blankets of warm aroma smelling like electronic components lingers around you.", "A whirring noise can be heard quietly nearby"]
    
    def at_script_creation(self):
        self.interval = 1
        self.persistent = False
    
    def send_message(self):
        location = self.location
        self.location.msg_contents(random.choice(self.messages_list))
        
    def at_repeat(self):
        self.send_message()