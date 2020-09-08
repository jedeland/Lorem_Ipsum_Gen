class Location:
    """
    This class should be used to create a location in the main running portion, the locations should have a name, type(town, country, duchy, village ect.), population, situation(recently invaded, prosperous, new ruler, quests) and customs
    There should be a function to create a timeline and branchoff of important events for characters within the region (eg. discovered ruins, new enterprises created)
    That can be used to create a location that can house the families and characters within it
    Regions should be created as a part of another region (eg. a town is contained within a county, that county is within a duchy, that duchy is within a mageocracy ect)
    Regions should be assigned how populated they are (eg. they exist in most towns, or only in small villages), and how affluent they are,
    Then a history of important figures and relations is created as families interact with one another and the region gains boons or negatives (eg. new cathedral built, undead horde raided town recently ect.)
    The regions should take the form of nodes, that are related to and influence one another to give the impression of realistic situations with minor oddities
    (eg. rich cities should be surrounded by relatively well of cities (city_nodes connected to capital node gain bonuses to their affluence, regions that contain a capital should have centralised power there (richer or more populous than the others)
    """
    def __init__(self, town, regional_check, family_name, rank, moto, relations, heraldry):
        print("This function should initialise a family inside of a region")

    def set_region(self, regional_check, culture):
        #Region types are ranked numerically, to ensure seperate regions can be randomly assigned names
        #Scope of the regions will go from 1 - 7, starting with kingdom and ending with hamlet / outpost
        region_types = {1: ["Kingdom", "State", "Lordship", "Grand Duchy", "Viceroyalty"], 2: ["Duchy", "Earldom", "Knezevina", "Duché", "Herzogtum", "Grand Cities", "Principality"],
                        3: ["County", "Earldom", "League Territory", "Grafschaft", "Comitat"], 4: ["City", "Grand Fortress", "Grand Library", "Capital", "Imperial Free City"],
                        5: ["Town", "Castle", "University Town", "Market Town", "Grand Harbour", "Renowned Suburb"], 6: ["Village", "Fief", "Abbey", "Fortification", "Barony", "Barracks"],
                        7: ["Hamlet", "Settlement", "Hunters Lodge", "Outpost", "Chapel"]}
        target_culture = culture
    def get_neighbouring_regions(self, region_nodes, neighbours):
        if region_nodes:
            print("Regions have been created, connecting new location to others")
        else:
            initialise_regions()


def initialise_regions():
    #import namegen functions and name binary trees after generated regions, create single use name generator based on european names and add the name and respective culture to binary tree to be used in setting regions
    region_number = 
    binary_trees = {}
    for i in range(10):
