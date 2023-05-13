from django.test import TestCase, Client
from django.urls import reverse
from realDealz.models import Game
import json
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        Game.objects.create(
            appid="440"
        )
    def test_home_GET(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
    def test_home_POST(self):
        client = Client()
        response = client.post(reverse('home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
    def test_home_POST_reset(self):
        client = Client()
        response = client.post(reverse('home'), {'reset': True})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
    def test_home_POST_load(self):
        client = Client()
        response = client.post(reverse('home'), {'load': True})
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
    def test_game_detail_GET(self):
        client = Client()
        response = client.get(reverse('game-detail', args=[440]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'game_detail.html')
    def test_contact_GET(self):
        client = Client()
        response = client.get(reverse('contact'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'contact.html')
    def test_profile_GET(self):
        client = Client()
        response = client.get(reverse('profile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'profile.html')
    def test_game_api_GET(self):
        client = Client()
        response = client.get(reverse('games_api'))
        self.assertEquals(response.status_code,200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.assertIn('has_next', content)
    
    
    ##def test_home_POST_Steam(self):
     #   client = Client()
      #  response = client.post(reverse('home'), {'steam-login': True})
      #  self.assertEquals(response.status_code,302)## 302 = redirect
      #  if self.user.is_authenticated:
      #      self.assertRedirects(response, reverse('catalog'), fetch_redirect_response=False)
      #  else:
      #      self.assertRedirects(response, '/accounts/steam/login/', fetch_redirect_response=False)

        # Check that the expected template is used
      #  self.assertTemplateUsed(response, 'home.html')
  