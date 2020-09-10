import pandas as pd
import numpy as np

class Character:
    """
    This class should be used to create characters in the main running portion, the character should have a name, title and background type as a base type
    There should be a function to create a timeline and branchoff characters that can be used to create a family inside of a town or region alternatively
    Characters should be created within a region, and assigned to places to live, then a history of them is created and they interact with one another
    """
    #Alternate implementation with *arg and **kwargs but for now will use the regular attributes
    def __init__(self, name, family, background, aspirations, possible_quests,
                 wealth, health, power):
        checked_family = self.check_family(self, family)
        #These attributes should be considered as static (in short term cases) and dont change unless there are major shifts in the world / character
        self.name = name
        #Background should contain some pointers on a characters position within a town, and should be influenced by the family class
        self.background = background
        self.aspirations = aspirations
        #Should retrieve possible quests using the characters traits, eg it makes no sense for a peasant to ask for a group to assassinate a noble unless he has money
        self.possible_quests = possible_quests
        #These attributes should be considered as non-static, and are moving up or down depending on outside factors
        self.wealth = wealth
        self.health = health
        self.power = power


        print("Creating new character")

    def check_family(self, family):
        #METHOD: checks the families in a region, if the last name exists then it either adds the characer to the family or creates a new cadet branch, else it creates a new family
        town_groups = []


