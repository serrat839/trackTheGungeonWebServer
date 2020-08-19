import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pprint

def scrapeURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def scrapePaths(url):
    gungeon_links = scrapeURL(url).find_all("center")[0]

    paths = []
    for link in gungeon_links.find_all("a"):
        paths.append(link.get("href"))
    return paths

def scrapeGungeoneer(url, paths):
    # scrape gungeoneer info, stored in tr objects
    gungeon_links = scrapeURL(url + paths[0]).find_all("div", class_="tabbertab")
    gungeon_links = gungeon_links[0].find_all("tr")

    columns = ["Gungeoneer", "Starting Weapons", "Starting Items"]
    rows_list = []

    # for each row
    for row in gungeon_links:

        # for each actual gungeoneer
        gungeoneer = None
        weapons = []
        items = []
        for i, col in enumerate(row.find_all("td")):
            # for each cell
            for cell in col.find_all("a"):
                contents = cell.string
                if contents is not None:
                    if i == 0:
                        gungeoneer = contents
                    elif i == 1:
                        weapons.append(contents)
                    elif i == 2:
                        items.append(contents)

        if gungeoneer is not None:
            rows_list.append({"Gungeoneer": gungeoneer,
                              "Starting Weapons": weapons,
                              "Starting Items": items})

    gungeoneer_data = pd.DataFrame(rows_list)
    return gungeoneer_data

def scrapeWeapons(url, paths):
    gungeon_links = scrapeURL(url + paths[1]).find_all("tr")
    headers = gungeon_links[0].find_all("th")
    gungeon_links = gungeon_links[1:]

    header_order = []
    gungeon_data = {}
    for column in headers:
        data = column.string
        if data is None:
            data = column.contents[0].string
        data = data.replace("\n", "")

        gungeon_data[data] = []
        header_order.append(data)

    for row in gungeon_links:
        for i, cell in enumerate(row.find_all("td")):
            data = ""
            if i == 0 or i == 3:
                temp = cell.contents[0].contents[0].get("alt", "")
                data = temp.replace(" Quality Item.png", "")
            elif i == 1:
                data = cell.contents[0].string
            elif i == 15:
                for child in cell.contents:
                    data += child.string
            else:
                data = cell.string
            if data is not None:
                data = data.replace("\n", "")
            gungeon_data[header_order[i]].append(data)

    return pd.DataFrame(gungeon_data)

def scrapeItems(url, paths):
    gungeon_links = scrapeURL(url + paths[2]).find_all("tr")
    headers = gungeon_links[0].find_all("th")
    gungeon_links = gungeon_links[1:]

    header_order = []
    gungeon_data = {}
    for column in headers:
        data = column.string
        if data is None:
            data = column.contents[0].string
        data = data.replace("\n", "")

        gungeon_data[data] = []
        header_order.append(data)

    skipnext = False
    for row in gungeon_links:
        for i, cell in enumerate(row.find_all("td")):
            data = ""
            if skipnext:
                # ruby bracelet is dumb so i am hardcoding in this item lol
                gungeon_data[header_order[1]].append("Ruby Bracelet")
                gungeon_data[header_order[2]].append("Passive")
                gungeon_data[header_order[3]].append("Thrown Guns Explode | Moving Forward")
                gungeon_data[header_order[4]].append("D")
                gungeon_data[header_order[5]].append("Thrown guns will explode. | Thrown guns will explode. Grants immunity to contact damage. Moving constantly without rolling or taking damage for 4 seconds charges a dodge roll, which will deal 300 damage.")
                skipnext = False
                break
            if i == 0 or i == 4:
                # get icon name
                for child in cell.contents:
                    if type(child) == NavigableString:
                        continue
                    temp = child.contents[0].get("alt", "")
                    data += temp.replace(" Quality Item.png", "")
            elif i == 1:
                data = cell.contents[0].string
                if data == "Ruby Bracelet":
                    skipnext = True
                    break

            elif i == 5:
                data = cell.string
                if cell.string is None:
                    data = ""
                    for child in cell.contents:
                        if child.string is None:
                            continue
                        data += child.string
            else:
                data = cell.string

            if data is not None:
                data = data.replace("\n", "")
            gungeon_data[header_order[i]].append(data)

    return pd.DataFrame(gungeon_data)



if __name__ == "__main__":
    # stores all the links to the wiki The first center has all we want
    url = "https://enterthegungeon.gamepedia.com/Enter_the_Gungeon_Wiki"

    # index 2 is items
    paths = scrapePaths(url)

    # base url for all the enter the gungeon data
    url = "https://enterthegungeon.gamepedia.com"

    # Scrape the starting gungeoneer data
    # gungeoneer_data = scrapeGungeoneer(url, paths)

    # Scrape gun data
    gun_data = scrapeWeapons(url, paths)

    # scrape item data
    item_data = scrapeItems(url, paths)

    sqlcommand = '''
-- Author: Thomas Serrano
-- Last Updated: 8/8/2020
-- Creates a table containing gungeon weapon data. For the record, these are all varchars because the website i scraped this info from has text in numerical columns sometimes.
CREATE TABLE weapons (
    icon			VARCHAR(255),
    name			VARCHAR(255) PRIMARY KEY,
    "quote"			VARCHAR(255),
    quality			VARCHAR(20),
    type			VARCHAR(20),
    dps				VARCHAR(10),
    magazine		VARCHAR(25),
    ammo_capacity	VARCHAR(20),
    damage			VARCHAR(36),
    fire_rate		VARCHAR(10),
    reload_time		VARCHAR(10),
    shot_speed		VARCHAR(10),
    "range"			VARCHAR(10),
    force			VARCHAR(10),
    spread			VARCHAR(4),
    notes			VARCHAR(300)
); \n
        '''

    sql_insert = 'INSERT INTO weapons (icon, name, "quote", quality, type, dps, magazine, ammo_capacity, damage,' \
                 ' fire_rate, reload_time, shot_speed, "range", force, spread, notes) VALUES' \
                 '("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"); \n'
    for row in gun_data["Icon"]:
        row = gun_data[gun_data["Icon"] == row]

        sqlcommand += sql_insert.format(
            row.iloc[0]["Icon"],
            row.iloc[0]["Name"],
            row.iloc[0]["Quote"],
            row.iloc[0]["Quality"],
            row.iloc[0]["Type"],
            row.iloc[0]["DPS"],
            row.iloc[0]["Magazine Size"],
            row.iloc[0]["Ammo Capacity"],
            row.iloc[0]["Damage"],
            row.iloc[0]["Fire Rate"],
            row.iloc[0]["Reload Time"],
            row.iloc[0]["Shot Speed"],
            row.iloc[0]["Range"],
            row.iloc[0]["Force"],
            row.iloc[0]["Spread"],
            row.iloc[0]["Notes"]
        )

    text_file = open("weapons.sql", "w")
    text_file.write(sqlcommand)
    text_file.close()

    # #################################################################################################################

    sqlcommand = '''
-- Author: Thomas Serrano
-- Last Updated: 8/8/2020
-- Creates a table containing gungeon item data. For the record, these are all varchars because the website i scraped this info from has text in numerical columns sometimes.
-- here icon is primary key since some items are duplicates but the sprites are unique/insinuate diff things
-- although this is automatically generated, there are some things you will need to change: 
-- master rounds: change their names to be I - V
-- Remove duplicate junk
-- for yellow chamber, change outer " to ' 
CREATE TABLE items (
    icon			VARCHAR(255),
    name			VARCHAR(255) PRIMARY KEY,
    type            VARCHAR(20),
    "quote"         VARCHAR(255),
    quality         VARCHAR(20),
    effect          VARCHAR(300)
); \n
            '''

    sql_insert = 'INSERT INTO items (icon, name, type, "quote", quality, effect) VALUES' \
                 '("{}","{}","{}","{}","{}","{}"); \n'
    for row in item_data["Icon"]:
        row = item_data[item_data["Icon"] == row]

        sqlcommand += sql_insert.format(
            row.iloc[0]["Icon"],
            row.iloc[0]["Name"],
            row.iloc[0]["Type"],
            row.iloc[0]["Quote"],
            row.iloc[0]["Quality"],
            row.iloc[0]["Effect"]
        )

    text_file = open("items.sql", "w")
    text_file.write(sqlcommand)
    text_file.close()
