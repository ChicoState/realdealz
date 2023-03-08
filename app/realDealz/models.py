from django.db import models
from django.urls import reverse
import logging as log
from . import library as lib

# Model attributes are declared here

# ImageField requires Pillow to use. WIP
# cover = models.ImageField(upload_to='images/')


#Allow multiple platforms
class Platform(models.Model):
    '''Model representing a game genre'''
    P = models.CharField(max_length=200, default='PC')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.P)
    
#Default value for platforms
def DefaultPlatforms():
    return ['PC']
    
class Genre(models.Model):
    '''Model representing a game genre'''
    G = models.CharField(max_length=200, default='Action')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.G)
    
def DefaultGenres():
    return ['Action']
    
class Seller(models.Model):
    '''Model representing the source seller'''
    sources = models.URLField(max_length = 200, default='https://www.google.com/')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.sources)
    
def DefaultSellers():
    return ['https://www.google.com/']




# Here is an example record from a steamspy GET request 
# "appid": 570,
#     "name": "Dota 2",
#     "developer": "Valve",
#     "publisher": "Valve",
#     "score_rank": "",
#     "positive": 1603433,
#     "negative": 335731,
#     "userscore": 0,
#     "owners": "200,000,000 .. 500,000,000",
#     "average_forever": 37644,
#     "average_2weeks": 1338,
#     "median_forever": 798,
#     "median_2weeks": 809,
#     "price": "0",
#     "initialprice": "0",
#     "discount": "0",
#     "ccu": 532383

class Game(models.Model):
    '''Generic Game model'''
    appid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Empty Game", help_text='Give title')
    price = models.CharField(max_length=20, default="-1")
    discount = models.CharField(max_length=20, default="-1")
    developer = models.CharField(max_length=100, default="Unknown")
    publisher = models.CharField(max_length=100, default="Unknown")
    positive = models.CharField(max_length=100, default="-1")
    negative = models.CharField(max_length=100, default="-1")
    average_forever = models.CharField(max_length=100, default="-1")
    average_2weeks = models.CharField(max_length=100, default="-1")


    #Field can include multiple MultiFields. This allows multiple platforms and genres per game entry
    platform = models.ManyToManyField(Platform, help_text='Select Game platforms', default=DefaultPlatforms)
    genre = models.ManyToManyField(Genre, help_text='Select Game genres', default=DefaultGenres)
    vendors = models.ManyToManyField(Seller, help_text='Links to all vendors', default=DefaultSellers)

    def __str__(self):
        return f"{self.name} : ${self.price} - made by {self.developer}"

    @classmethod
    def initial_load(self):
        '''Load the initial library from steamspy'''
        l = lib.Library()
        _games = l.get_top_100()
        for game in _games.keys():
            _game = Game.objects.create(
                appid = _games[game]['appid'],
                name = _games[game]['name'],
                price = _games[game]['price'],
                discount = _games[game]['discount'],
                developer = _games[game]['developer'],
                publisher = _games[game]['publisher'],
                positive = _games[game]['positive'],
                negative = _games[game]['negative'],
                average_forever = _games[game]['average_forever'],
                average_2weeks = _games[game]['average_2weeks'],
            )
            _game.save()
    
    @classmethod
    def clear_all(self):
        '''Clear the database'''
        Game.objects.all().delete()
        print("Database cleared")

    #When clicking a link, return the respective id of the game
    def get_absolute_url(self):
        '''Returns the URL to access a detail record for this Game.'''
        return reverse('game-detail', args=[str(self.appid)])

if __name__ == "__main__":
    print("hekkio")
    Game().initial_load