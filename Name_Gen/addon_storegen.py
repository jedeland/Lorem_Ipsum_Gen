import random
import sqlite3
import sys

import pandas as pd; import numpy as np
import requests; import os; import re; from Name_Gen import addon_namegen

store_types = ["General_Store", "Wandmaker", "Blacksmith", "Armourer", "Weaponsmith", "Alchemist", "Enchanter",
               "Scribe"]
assign_types = {"civilian stores": ["General_Store", "Wandmaker", "Alchemist", "Enchanter", "Scribe"],
                "hero stores": ["Blacksmith", "Armourer", "Weaponsmith", "Alchemist", "Enchanter"]}

def get_relevant_names():
    print("Getting relevant names")
