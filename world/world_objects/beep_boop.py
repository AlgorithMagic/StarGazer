from typeclasses.scripts import Script
from typeclasses.objects import Object
from random import choice, randint
from commands.util_tools import docstring_prefix

@docstring_prefix("|035")
class BeepBooper(Script):
    """
    This script periodically sends random beep and boop messages to all characters present in the
    same location as the associated object. The interval between messages is randomly determined.
    """
    beep_boop_messages = [
        "|500The terminal beeps harmlessly.|w", "|050A sudden boop emits from the terminal nearby.|w", 
        "|005The sound of various blips fills the air for a moment.|w", "|550The computer bleeps, how rude!|w",
        "|530The mechanical drives inside the terminal whirrs|w", "|305Whizzes emit from the terminal, as if it's suddenly processing something intense.|w", 
        "|035Hums from cooling fans silently fill the air like a gentle digital lullaby|w", "|553The computer buzzes to indicate something rudimentary|w",
        "|513Click, click, click goes the terminal.|w", "|351The terminal suddenly clacks as if a heavy mechanical switch fell somewhere inside of it.|w", 
        "|135The terminal lets off precisely spaced ticks at 0.16777 seconds apart|w", "|155Tocks|w",
        "|505The terminal swooshes.|w", "|055Sweeps and burrs resound from the terminal here and there.|w", 
        "|050Zipppp goes the terminal as the screen flickers off, then back on as it detects your subtle motions|w",
        "|005Zing! A loud sound suddenly blankets the air then silence resumes.|w", "|550Ping, |500ping, |005ping|w", 
        "|505Pong|w", "|055Ding sounds the terminal.|w",
        "|530Vroom! Goes a disk drive|w", "|305The terminal vibrates gently|w", 
        "|055Chimes occasionally sound to indicate routine tasks finishing.|w"
    ]

    def at_script_creation(self):
        """
        Called when the script is first created. Sets the initial interval for the script to run 
        and marks the script as persistent.
        """
        self.interval = randint(10, 360)
        self.persistent = True

    def at_repeat(self):
        """
        Called at each interval. Sends a random beep or boop message to all characters in the 
        same location as the associated object. Resets the interval for the next message.
        """
        self.interval = randint(10, 360)
        current_location = self.obj.location
        characters_in_location = current_location.contents

        for obj in characters_in_location:
            if obj.has_account:
                obj.msg(choice(self.beep_boop_messages))

class BeepBoop(Object):
    """
    An object that can be associated with the BeepBooper script to emit periodic beep and boop messages.
    """
    pass
