from django.db import models
from django.urls import reverse

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


#Model Breakdown
#Title: Name of game
#Price: This should list the lowest price of the game
#Platform: This should include all platforms (Ex. Windows, Linux, Playstation, etc..)
#Genre: This should include all genres to the game (Ex. Action, Strategy, Survival, etc.. )
class Game(models.Model):
    '''Generic Game model'''
    title = models.CharField(max_length=100, default="Empty Game", help_text='Give title')
    price = models.CharField(max_length=20, default="-1")
    game_id = models.AutoField(primary_key=True)


    #Field can include multiple MultiFields. This allows multiple platforms and genres per game entry
    platform = models.ManyToManyField(Platform, help_text='Select Game platforms', default=DefaultPlatforms)
    genre = models.ManyToManyField(Genre, help_text='Select Game genres', default=DefaultGenres)
    vendors = models.ManyToManyField(Seller, help_text='Links to all vendors', default=DefaultSellers)

    def __str__(self):
        return str(self.title)
    
    #When clicking a link, return the respective id of the game
    def get_absolute_url(self):
     '''Returns the URL to access a detail record for this Game.'''
     return reverse('game-detail', args=[str(self.game_id)])