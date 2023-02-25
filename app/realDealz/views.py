from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from .models import Game


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

class catalog(generic.ListView):
    model = Game;
