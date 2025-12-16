from django.contrib import admin
from django.urls import path, include

from todolist import views
from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.todo_list, name='todolist'),
    path('/<int:pk>', views.todo_info, name='todoinfo'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
]
