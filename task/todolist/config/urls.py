from django.contrib import admin
from django.urls import path, include

from member import views as member_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV urls
    # path('', views.todo_list, name='todolist'),
    # path('<int:pk>/', views.todo_info, name='todoinfo'),
    # path('create/', views.todo_create, name='todo_create'),
    # path('<int:pk>/update/', views.todo_update, name='todo_update'),
    # path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),

    # USER urls
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),

    # CBV urls
    path('todo/', include('todolist.cbv_urls')),
]
