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
