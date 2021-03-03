import numpy as np
import networkx as nx
from Name_Gen.addon_namegen import find_location_names
import matplotlib.pyplot as plt
import random
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
    #def __init__(self, town, regional_check, family_name, rank, moto, relations, heraldry):
    #    print("This function should initialise a family inside of a region")
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        print("This function initialises a region")
        print(kwargs, list(kwargs))
        regional_check = kwargs["settlement_type"]
        culture = kwargs["culture"]


    def get_town_type(self, regional_check, culture):
        #Region types are ranked numerically, to ensure seperate regions can be randomly assigned names
        #Scope of the regions will go from 4 - 7, starting with City and ending with hamlet / outpost - Refactored from previous version
        #TODO: Add names to a YAML file in similar fashion to JSON
        town_region_types = {4: ["City", "Grand Fortress", "Grand Library", "Grand City", "Imperial Free City"],
                        5: ["Town", "Castle", "University Town", "Market Town", "Grand Harbour", "Renowned Suburb"], 6: ["Village", "Fief", "Abbey", "Fortification", "Barony", "Barracks"],
                        7: ["Hamlet", "Settlement", "Hunters Lodge", "Outpost", "Chapel"]}
        target_culture = culture
        regions = town_region_types.get(regional_check)
        region = random.choice(regions)
        print(region)
        return region

    def get_region_type(self, regional_check, culture):
        regional_types = {1: ["Kingdom", "State", "Lordship", "Grand Duchy", "Viceroyalty"], 2: ["Duchy", "Earldom", "Knezevina", "Duché", "Herzogtum", "Grand Cities", "Principality"],
                        3: ["County", "Earldom", "League Territory", "Grafschaft", "Comitat"],}


    def get_neighbouring_regions(self, region_nodes, neighbours):
        if region_nodes:
            print("Regions have been created, connecting new location to others")
        else:
            initialise_holdings()

class Holding(Location):
    #Testing args should contain, name, culture, region number (returns region)
    holding = Location

class Region(Location):
    region = Location
    
def initialise_regions():
    #Use dictionary to create regions that hold an NX graph and subdictionary containing the holdings relative to a region
    #regions are a division of a kingdom
    region_size = np.random.randint(5, 11)
    settlement_type = np.random.randint(1, 3)
    #TODO: Add long individual names, so that it creates each region with the same culture
    output_list = load_names(region_size)
    new_dict, culture, new_list = output_list[0], output_list[1], output_list[2]
    regions_set = set([])
    nxgraph = nx.Graph()
    for i in range(region_size):
        region = Region(name=new_list[i], culture= culture, settlement_type= Region.get_region_type(new_list[i], settlement_type, culture))
        region_dict = {"Name": region.name, "Object": region}
        print("Adding node : {} {}".format(region.name, region_dict))
        nxgraph.add_node(region.name, attr_dict=region_dict)
        print("List contains : ", list(nxgraph.nodes))
        temp_list = list(nxgraph.nodes)
        print(nxgraph.number_of_nodes())
        if nxgraph.number_of_nodes() >= 1:
            nxgraph.add_edge(region.name, temp_list[i-1])
            print("This should add edges")
        if nxgraph.number_of_nodes() >= 3:
            print("There are over 3 nodes")
            try:
                for g in range(np.random.randint(1, 3)):
                    print("adding connection between region and node {} : {}".format(g, temp_list[g]))
                    nxgraph.add_edge(region.name, temp_list[g-1])

            except Exception as e:
                print("Exception found" , e)
                pass
    plt.figure()
    node_list = list(nxgraph.nodes.data())
    print(node_list)
    #print(node_list[node_list[-1]])
    # nx.draw_networkx(tree)
    # nx.draw_networkx_edge_labels(tree, pos=nx.spring_layout(tree), label_pos=0.7, rotate=False, font_size=5)
    nx.draw_networkx(nxgraph)

    plt.show()
    #TODO: make graph made up of holding graphs



def initialise_holdings():
    #import namegen functions and name binary trees after generated regions, create single use name generator based on european names and add the name and respective culture to binary tree to be used in setting regions
    town_size = np.random.randint(5, 55)
    names_list = load_names(town_size)
    binary_dict, culture, new_list = names_list[0],  names_list[1],  names_list[2]
    print("Culture of the new region is {} and the following towns {}".format(culture, new_list))
    print(new_list[0], str(culture))
    print(binary_dict)
    tree = nx.Graph()
    object_tree = nx.Graph()
    for i in range(town_size):
        distance = np.random.randint(3,12)
        settlement_type = np.random.randint(4,7)
        connections = np.random.randint(1,4)

        other_town = list(tree.nodes)

        town = new_list[i]
        holding = Holding(name=town, culture = culture, settlement_type = Holding.get_town_type(town, settlement_type, culture))
        object_tree.add_node(holding.name)
        if object_tree.number_of_nodes() > 3:
            print("Tree has {} nodes".format(len(list(object_tree.nodes))))
            for y in range(connections):
                object_tree.add_edge(holding.name, other_town[y], weight=distance)

        print(holding)
        tree.add_node(town)
        if tree.number_of_nodes() > 3:
            print("Tree has {} nodes".format(len(list(tree.nodes))))
            for x in range(connections):
                tree.add_edge(town, other_town[x], weight=distance)
    plt.figure()

    # nx.draw_networkx(tree)
    # nx.draw_networkx_edge_labels(tree, pos=nx.spring_layout(tree), label_pos=0.7, rotate=False, font_size=5)
    nx.draw_networkx(object_tree)
    nx.draw_networkx_edge_labels(object_tree,pos=nx.spring_layout(object_tree), label_pos=0.2, rotate=False, font_size=5 )
    plt.show()

def load_names(size_arg):
    binary_dict = find_location_names(size_arg)
    culture = list(binary_dict.keys())[0]
    new_list = list(binary_dict.values())[0] #Returns list within list
    objects = [binary_dict, culture, new_list]
    return objects

initialise_regions()