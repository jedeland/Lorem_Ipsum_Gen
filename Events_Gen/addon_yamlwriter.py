import yaml
import os

def input_flow():
    #Creates command line arguments to control the flow of YAML inputs
    #Uses event_id and event to add line to new yaml file
    print("Please type the name of the section of events you are creating")
    section_in = str(input(""))
    print("Section: "+section_in)
    if os.path.exists(section_in):
        print("Section already exists, adding new events ...")
    else:
        os.mkdir(section_in)


input_flow()