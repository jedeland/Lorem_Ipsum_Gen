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
    print("Current df is ", df)
    print("Next page is ", next_page)



    divide = False
    argument = "https://en.wiktionary.org/wiki/Category:{}_female_given_names".format(nations[0])
    file = requests.get(argument)
    pages_found = look_for_pages(file, argument)
    print(pages_found)
    if next_page is not None:
        argument = next_page
        if next_page not in pages_vistited:
            pages_vistited.append(next_page)




    print(str(file), "Iteration is {}".format(nations), nations[0])
    #print("This has updated")
    #print(str(file))
    if str(file) == "<Response [404]>":
        pass
    elif str(file) == "<Response [200]>":
        for pages in pages_found:

            #print("Also updated")
            soup = BeautifulSoup(file.content, "lxml")
            div_tag = soup.find_all("div", {"id": "mw-pages"})
            for tag in div_tag:
                rec_data = tag.find_all("li")
                item_txt = ""

                for item in rec_data:
                    item_txt = item.string
                    print(item_txt)
                    origins = nations[0]
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
                print("starting to look for links")
                a_tag = soup.find_all("a", href=True)
                final_df = df
                print("Outside Current Df is ", final_df)


def look_for_pages(file, start_page):
    soup = BeautifulSoup(file.content, "lxml")
    a_tag = soup.find_all("a", href=True)
    pages = [start_page]
    for a_link in a_tag:

        # print(a_link)
        try:

            if "next page" in a_link.string:
                print("The link is", a_link, file, a_link["href"])
                print("There is a page in the tag: {0} \n {1}".format("https://en.wiktionary.org" + a_link["href"],
                                                                      file))
                if "https://en.wiktionary.org" + a_link["href"] not in pages:
                    pages.append("https://en.wiktionary.org" + a_link["href"])
                    page_in_tag = "https://en.wiktionary.org" + a_link["href"]
                    print(page_in_tag)



        except:
            break
    return pages



    print("Its a df + ", df)
        # for e in nations:
        #     print(e)
        #     g = df.loc[df["origin"] == e]
        #     print("DF IS + {}".format(e), g)
        #     print(g, g["tag"].value_counts())




df = pd.DataFrame(columns=["name", "tag", "origin"])
df = add_female_names(df, nations, next_page=None, pages_vistited=[])
print(df)

