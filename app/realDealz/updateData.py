from realDealz.models import Game
import http.client
import json
import logging as log
from bs4 import BeautifulSoup
import re


def updateGamePrices(): 
    appids = [game.appid for game in Game.objects.all()]
    log.info("updating Game Prices")

    for appid in appids:
        # Construct URL for the API request
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=en_us"
        # Send API request and get response
        conn = http.client.HTTPSConnection("store.steampowered.com")
        conn.request("GET", url)
        response = conn.getresponse()

        if response.status == 200:
            # Decode response data and parse JSON
            data = response.read()
            response_str = data.decode('utf-8')
            response_json = json.loads(response_str)

            # Extract price data from JSON
            if response_json[str(appid)].get('data') is None:
                log.info("No Data found")
                continue

            game_data = response_json[str(appid)]['data']

            price_data = game_data.get('price_overview')
            soup = BeautifulSoup(game_data.get('detailed_description'), 'html.parser')
            about_data = soup.get_text().strip()
    
            platform_data = game_data.get('platforms')
            
            temp = game_data.get('genres')
            
            temp2= re.sub("[^a-zA-Z]",' ', str(temp))
            
            temp3  = temp2.replace('id', '')
            genre_data = temp3.replace('description', '')
            
            if price_data is None: 
                # Happens when game is free to play
                continue
                # log.error(f"price data not valid skipping: {appid}")
                # print(f"{game_data.get('name')}")
            # Update price information in database
            game = Game.objects.get(appid=appid)
    
            try: 
                if price_data.get('final_formatted') is not None:
                    price = price_data['final_formatted'].split("$")[1].split(" ")[0]

                    print(f"{appid}: {price_data['final_formatted']} ... {price}")
                    game.price = price
                    game.discount = price_data.get('discount_percent', None)
                else:
                    game.price = 0
                    game.discount = "N/A"    

                game.save()
            except Exception as e: 
                print(e)
                print(price_data)
            try:
                if about_data:
                    game.about = about_data
                else:
                    game.about = "loaded nothing, probably empty"
                game.save()
            except Exception as a:
                print(a)
                print(about_data)
            try:
                if genre_data is not None:
                    game.genre = genre_data
                else:
                    game.genre = "its a game, idk what else to tell ya"
                game.save()
            except Exception as g:
                print(g)
                print(genre_data)
            try:
                if platform_data.windows:
                    game.platform = platform_data.windows
                else:
                    game.platform = "unknown"
                game.save()
            except Exception as p:
                print(p)
                print(platform_data)
            
                
        else: 
            log.error("update game price response error: (Non 200)")

        conn.close()