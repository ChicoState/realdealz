from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    context ={
        'title': 'CSCI 430 RealDealz',
        'msg': 'Hello World!',
    }
    return render(request, "home.html",context=context)
