"""
Handler Module for space descriptions, lists, dicts, db access, etc.
"""
from random import randint, choice


class SpaceDescHandler():
    """
    Manages space descriptions within a virtual environment.

    This class provides methods to set and retrieve descriptions of spaces, represented as strings,
    and interacts with a database to store and update these descriptions. It also converts space
    descriptions into a map format for easier manipulation and visualization.

    Attributes:
        old_desc (list): The current description of the space as a list of strings.
        new_desc (list): The new description of the space to be updated.

    Methods:
        setget_space_desc(new_desc): Updates the space description if new_desc is different from old_desc.
        setget_spacemap(): Retrieves the space description and converts it into a map format.
        return_spacemap(spacemap_in): Returns a string representation of the space map for display.
        change_map(new_elements): Changes elements in the space map based on new_elements provided.
    """
    def setget_space_desc(self, new_desc):
        """
        Updates the space description with a new description if provided and different from the current one.

        Args:
            new_desc (list): A list of strings representing the new description of the space.

        Returns:
            list: The updated space description as a list of strings.
        """
        size_of_space = 75 # change this in the class below too
        num_of_lines = 25 # Change this in the class below too
        self.old_desc = [
            ["|0550" + "-" * 16 + "0"]
        ]
        for _ in range(num_of_lines):
            self.old_desc.append(["|055!" + "|000o" * size_of_space + "|055!"])
        self.old_desc.append(["|0550" + "-" * size_of_space + "0|n"])
        if self.old_desc != new_desc and new_desc != "":
            return self.new_desc
        else:
            return self.old_desc
        
        
    def setget_spacemap(self):
        """
        Retrieves the current space description and converts it into a map format.

        Returns:
            list: A 2D list representing the space map.
        """
        string_list = self.setget_space_desc(new_desc="")
        space_map = [list(row) for row in string_list]
        return space_map
    
    
    def return_spacemap(self, spacemap_in):
        """
        Converts a space map into a string representation for display.

        Args:
            spacemap_in (list): A 2D list representing the space map.

        Returns:
            str: A string representation of the space map.
        """
        return '\n'.join([''.join(row) for row in spacemap_in])
    
    def change_map(self, new_elements):
        """
        Modifies elements in the space map based on the provided new elements.

        Args:
            new_elements (list of tuples): A list of tuples where each tuple contains the row index,
                                           column index, and the new element to be placed at that position.

        """
        for row_index, col_index, new_element in new_elements:
            if 0 <= row_index < len(self.old_desc) and 0 <= col_index < len(self.old_desc[row_index][0]):
                row = self.old_desc[row_index][0]
                self.old_desc[row_index][0] = row[:col_index] + new_element + row[col_index+1:]
                
                
class SpaceRoomsProvider():
    """
    Provides functionality to dynamically change the space in a virtual environment.

    This class uses randomization to alter the elements within the space, simulating a dynamic
    and changing environment. It leverages the SpaceDescHandler class to update the space
    descriptions and visualize them as maps.

    Methods:
        changespace(): Randomly changes elements in the space and returns the updated space map.
    """
    def changespace(self):
        """
        Randomly alters elements within the space to simulate a dynamic environment.

        Returns:
            str: The updated space map as a string representation.
        """
        chance_of_change = 1000
        size_of_space = 75 # change this in the class below too
        num_of_lines = 25 # Change this in the class below too
        probability_of_space_object = self.get_random()
        space_objects = [
            "*", "'", ".", "`"
        ]
        color_prefixes = ["|{}{}{}".format(r, g, b) for r in range(6) for g in range(6) for b in range(6)] # List of all colors

        space = [
            ["|0550" + "-" * size_of_space + "0"]
        ]
        for _ in range(num_of_lines):
            space.append(["!" + "|000o" * size_of_space + "|055!"])
        space.append(["|0550" + "-" * size_of_space + "0|n"])
        
        for row_index, row in enumerate(space):
            new_row = list(row[0])
            for col_index, s in enumerate(new_row):
                if s == 'o' and randint(1, probability_of_space_object) >= chance_of_change:
                    # Choose a random space object
                    space_object = choice(space_objects)
                    # Determine the color based on the space object
                    color = "|000" if space_object == 'o' else "|055" if s == '-' or s == '!' else choice(color_prefixes)
                    # Update the char with the new space object and color
                    new_row[col_index] = color + space_object
            space[row_index] = [''.join(new_row)]
        # Check for the special event
        special_event_occurred = self.get_random() == 2000
        return SpaceDescHandler().return_spacemap(space), special_event_occurred

    def get_random(self) -> int:
        number = randint(990,1001) if randint(0,100) != 1 else 1010 if randint(0,1) != 1 else 2000
        return number
    
class SpaceSearchHandler():
    """
    Handles the logic and descriptions for searching space in the game.
    
    This class provides methods to analyze the space map and generate descriptions
    for the results of a space search. It also updates the matter resource based on
    the findings.
    
    Methods:
        search_space(spacemap): Analyzes the spacemap and returns a description of the search results.
    """
    
    def search_space(self, spacemap):
        """
        Analyzes the spacemap and returns a description of the search results.
        
        Args:
            spacemap (list): A 2D list representing the space map.
            
        Returns:
            tuple: A tuple containing the search result description and the amount of matter found.
        """
        size_of_space = 75 # change this in the class below too
        num_of_lines = 25 # Change this in the class below too
        # Count the number of objects that are not the default |000o
        non_default_objects = (size_of_space * num_of_lines) - sum(row.count('o') for row in spacemap)
        
        # If there are no objects other than |000o, return "Nothing Happens"
        if non_default_objects == 0:
            return ("Nothing Happens", 0)
        
        # Otherwise, choose a random immersive message and update matter
        messages = [
            "As your ship's lights pierce the void, you uncover floating debris from ancient civilizations.",
            "Your sensors detect unusual energy signatures, leading you to a cluster of exotic matter.",
            "Navigating through the silent expanse, you stumble upon remnants of a forgotten cosmic event."
        ]
        message = choice(messages)
        
        # Increase matter by the number of non-default objects found
        matter_found = non_default_objects
        
        return (message, matter_found)