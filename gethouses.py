from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math

def get_houses(max_price: int, min_beds: int, pages_checked = None):
    """
    Returns a list of houses that are priced under the specified maximum price and have more
    than the specified minimum number of beds, along with their locations, prices, number of beds,
    and links to the houses.

    Parameters:
        max_price (float): The maximum rent of the house.
        min_beds (int): The minimum number of beds the house must have.
        pages_checked (int): How many pages of the website should be checked for houses

    Returns:
        list: A list of lists, each containing information about suitable houses.
            Each inner list contains: location, price, number of beds, and house link.
    """
        
    browser = webdriver.Chrome()

    browser.get("https://rentals.ca/toronto")

    link = []
    prices = []
    locations = []
    beds = []

    # checks all pages if pages_checked is none
    # since the website has 10 houses per page, it will look at (all listings/10) pages
    if pages_checked is None:
        pages_checked = browser.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/p[1]/strong[1]").text
        pages_checked = int(pages_checked[0:pages_checked.index(" ")])
        pages_checked = math.ceil(pages_checked / 10)


    for page_number in range(1, pages_checked):
        temp_beds = []
        temp_prices = []
        temp_locations = []
        temp_link = []
        
        # gets the number of beds
        for j in browser.find_elements(By.CLASS_NAME, "listing-card__main-features"):
            bed = j.text
            bed = bed[0:3].strip("B").strip("-").strip()
            temp_beds.append(float(bed))

        # gets the link of the apartment
        for j in browser.find_elements(By.CLASS_NAME, "listing-card__details-link"):
            temp_link.append(j.get_attribute("href"))

        # gets the price of the apartment
        for j in browser.find_elements(By.CLASS_NAME, "listing-card__price"):
            price = j.text

            price = price[price.index("$")+1:].strip()
            if "-" in price:
                price = price[0:price.index("-") - 1]
            temp_prices.append(int(price))

        # gets the name adress of the apartment
        for j in browser.find_elements(By.CLASS_NAME, "listing-card__title"):
            temp_locations.append(j.text)

        # adds the apartment to the return list if it fits the criteria
        for apartment in range(0, len(temp_prices)):
            if temp_prices[apartment] <= max_price or temp_beds[apartment] >= min_beds:
                prices.append(temp_prices[apartment])
                link.append(temp_link[apartment])
                locations.append(temp_locations[apartment])
                beds.append(temp_beds[apartment])

        # sometimes a popup may appear on the second page, so it waits 30 seconds for it to dissapear
        if page_number == 1:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(page_number+1))
            time.sleep(30)

        else:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(page_number+1))

    info = []

    for i in range(0, len(prices)):
        info.append([locations[i], prices[i], beds[i], link[i]])

    info.sort(key = lambda x: x[1])
    
    return info
