from django.db import models

# Model attributes are declared here
class Game(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
