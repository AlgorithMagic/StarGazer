from commands.command import Command
from evennia.utils.evtable import EvTable
from commands.util_tools import docstring_prefix


@docstring_prefix("|035")
class CmdStats(Command):
    """
    View, increase, or reset character stats.

    |025Usage:
      |035Stats
      Stats |w<statname> <value>
      Stats |wreset

    |035Displays current stats, increases a single stat, or resets all stats.
    """
    
    
    key = "Stats"


    def parse(self):
        args = self.args.strip().split()
        self.stat_to_increase = None
        self.reset = False
        self.display_only = len(args) == 0

        if self.display_only:
            return

        if args[0].lower() == 'reset':
            self.reset = True
        elif len(args) == 2:
            self.parse_stat_increase(args)
        else:
            self.caller.msg("Invalid command usage. Type |w'help Stats'|035 for more information.")


    def parse_stat_increase(self, args):
        stat, value = args[0].lower(), args[1]
        if value.isdigit():
            self.stat_to_increase = (stat, int(value))
        else:
            self.caller.msg(f"Value for |050{stat}|035 must be an integer.")


    def func(self):
        if self.reset:
            self.reset_stats()
        elif self.stat_to_increase:
            self.stat_up(*self.stat_to_increase)
        else:
            self.display_stats()


    def display_stats(self):
        stats = self.caller.get_stats()
        stat_points = self.caller.db.stat_points
        exp = self.caller.get_exp()
        tnl = self.caller.get_tnl()
        level = self.caller.db.level
        
        # Initialize the EvTable for stats with an additional column for cost
        stats_table = EvTable("|005Neurological Traits", "|252Value", "|252Cost", border="cells", header_line_char="=")
        
        # Loop through each stat and add it to the stats table with its current value and cost
        for stat, value in stats.items():
            cost = self.calculate_cost(stat, value, level)
            stats_table.add_row(f"|055{stat.capitalize()}", f"|050{value}", f"|050{cost}")

        # Initialize the EvTable for features
        features_table = EvTable("|005Neurological Features", "|252Value", border="cells", header_line_char="=")
        
        # Add rows for level, stat points, experience, and experience to next level
        features_table.add_row("|055Level", f"|050{level}")
        features_table.add_row("|055Stat Points", f"|050{stat_points}")
        features_table.add_row("|055Exp", f"|050{exp}")
        features_table.add_row("|055To Next Level", f"|500{tnl}")

        # Display the tables to the caller
        self.caller.msg(str(stats_table))
        self.caller.msg(str(features_table))


    def calculate_cost(self, stat, value, level):
        # Define the cost formula here
        cost = value * level
        return cost
          
           
    def stat_up(self, stat, value):
        current_stats = self.caller.db.stats
        stat_points = self.caller.db.stat_points
        resources = self.caller.db.resources
        level = self.caller.db.level
        # Check if the stat is a valid stat name
        if stat not in current_stats:
            self.caller.msg(f"{stat}|035 is not a valid stat.")
            return

        # Calculate the total cost for the desired increase
        total_cost = sum(self.calculate_cost(stat, current_stats[stat] + i, level) for i in range(value))

        # Check if there are enough resources (Matter) AND stat points for the desired increase
        if resources['Matter'] < total_cost and stat_points < value:
            self.caller.msg(f"Not enough resources to increase |050{stat}|035 by |500{value}|035. You are short by |050{total_cost - resources['Matter']}|035 matter and |050{value - stat_points}|035 stat points.")
        elif resources['Matter'] < total_cost:
            self.caller.msg(f"Not enough Matter to increase |050{stat}|035 by |500{value}|035. You are short by |050{total_cost - resources['Matter']}|035 matter.")
        elif stat_points < value:
            self.caller.msg(f"Not enough stat points to increase |050{stat}|035 by |500{value}|035. You are short by |050{value - stat_points}|035 stat points.")
        else:
            # If there are enough resources, proceed to increase the stat
            for i in range(value):
                cost = self.calculate_cost(stat, current_stats[stat] + i, level)
                current_stats[stat] += 1
                stat_points -= 1
                resources['Matter'] -= cost

            # Update the caller's resources and stat points
            self.caller.db.stats = current_stats
            self.caller.db.stat_points = stat_points
            self.caller.db.resources = resources

            # Inform the caller of the new stat value, total cost, and remaining resources
            self.caller.msg(f"Raised |050{stat}|035 to: |050{current_stats[stat]}|035, costing |050{total_cost}|035 matter. |035(|500{value}|035 stat points used, |050{stat_points}|035 left, |050{resources['Matter']}|035 matter remaining.)")


    def reset_stats(self):
        default_stat_value = 1
        refunded_points = sum(value - default_stat_value for value in self.caller.db.stats.values())

        self.caller.db.stats = {stat: default_stat_value for stat in self.caller.db.stats}
        self.caller.db.stat_points += refunded_points

        self.caller.msg(f"All stats have been reset. |050{self.caller.db.stat_points} |035points available.")
