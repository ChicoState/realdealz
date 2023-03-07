#pylint: disable=no-member
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from .models import Game
from django.db.models import Q
from django.db import connection
from .load_library import Library


def home(request):
    l = Library()
    context ={
        'title': 'Homepage',
        'msg': 'Home',
        'games': l.search_all(),
    }
    return render(request, "home.html",context=context)

def about(request):
    context ={
        'msg': 'About Us',
    }
    return render(request, "about.html",context=context)

def contact(request):
    context ={
        'msg': 'Contact',
    }
    return render(request, "contact.html",context=context)

def game_search(request):
    pass
    # query = request.GET.get('q')
    # games = Game.objects.filter(
    #     Q(title__icontains=query) | Q(platform__icontains=query) | Q(genre__icontains=query)
    # )
    # return render(request, 'game_search.html', {'games': games})
    
    
def game_detail(request, game_id):
    game = Game.objects.get(game_id=game_id)
    return render(request, 'game_detail.html', {'Game': game})



class catalog(generic.ListView):
    '''Catalog view for all games in the database used for catalog page'''
    model = Game
    paginate_by = 10
    