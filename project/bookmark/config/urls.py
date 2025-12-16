"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import path

from bookmark import views

movie_list = [
    {'title' : '파묘', 'director' : '장재현'},
    {'title' : '웡카', 'director' : '폴 킹'},
    {'title' : '듄', 'director' : '드니 빌뇌브'},
    {'title' : '시민덕희', 'director' : '박영주'},
]

def index(request):
    return HttpResponse("<html><body><h1>Hello World</h1></body></html>")

def book_list(request):
    # book_text = ''
    # for i in range(10):
    #     book_text += f'book {i} <br>'
    return render(request, 'book_list.html', {'range': range(10)})

def book(request, num):
    return render(request, 'book.html', {'num' : num})

def language(request, leng):
    return HttpResponse(f'<h1>{leng} 언어 페이지 입니다.</h1>')


def movies(request):
    # movie_titles = [
    #     f'<a href="/movie/{index}/">{movie['title']}</a>'
    #     for index, movie in enumerate(movie_list)]
    # response_text = '<br>'.join(movie_titles)

    return render(request, 'movies.html', {'movie_list': movie_list})

def movie_detail(request, index):

    if index > len(movie_list)-1:
        raise Http404

    movie = movie_list[index]
    return render(request, 'movie.html', {'movie': movie})

# path 순서대로 읽음, str은 주의해서 사용하길.
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),
    # path('book_list/', book_list),
    # path('book_list/<int:num>/', book),
    # path('language/<str:leng>/', language),
    # path('movie/', movies),
    # path('movie/<int:index>/', movie_detail),
    path('bookmark/', views.bookmark_list),
    path('bookmark/<int:pk>/', views.bookmark_detail),
]
