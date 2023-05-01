from realDealz.models import Game
import http.client
import json
import logging as log
from bs4 import BeautifulSoup


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
            soup = BeautifulSoup(game_data.get('about_the_game'), 'html.parser')
            about_data = soup.get_text().strip()
            platform_data = game_data.get('platforms')
            

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

                    # log.debug(f"{appid}: {price_data['final_formatted']} ... {price}")
                    game.price = price
                    game.discount = price_data.get('discount_percent', None)
                else:
                    game.price = 0
                    game.discount = "N/A"
             
                if about_data:
                    game.about = about_data
                else:
                    game.about = 'n/a'
                game.save()
            except Exception as e: 
                print(e)
                print(price_data)
        else: 
            log.error("update game price response error: (Non 200)")

        conn.close()
    log.info("Game Prices Finished Updated")