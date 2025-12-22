from django.urls import path

from todolist.cb_views import TodoListView ,TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'cbv'

urlpatterns = [
    path('', TodoListView.as_view(), name='list'),
    path('<int:todo_pk>', TodoDetailView.as_view(), name='detail'),
    path('create/', TodoCreateView.as_view(), name='create'),
    path('<int:todo_pk>/update/', TodoUpdateView.as_view(), name='update'),
    path('<int:todo_pk>/delete/', TodoDeleteView.as_view(), name='delete'),

    path('comment/<int:todo_pk>', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:todo_pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]