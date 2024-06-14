"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from django.utils.translation import gettext as _
from evennia.objects.objects import DefaultCharacter
from typeclasses.objects import ObjectParent
import random

class Character(ObjectParent, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the prelogout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    prelogout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """


    def at_post_puppet(self, **kwargs):
        self.msg(_("\n|035You log into your |025StarGazer |035console as |c{name}|n.\n").format(name=self.key))
        self.msg((self.at_look(self.location), {"type": "look"}), options=None)

        def message(obj, from_obj):
            obj.msg(
                _("{name} has logged into their ships console.").format(name=self.get_display_name(obj)),
                from_obj=from_obj,
            )

        self.location.for_contents(message, exclude=[self], from_obj=self)
        y = self.db.y
        failed_rolls = self.db.failed_rolls
        x = self.db.x
        if failed_rolls == 0:
            y = 1
        else:
            if (1 * failed_rolls * 1000) <= x * 0.9:
                y = 1 * failed_rolls * 1000
            else:
                y = x * 0.9
        self.db.y = y
        
        
    def at_object_creation(self):
        
        self.db.stats = {
            "piloting" : 1,
            "fortitude" : 1,
            "intelligence" : 1,
            "luck" : 1
        }
        self.db.stat_points = 0
        self.db.level = 1
        self.db.exp = 0
        self.db.tnl = (self.db.level * 2) * self.db.level * 100
        self.db.max_level = 10000
        self.db.has_home = False
        self.db.home_location = None
        self.db.failed_rolls = 0
        self.db.max_random_number_in_drop_generation = 1000000
        # Matter is the base currency.  Antimatter is uncommon currency.  
        # Singularities are rare currency.  Gravity Wells are extremely rate.
        # Dimensions are dropped with a 1 in 1 billion drop rate.
        
        self.db.resources = {
            "Matter" : 0,
            "Anti-matter" : 0,
            "Singularities" : 0,
            "Gravity Wells" : 0,
            "Dimensions" : 0
        }


    def get_stats(self):
        """
        Get the main stats of this character. 
        
        Command implemented as "stats" in commands.default_cmdsets
        """
        return self.db.stats
    
    
    def get_exp(self): return self.db.exp
    
    
    def get_tnl(self): return self.db.tnl
    
    
    def get_resources(self):
        """
        Get the resources of this character. 
        
        Command implemented as "resources" in commands.default_cmdsets
        """
        return self.db.resources
    
    
    def level_up(self):
        """
        Perform level up on character if level is below max level else set to max level.
        Returns a string detailing the resources gained during the level up.
        """
        exp = self.db.exp
        tnl = self.db.tnl
        level = self.db.level
        max_level = self.db.max_level
        resources_gained = {}
        failed_rolls = self.db.failed_rolls
        x = self.db.max_random_number_in_drop_generation
        y = self.db.y = 1
        if failed_rolls == 0:
            y = 1
        else:
            if (1 * failed_rolls * 1000) <= x * 0.9:
                y = 1 * failed_rolls * 1000
            else:
                y = x * 0.9
        self.db.y = y
        
        if exp >= tnl:
            # Increase level by 1, or set to max level if already at max
            new_level = min(level + 1, max_level)
            self.db.level = new_level

            # Reset experience to the amount over the required tnl
            self.db.exp = exp - tnl

            # Calculate the new tnl for the next level
            self.db.tnl = (new_level * 2) * new_level * 100

            # Add stat points for leveling up
            self.db.stat_points += 1
            
            # Increases matter by X where X is a random number between 1 and level
            matter_increase = random.randint(1, self.db.level)
            self.resource_up("Matter", matter_increase)
            resources_gained["|555Matter"] = f"{matter_increase}"

            # Generate two random numbers between Y and X where Y is calculated based off how many times the player failed
            # to receive the highest rarity dropped resource (Singularity) and X is set by me.
            rand_num1 = random.randint(y, x)
            rand_num2 = random.randint(y, x)
            
            if rand_num1 != rand_num2:
                raise_pity_roll = 1 > (random.randint(0,2))
                if raise_pity_roll:
                    self.db.failed_rolls += 1
                    self.msg("|wThe |055goddess of pity|w has shown their light to you, you feel you'll find |rgreater treasures|w moving forward.")
                    
            # If both numbers within 1% of each other, increase singularity by 1 and reset failed_rolls
            if abs(rand_num1 - rand_num2) <= (x * 0.01):
                self.resource_up("Singularities", 1)
                resources_gained["|500Singularities"] = "|5001|n"
                self.db.failed_rolls = 0
                self.msg("|055Pity's |wlight has paid off, and her |050luck |wleaves you.")
            

            # If they are within 75% of each other, increase anti-matter
            if abs(rand_num1 - rand_num2) <= (x * 0.75):
                anti_matter_increase = random.randint(1, self.db.level)
                self.resource_up("Anti-matter", anti_matter_increase)
                resources_gained["|505Anti-matter"] = f"|005{anti_matter_increase}|n"

            # If they are within 25% of each other, increase gravity well by 1
            if abs(rand_num1 - rand_num2) <= (x * 0.25):
                self.resource_up("Gravity Wells", 1)
                resources_gained["|111Gravity Wells"] = "|5501|n"

            # If they are within 1.5% of each other, increase matter significantly
            if abs(rand_num1 - rand_num2) <= (x * 0.015):
                min_amount = 1000000
                max_amount = 1000000000
                matter_massive_increase = random.randint(min_amount, self.db.level * max_amount)
                self.resource_up("Matter", matter_massive_increase)
                treasure_or_stash = "|505TREASURE TROVE|035" if matter_massive_increase >= (max_amount * 0.5) else "|303legendary stash|035"
                resources_gained["|555Matter"] += f" and a {treasure_or_stash} of |500{matter_massive_increase}|035 Matter|500!|050!|005!|n"
                
        # Format the resources gained into a string to return
        resources_gained_str = ', '.join(f"{resource} |050{amount}" for resource, amount in resources_gained.items())
        return resources_gained_str


    def level_down(self):
        """
        Perform a down level on character if exp falls below the tnl for the previous level.
        """
        exp = self.db.exp
        level = self.db.level
        if exp > ((level - 1) * 2) * (level - 1) * 100: level -= 1 if level > 1 else 1
        self.db.level = level
        
        
    def stat_up(self, stat, inc_value):
        """
        Increases a single stat by the increment value if there's enough stat points.
        Provides feedback if the stat is invalid or if there are not enough points to increase the stat.

        :param stat: The name of the stat to increase.
        :param inc_value: The increment value by which to increase the stat.
        """
        current_stats = self.db.stats
        stat_points = self.db.stat_points

        if stat in current_stats:
            if stat_points >= inc_value:
                current_stats[stat] += inc_value
                stat_points -= inc_value
            else:
                # Not enough points to increase the stat
                print(f"|035Ran out of stat points before assigning |500{inc_value}|035 to |025{stat}.")
        else:
            # Invalid stat name
            print(f"|035Invalid stat: |500{stat}")

        self.db.stats = current_stats
        self.db.stat_points = stat_points
        
        
    def resource_up(self, resource, resource_inc_value):
        if resource in self.db.resources:
            self.db.resources[resource] += abs(resource_inc_value)

        
    def resource_down(self, resource, resource_dec_value):
        if resource in self.db.resources:
            self.db.resources[resource] -= abs(resource_dec_value)
