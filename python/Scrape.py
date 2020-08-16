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
                data = cell.contents[0].contents[0].get("alt", "")
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
                gungeon_data[header_order[4]].append("D Quality Item.png")
                gungeon_data[header_order[5]].append("Thrown guns will explode. | Thrown guns will explode. Grants immunity to contact damage. Moving constantly without rolling or taking damage for 4 seconds charges a dodge roll, which will deal 300 damage.")
                skipnext = False
                break
            if i == 0 or i == 4:
                # get icon name
                for child in cell.contents:
                    if type(child) == NavigableString:
                        continue
                    data += child.contents[0].get("alt", "")
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
    gun_data.to_csv("weapons.csv")

    # scrape item data
    item_data = scrapeItems(url, paths)
    item_data.to_csv("items.csv")
