from django.test import TestCase
from realDealz.models import Game #, Platform, Genre

class TestModels(TestCase):
    
    def setUp(self):
        self.game1 = Game.objects.create(
            name='Game 1',
            price=10.0,
            developer='Developer 1',
            publisher='Publisher 1',
            positive='Positive review',
            negative='Negative review',
            average_forever='10 hours',
            average_2weeks='2 hours'
        )
    
    def test_game_str_method(self):
        self.assertEqual(str(self.game1), 'Game 1 : $10.0 - made by Developer 1')
    
    def test_game_initial_load(self):
        Game.initial_load()
        game = Game.objects.filter(name='Terraria')
        self.assertTrue(game.exists())
    
    def test_game_clear_all(self):
        Game.clear_all()
        self.assertEqual(Game.objects.count(), 0)

