from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math


/**
 * Returns a list of houses under the max price with more than the minimum number of beds
 * @param max_price The maximum rent of the house
 * @param min_beds The minimum number of beds the house must have
 * @returns An list of lists that contain the suitable houses': locations, prices, number of beds, and links to the houses
 */
def get_houses(max_price: int, min_beds: int, pages_checked = None):

    browser = webdriver.Chrome()

    browser.get("https://rentals.ca/toronto")

    link = []
    prices = []
    locations = []
    beds = []
    if pages_checked is None:
        pages_checked = browser.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/p[1]/strong[1]").text
        pages_checked = int(pages_checked[0:pages_checked.index(" ")])
        pages_checked = math.ceil(pages_checked / 10)

    for i in range(1, pages_checked):
        temp_beds = []
        temp_prices = []
        temp_locations = []
        temp_link = []

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__main-features"):
            bed = j.text
            bed = bed[0:3].strip("B").strip("-").strip()
            temp_beds.append(float(bed))

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__details-link"):
            temp_link.append(j.get_attribute("href"))

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__price"):
            price = j.text

            price = price[price.index("$")+1:].strip()
            if "-" in price:
                price = price[0:price.index("-") - 1]
            temp_prices.append(int(price))

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__title"):
            temp_locations.append(j.text)

        bad_indexes = []
        for k in range(0, len(temp_prices)):
            if temp_prices[k] > max_price or temp_beds[k] < min_beds:
                bad_indexes.append(k)

        for p in range(0, len(temp_prices)):
            if p not in bad_indexes:
                prices.append(temp_prices[p])
                link.append(temp_link[p])
                locations.append(temp_locations[p])
                beds.append(temp_beds[p])

        if i == 1:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(i+1))
            time.sleep(30)

        else:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(i+1))

    info = []

    for i in range(0, len(prices)):
        info.append([locations[i], prices[i], beds[i], link[i]])

    info.sort(key = lambda x: x[1])
    
    return info
