import googlemaps

import pandas as pd

from gethouses import get_houses

API = open("key.txt", "r")
APIkey = API.read()

MAX_MINUTES = 20
MAX_PRICE = 2500

gmaps = googlemaps.Client(key=APIkey)

houses = get_houses(MAX_PRICE)

end = "31 King's College Circle"

good_distance = []

for house in houses:
    start = house[0]
    distance = gmaps.distance_matrix(start, end, mode='walking')["rows"][0]["elements"][0]["duration"]["text"]
    if "hour" not in str(distance) and int(str(distance[:2]).strip()) <= MAX_MINUTES:
        other_stuff = {}
        other_stuff["adress"] = house[0]
        other_stuff["link"] = house[2]
        other_stuff["distance"] = distance
        other_stuff["price"] = house[1]
        good_distance.append(other_stuff)
    
adress = [x["adress"] for x in good_distance]
link = [x["link"] for x in good_distance]
distance = [x["distance"] for x in good_distance]
price = [x["price"] for x in good_distance]

columns = ["adress", "link", "distance", "price"]
dataframe = pd.DataFrame(list(zip(adress, link, distance, price)), columns = columns)

dataframe.to_excel("housing.xlsx")

print(dataframe)
