import requests
from bs4 import BeautifulSoup
import pandas as pd

year = 2022 # Set to year you want to pull. Pulls top 25 passers from specified year.

## Gets data for the year specified.
def Get_Data(year):
    try:
        URL = "https://www.nfl.com/stats/player-stats/category/passing/" + str(year) + "/reg/all/passingyards/desc"

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(class_="d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable") # Find class containing the table.

        r_data = results.tbody
    except:
        print("----------Error getting data from webpage---------------")
    else:
        raw_data = r_data.find_all("tr") # Get all rows of the table

        return raw_data

## From the raw data get years for first row.
def Get_Players(raw_data):
    quarterbacks = []
    for child in raw_data:
        player = [year]
        for x in child:
            player.append(x.text)
        quarterbacks.append(player)

    return quarterbacks


## Can pull from multiple years as well. Update the year to the max year you want pulled.

## Create a list to add all of this data too and a for loop to pull for each year.
quarterbacks = []
for x in range(45): ## set to one less than you want to pull. Ex. 15 will pull 2022 - 2018
    data = Get_Players(Get_Data(year))
    quarterbacks.extend(data) ## add the data to established list
    year = year - 1
    print(str(year) + " successfully loaded!")

df = pd.DataFrame(quarterbacks)
df.to_csv('nflquarterbackstats.csv', index= False)