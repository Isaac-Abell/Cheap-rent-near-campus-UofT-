import googlemaps
import pandas as pd
from gethouses import get_houses

/**
 * Returns a pandas dataframe with all the houses that are within the parameters and makes an excel spreadsheet with the info
 * @param min The maximum time it should take to walk to uoft
 * @param price The maximum rent the house should be
 * @param rooms The minimum number of rooms the house should have
 * @returns A pandas dataframe with all the houses that fit the parameters
 */
def find-cheap-rent(min, price, rooms):
    //make another file called key.txt that contains your api key for the distance marix api
    API = open("key.txt", "r")
    APIkey = API.read()
    MAX_MINUTES = min
    MAX_PRICE = price
    MIN_ROOMS = rooms
    
    gmaps = googlemaps.Client(key=APIkey)
    
    houses = get_houses(MAX_PRICE, MIN_ROOMS)
    
    end = "31 King's College Circle"
    
    address = []
    price = []
    beds = []
    link = []
    distance = []
    
    for house in houses:
        start = house[0]
        distance = gmaps.distance_matrix(start, end, mode='walking')["rows"][0]["elements"][0]["duration"]["text"]
        if "hour" not in str(distance) and int(str(distance[:2]).strip()) <= MAX_MINUTES:
            other_stuff = {}
            address.append(house[0])
            price.append(house[1])
            beds.append(house[2])
            link.append(house[3])
            distance.append(distance)
        
    
    
    columns = ["address", "link", "distance", "price", "beds"]
    dataframe = pd.DataFrame(list(zip(address, link, distance, price, beds)), columns = columns)
    dataframe.to_excel("housing.xlsx")
    return(dataframe)

print(find-cheap-rent(15, 2700, 0))
