from django.db import models

# Model attributes are declared here
# cover = models.ImageField(upload_to='images/')
class Game(models.Model):
    '''Generic Game model'''
    title = models.CharField(max_length=100, default="Empty Game")
    price = models.CharField(max_length=20, default="-1")
    platform = models.CharField(max_length=20, default="-1")
    genre = models.CharField(max_length=20, default="-1")

    def __str__(self):
        return str(self.title)
    