from django.urls import path

from todolist.cb_views import TodoListView ,TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView

app_name = 'cbv'

urlpatterns = [
    path('', TodoListView.as_view(), name='list'),
    path('<int:pk>', TodoDetailView.as_view(), name='detail'),
    path('create/', TodoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='delete'),
]