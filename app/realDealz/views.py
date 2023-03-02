from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from .models import Game
from django.db.models import Q


def home(request):
    context ={
        'title': 'Homepage',
        'msg': 'Home',
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

class catalog(generic.ListView):
    model = Game
