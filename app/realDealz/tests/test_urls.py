from django.test import SimpleTestCase
from django.urls import reverse, resolve
from realDealz.views import home, game_list,about, game_detail


class TestUrls(SimpleTestCase):
    def test_smoke(self):
        assert 1 == 1 
    def test_home_url_is_resolved(self):
        url = reverse('home')  
        self.assertEquals(resolve(url).func,home)
        
    def test_catalog_url_is_resolved2(self):
        url = reverse('catalog')
        self.assertEquals(resolve(url).func,game_list)
    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func,about)
    def test_about_url_is_resolved(self):
        url = reverse('game-detail',args=['440'])
        self.assertEquals(resolve(url).func,game_detail)