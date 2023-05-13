from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render, redirect
from realDealz.models import Game
from django.db.models import Q
from django.db import connection
from realDealz.library import Library
from django.core.paginator import Paginator
from django.core import serializers
from realDealz.updateData import updateGamePrices
import requests
import json


def home(request):
    l = Library()
    context = {
        'title': 'Homepage',
        'msg': 'Home',
    }
    if request.method == 'POST':
        if 'load' in request.POST:
            Game.initial_load()
            updateGamePrices()
            # return redirect('Catalog')
        if 'reset' in request.POST:
            Game.clear_all()
            # return redirect('Catalog')
        if 'steam-login' in request.POST:
            if request.user.is_authenticated:
                return redirect('catalog/')
            return redirect('accounts/steam/login/')

    return render(request, "home.html", context=context)

def profile(request):
    return render(request, "profile.html")


def about(request):
    context = {
        'msg': 'About Us',
    }
    return render(request, "about.html", context=context)


def contact(request):
    context = {
        'msg': 'Contact',
    }
    return render(request, "contact.html", context=context)

def game_detail(request, game_id):
    game = Game.objects.get(appid=game_id)
    return render(request, 'game_detail.html', {'Game': game})


def game_list(request):

    games = Game.objects.all()
    paginator = Paginator(games, 50)    
    page_number = request.GET.get('page')    
    current_page = paginator.get_page(page_number)        
    filtered_table = paginator.get_page(page_number)

    context = {
        'games': games,
        'filtered_table': filtered_table,
        'current_page': current_page,  
        'page_number': page_number
    }
    return render(request, 'game_list.html', context)


def games_api(request):
    games = Game.objects.all()
    paginator = Paginator(games, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = []
    for game in page_obj:
        data.append({
            'appid': game.appid,
            'name': game.name,
            'price': game.price,
            'discount': game.discount,
            'developer': game.developer,
            'publisher': game.publisher,
            'positive': game.positive,
            'negative': game.negative,
            'average_forever': game.average_forever,
            'average_2weeks': game.average_2weeks,
        })
    return JsonResponse({'data': data, 'has_next': page_obj.has_next()})