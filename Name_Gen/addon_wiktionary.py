import pandas as pd

import requests

import re
from bs4 import BeautifulSoup




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

def add_male_names(df, nations, pages_visited):

    print(pages_visited)

    for n in range(len(nations)):

        divide = False
        argument = "https://en.wiktionary.org/wiki/Category:{}_male_given_names".format(nations[n])
        file = requests.get(argument)
        pages = [argument]
        pages_found = look_for_pages(file, pages)
        # Loop through pages and retrieve names
        print("pages that have been found", pages_found)

        print(str(file), "Iteration is {}".format(nations), nations[n])
        # print("This has updated")
        # print(str(file))
        for page in pages_found:
            argument = page
            file = requests.get(argument)
            if str(file) == "<Response [404]>":
                pass
            elif str(file) == "<Response [200]>":
                # print("Also updated")
                soup = BeautifulSoup(file.content, "lxml")
                div_tag = soup.find_all("div", {"id": "mw-pages"})
                for tag in div_tag:
                    rec_data = tag.find_all("li")
                    item_txt = ""

                    for item in rec_data:
                        item_txt = item.string
                        print(item_txt)
                        origins = nations[n]
                        print(origins)
                        try:
                            item = item.string.split("(")[0]  # Incase of any disambiguations or other issues
                        except:
                            pass
                        if any(re.findall(r"Appendix|learn more|previous|List|Surnames|name|Mobile|Cookie", item,
                                          re.IGNORECASE)):
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
                        if any(re.findall(r"Appendix|learn more|previous|List|Surnames|name|Mobile|Cookie", item,
                                          re.IGNORECASE)):
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
                            df = df.append({"name": adder, "tag": "M", "origin": origins},
                                           ignore_index=True)
                    print("Current Df is ", df)

        print(df)
    return df
def add_female_names(df, nations, pages_visited):

    print(pages_visited)

    for n in range(len(nations)):

        divide = False
        argument = "https://en.wiktionary.org/wiki/Category:{}_female_given_names".format(nations[n])
        file = requests.get(argument)
        pages = [argument]
        pages_found = look_for_pages(file, pages)
        #Loop through pages and retrieve names
        print("pages that have been found", pages_found)

        print(str(file), "Iteration is {}".format(nations), nations[n])
        #print("This has updated")
        #print(str(file))
        for page in pages_found:
            argument = page
            file = requests.get(argument)
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
                        origins = nations[n]
                        print(origins)
                        try:
                            item = item.string.split("(")[0]  # Incase of any disambiguations or other issues
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
                    print("Current Df is ", df)

        print(df)
    return df
def add_surnames(df, nations, pages_visited):
    print(pages_visited)

    for n in range(len(nations)):

        divide = False
        argument = "https://en.wiktionary.org/wiki/Category:{}_surnames".format(nations[n])
        file = requests.get(argument)
        pages = [argument]
        pages_found = look_for_pages(file, pages)
        #Loop through pages and retrieve names
        print("pages that have been found", pages_found)

        print(str(file), "Iteration is {}".format(nations), nations[n])
        #print("This has updated")
        #print(str(file))
        for page in pages_found:
            argument = page
            file = requests.get(argument)
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
                        origins = nations[n]
                        print(origins)
                        try:
                            item = item.string.split("(")[0]  # Incase of any disambiguations or other issues
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
                            df = df.append({"name": adder, "tag": "N", "origin": origins},
                                               ignore_index=True)
                    print("Current Df is ", df)

        print(df)
    return df

def look_for_pages(file, pages):
    soup = BeautifulSoup(file.content, "lxml")
    a_tag = soup.find_all("a", href=True)
    for a_link in a_tag:
        # print(a_link)
        try:
            if "next page" in a_link.string:
                print("The link is", a_link, file, a_link["href"])
                print(pages)
                print("There is a page in the tag: {0} \n {1}".format("https://en.wiktionary.org" + a_link["href"],
                                                                      file))
                if "https://en.wiktionary.org" + a_link["href"] not in pages:
                    pages.append("https://en.wiktionary.org" + a_link["href"])
                    page_in_tag = "https://en.wiktionary.org" + a_link["href"]
                    print(page_in_tag)
                    file = requests.get(page_in_tag)
                    look_for_pages(file, pages)
        except:
            break
    return pages

def add_wiktionary_names():

    nations = ["French", "Italian", "Spanish", "Turkish", "Dutch", "Swedish", "Polish", "Serbian", "Irish",
                   "Czech", "Hungarian", "Russian", "Romanian", "Persian", "Basque", "Armenian",
                   "German", "English", "Latvian", "Lithuanian", "Estonian", "Latin", "Japanese"]
    df = pd.DataFrame(columns=["name", "tag", "origin"])
    df = add_female_names(df, nations, pages_visited=[])
    df = add_male_names(df, nations, pages_visited=[])
    #df = add_surnames(df, nations, pages_visited=[])

    return df

#add_wiktionary_names()