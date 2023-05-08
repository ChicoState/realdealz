from django.test import TestCase, Client
from django.urls import reverse
from realDealz.models import Game


class TestViews(TestCase):
    
    def test_home_GET(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
    def test_about_GET(self):
        client = Client()
        response = client.get(reverse('about'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'about.html')
    def test_game_list_GET(self):
        client = Client()
        response = client.get(reverse('catalog'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'game_list.html')
  ##  def test_game_detail_GET(self):
   ##     client = Client()
  ##      response = client.get(reverse('game-detail', args=[440]))
  ##      self.assertEquals(response.status_code,200)
  ##      self.assertTemplateUsed(response,'game_detail.html')
        

  