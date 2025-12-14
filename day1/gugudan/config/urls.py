from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

def index(request):
    return HttpResponse("<html><body><h1>Hello World</h1></body></html>")

def gugu(request, num):
    context ={
        'num' : num,
        'results' : [num * i for i in range(1, 10)]
    }
    return render(request, 'gugu.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('gugu/<int:num>', gugu),
]
