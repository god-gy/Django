from django.contrib import admin
from django.urls import path, include

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
]
