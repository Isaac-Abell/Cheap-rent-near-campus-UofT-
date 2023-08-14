import googlemaps
import pandas as pd
from gethouses import get_houses

def find_cheap_rent(min, price, rooms):
    """
    Returns a pandas DataFrame with houses that fit the specified parameters and creates an Excel spreadsheet.

    Parameters:
        min_walk_time (int): The maximum time it should take to walk to uoft.
        max_price (int): The maximum rent the house should be.
        min_rooms (int): The minimum number of rooms the house should have.
    Returns:
        pandas.DataFrame: A DataFrame with all the houses that fit the parameters.
    """
    
    # make another file called key.txt that contains your api key for the distance marix api
    API = open("key.txt", "r")
    APIkey = API.read()
    MAX_MINUTES = min
    MAX_PRICE = price
    MIN_ROOMS = rooms
    
    gmaps = googlemaps.Client(key=APIkey)
    
    houses = get_houses(MAX_PRICE, MIN_ROOMS)
    
    end = "31 King's College Circle"
    
    good_distance = []

    # Uses the google matrix api to find the distance between the houses and the school
    for house in houses:
        start = house[0]
        distance = gmaps.distance_matrix(start, end, mode='walking')["rows"][0]["elements"][0]["duration"]["text"]
        if "hour" not in str(distance) and int(str(distance[:2]).strip()) <= MAX_MINUTES:
            other_stuff = {}
            other_stuff["address"] = house[0]
            other_stuff["price"] = house[1]
            other_stuff["beds"] = house[2]
            other_stuff["link"] = house[3]
            other_stuff["distance"] = distance
            good_distance.append(other_stuff)
        
    address = [x["address"] for x in good_distance]
    link = [x["link"] for x in good_distance]
    distance = [x["distance"] for x in good_distance]
    price = [x["price"] for x in good_distance]
    beds = [x["beds"] for x in good_distance]
    
    columns = ["address", "link", "distance", "price", "beds"]
    dataframe = pd.DataFrame(list(zip(address, link, distance, price, beds)), columns = columns)
    
    dataframe.to_excel("housing.xlsx")
    return(dataframe)

print(find_cheap_rent(15, 2700, 0))
