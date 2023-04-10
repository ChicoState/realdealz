from django.core.management.base import BaseCommand
from realDealz.models import Game
import http.client
import json


class Command(BaseCommand):
    help = 'Fetches the latest price for each game in the database'

    def handle(self, *args, **options):
       
        appids = [game.appid for game in Game.objects.all()]

        for appid in appids:
            # Construct URL for the API request
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

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
                game_data = response_json[str(appid)]['data']
                price_data = game_data.get('price_overview')

                # Update price information in database
                game = Game.objects.get(appid=appid)
                if price_data:
                    game.price = price_data['final_formatted']
                    game.discount = price_data.get('discount_percent', None)
                else:
                    game.price = "N/A"
                    game.discount = "N/A"
                game.save()

                # Print success message
                self.stdout.write(self.style.SUCCESS(f"Updated price for game {game.name} to {game.price}"))
            else:
                self.stderr.write(self.style.ERROR(f"Error: {response.reason}"))

            conn.close()