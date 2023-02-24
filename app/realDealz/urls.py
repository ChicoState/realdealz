"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from realDealz import views as home
#from app import views as app_views #for app in template folder left commented to rename
#from library import views as library_views #for library in template folder
#kinda confused why templates also has a urls page
urlpatterns = [
    path('', home.home, name='index'),
    path('admin/', admin.site.urls),
    #path('', ), #for app
    #path('', ) #for lib
]
