from django.urls import path

from blog import cv_views

app_name = 'blog'

urlpatterns = [
    # CBV blog
    path('', cv_views.BlogListView.as_view(), name='list'),
    path('<int:blog_pk>/', cv_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cv_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cv_views.BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', cv_views.BlogDeleteView.as_view(), name='delete'),

    path('comment/create/<int:blog_pk>/', cv_views.CommentCreateView.as_view(), name='comment_create'),
]
