import requests
import json
from bs4 import BeautifulSoup

def m_get(url: str):
    response = requests.get(url)
    data = response.json()
    return data

def getWishlistFromID(steam_ID: str):
    """This is a function that gets the wishlist of a user from their steamID"""
    url = f"https://store.steampowered.com/wishlist/profiles/{steam_ID}/wishlistdata/"
    return m_get(url)


def getGameData(app_ID: int):
    """This is a function that gets the game data from the appID"""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_ID}&l=en_us"
    return m_get(url)

if __name__ == "__main__":
    wishlist = getWishlistFromID("76561198180301021")
    a_id = list(wishlist.keys())[0]
    game_data = getGameData(a_id)
    print(game_data[a_id]["data"])



    # for app_id, app_data in wishlist.items():
    #     print(app_data["name"])

