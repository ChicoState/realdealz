from django.db import models
from django.urls import reverse
import logging as log
from library import Library as lib

# Model attributes are declared here

#Allow multiple platforms
class Platform(models.Model):
    '''Model representing a game genre'''
    P = models.CharField(max_length=200, default='PC')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.P)



class Genre(models.Model):
    '''Model representing a game genre'''
    G = models.CharField(max_length=200, default='Action')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.G)
    
    


class Seller(models.Model):
    '''Model representing the source seller'''
    sources = models.URLField(max_length = 200, default='https://www.google.com/')

    def __str__(self):
        '''String for representing the Model object.'''
        return str(self.sources)
        



class Game(models.Model):
    '''Generic Game model'''

    #View the Game object in the admin panel
    def __str__(self):
        return f"{self.name} : ${self.price} - made by {self.developer}"


    appid = models.IntegerField(primary_key=True, help_text='Unique ID for this particular game')
    name = models.CharField(max_length=100, default="-1", help_text='Game title')
    price = models.FloatField(default="-1")
    discount = models.CharField(max_length=20, default="-1")
    developer = models.CharField(max_length=100, default="Unknown")
    publisher = models.CharField(max_length=100, default="Unknown")
    positive = models.CharField(max_length=100, default="-1")
    negative = models.CharField(max_length=100, default="-1")
    average_forever = models.CharField(max_length=100, default="-1")
    average_2weeks = models.CharField(max_length=100, default="-1")
    cover = models.ImageField(upload_to='images/', default='images/default.png')

    #Field can include multiple MultiFields. This allows multiple platforms and genres per game entry
    platform = models.ManyToManyField(Platform, help_text='Select Game platforms', default="PC")
    genre = models.ManyToManyField(Genre, help_text='Select Game genres', default="-1")



    @classmethod
    def initial_load(self):
        '''Load the initial library from steamspy'''
        l = lib.Library()
        _games = l.get_top_100()
        for game in _games.keys():
            _g = _games[game]
            # If the game is already in the database, skip it
            if Game.objects.filter(appid=_g['appid']).exists():
                continue
            if _g['price'] == 999:  
                _g['price'] = 0 
            # We can also verify the price here. 
            _game = Game.objects.create(
                appid = _g['appid'],
                name = _g['name'],
                price = _g['price'],
                discount = _g['discount'],
                developer = _g['developer'],
                publisher = _g['publisher'],
                positive = _g['positive'],
                negative = _g['negative'],
                average_forever = _g['average_forever'],
                average_2weeks = _g['average_2weeks'],
            )
            _game.save()
    
    @classmethod
    def clear_all(self):
        '''Clear the database'''
        Game.objects.all().delete()
        print("Database cleared")

    #! Deprecated? 
    #When clicking a link, return the respective id of the game
    def get_absolute_url(self):
        '''Returns the URL to access a detail record for this Game.'''
        return reverse('game-detail', args=[str(self.appid)])

if __name__ == "__main__":
    print("Hello World")
    # Game().initial_load