import pandas as pd
import numpy as np
import requests
import os
import re
from bs4 import BeautifulSoup
from transliterate import translit, detect_language
import time
from unidecode import unidecode


def add_names(df, name_div, name_fin, nation_abrev, nations, probable_formats):
    for i in range(len(nations)):
        divide = False
        argument = "https://en.wiktionary.org/wiki/Appendix:{}_given_names".format(nations[i])
        print(argument)
        file = requests.get(argument)
        print(str(file), "Iteration is {}".format(i), nations[i])
        #print("This has updated")
        #print(str(file))
        if str(file) == "<Response [404]>":
            pass
        elif str(file) == "<Response [200]>":
            #print("Also updated")
            soup = BeautifulSoup(file.content, "lxml")

            rec_data = soup.find_all(probable_formats)
            item_txt = ""
            for item in rec_data:
                item_txt = item.string
                origins = nation_abrev[i]
                print(origins)

                if item_txt is None:
                    # print(item.text)
                    item_split = item.text.split(" ")
                    item_txt = item_split[0]
                    item_txt = re.sub(r"([A-Z])", r" \1", item_txt).split()
                    item_txt = item_txt[0]
                    item_txt = item_txt.strip()
                print(item.string)
                print("Divided text: ", item_txt)
                print(name_div, item_txt)
                if item_txt == name_div:  # First female entry
                    divide = True
                if item_txt == name_fin[i]:  # Last acceptable entry
                    adder = str(item_txt)

                    df = df.append({"name": adder, "tag": "F", "origin": origins},
                                   ignore_index=True)
                    break

                if item_txt is not None:
                    adder = str(item_txt)
                    parts = re.split(r'[;,\s]\s*', adder)  # removes any double names that are not hyphinated
                    print(parts)
                    adder = parts[0]
                    if not adder.strip():
                        print("Not Found")
                        pass
                    print(adder)
                    if adder == name_div[-1]:
                        # Had to add this to fix the polish names set, should rework later
                        divide = True
                    if not divide:
                        df = df.append({"name": adder, "tag": "M", "origin": origins},
                                       ignore_index=True)
                    else:
                        df = df.append({"name": adder, "tag": "F", "origin": origins},
                                       ignore_index=True)
            print(df)
    for e in nations:
        print(e)
        g = df.loc[df["origin"] == e]
        print("DF IS + {}".format(g), g)
        print(g, g["tag"].value_counts())


    return df
nations = ["French", "German", "Spanish"]
def add_male_names(nations):
    df = pd.DataFrame(columns=["name", "tag", "origin"])
    for i in range(len(nations)):
        divide = False
        argument = "https://en.wiktionary.org/wiki/Category:{}_male_given_names".format(nations[i])
        print(argument)
        file = requests.get(argument)
        print(str(file), "Iteration is {}".format(i), nations[i])
        #print("This has updated")
        #print(str(file))
        if str(file) == "<Response [404]>":
            pass
        elif str(file) == "<Response [200]>":
            #print("Also updated")
            soup = BeautifulSoup(file.content, "lxml")

            rec_data = soup.find_all("li")
            item_txt = ""
            for item in rec_data:
                item_txt = item.string
                origins = nations[i]
                print(origins)

                if item_txt is None:
                    try:
                        # print(item.text)
                        item_split = item.text.split(" ")
                        item_txt = item_split[0]
                        item_txt = re.sub(r"([A-Z])", r" \1", item_txt).split()
                        item_txt = item_txt[0]
                        item_txt = item_txt.strip()
                    except:
                        pass
                print(item.string)
                print("Divided text: ", item_txt)

                if item_txt is not None:
                    adder = str(item_txt)
                    parts = re.split(r'[;,\s]\s*', adder)  # removes any double names that are not hyphinated
                    print(parts)
                    adder = parts[0]
                    if not adder.strip():
                        print("Not Found")
                        pass
                    print(adder)
                    df = df.append({"name": adder, "tag": "M", "origin": origins},
                                       ignore_index=True)
            print(df)
        for e in nations:
            print(e)
            g = df.loc[df["origin"] == e]
            print("DF IS + {}".format(g), g)
            print(g, g["tag"].value_counts())

        return df
def add_female_names(df, nations, next_page, pages_vistited):

    print(pages_vistited)


    for i in range(len(nations)):
        divide = False
        argument = "https://en.wiktionary.org/wiki/Category:{}_female_given_names".format(nations[i])
        if next_page is not None:
            argument = next_page
            if next_page not in pages_vistited:
                pages_vistited.append(next_page)
            else:
                break

        print(argument)
        file = requests.get(argument)
        print(str(file), "Iteration is {}".format(i), nations[i])
        #print("This has updated")
        #print(str(file))
        if str(file) == "<Response [404]>":
            pass
        elif str(file) == "<Response [200]>":
            #print("Also updated")
            soup = BeautifulSoup(file.content, "lxml")
            div_tag = soup.find_all("div", {"id": "mw-pages"})
            for tag in div_tag:
                rec_data = tag.find_all("li")
                item_txt = ""

                for item in rec_data:
                    item_txt = item.string
                    print(item_txt)
                    origins = nations[i]
                    print(origins)
                    try:
                        item = item.string.split("(")[0]  # Incase of any disambiguations or other issues
                        name=item
                    except:
                        pass
                    if any(re.findall(r"Appendix|learn more|previous|List|Surnames|name|Mobile|Cookie", item, re.IGNORECASE)):
                        print("Invalid name: ", item)
                        continue
                    if item_txt is None:
                        try:
                            print(item.text)
                            item_split = item.text.split(" ")
                            item_txt = item_split[0]
                            item_txt = re.sub(r"([A-Z])", r" \1", item_txt).split()
                            item_txt = item_txt[0]
                            item_txt = item_txt.strip()
                        except:
                            pass
                    print(item)
                    print("Divided text: ", item_txt)
                    if any(re.findall(r"Appendix|learn more|previous|List|Surnames|name|Mobile|Cookie", item, re.IGNORECASE)):
                        print("Invalid name: ", item)
                        break
                    elif item_txt is not None:
                        adder = str(item_txt)
                        parts = re.split(r'[;,\s]\s*', adder)  # removes any double names that are not hyphinated
                        print(parts)
                        adder = parts[0]
                        if not adder.strip():
                            print("Not Found")
                            pass
                        print(adder)
                        df = df.append({"name": adder, "tag": "F", "origin": origins},
                                           ignore_index=True)

            a_tag = soup.find_all("a", href=True)
            for a_link in a_tag:
                try:
                    if "next page" in a_link.string:
                        print("There is a page in the tag: {}".format("https://en.wiktionary.org" + a_link["href"]))
                        add_female_names(df, nations, next_page="https://en.wiktionary.org" + a_link["href"], pages_vistited= pages_vistited)
                except:
                    break
        print(df)
        # for e in nations:
        #     print(e)
        #     g = df.loc[df["origin"] == e]
        #     print("DF IS + {}".format(e), g)
        #     print(g, g["tag"].value_counts())

        return df


df = pd.DataFrame(columns=["name", "tag", "origin"])
df = add_female_names(df, nations, next_page=None, pages_vistited=[])
print(df)