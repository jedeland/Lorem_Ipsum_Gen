import yaml
import os

def input_flow():
    #Creates command line arguments to control the flow of YAML inputs
    #Uses event_id and event to add line to new yaml file
    print("Please type the name of the section of events you are creating")
    #print("Please type the name of the section of events you are creating, or type 'list' to show existing events")
    section_in = str(input(""))
    print("Section: "+section_in)
    if os.path.exists(section_in):
        print("Section already exists, adding new events file...")
        name_in = str(input("Please input the name of the events file\n"))
        #TODO: continues on into a YAML dump creator, instead of creating a default file
        if os.path.exists("{}.{}.yml".format(section_in, name_in)):
            print("Input name already exists, opening editor")
        else:
            #YAML file should follow this format: Name of file as the tree node -> Event ID -> List containing event text and effect
            print("Creating new file")
            input_done = False
            yaml_file_dict = {}
            while input_done is not True:
                print("Input the event title and the description text, Followed by the impact - Type 'list' to see the possible impacts")
                title_input = str(input("Event ID: "))
                text_input = str(input("Event Text: "))
                text_input = "'{}'".format(text_input)
                impact_input = str(input("Impact: "))
                yaml_file_dict.update({title_input: [text_input, impact_input]})
            print(yaml_file_dict)
            yaml_file_arg = {section_in: yaml_file_dict}
            print(yaml_file_dict)




    else:
        os.mkdir(section_in)




input_flow()