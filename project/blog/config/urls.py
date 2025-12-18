from django.contrib import admin
from django.urls import path, include

from blog import views, cv_views
from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV blog
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/update/', views.blog_update, name='blog_update'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # CBV blog
    path('cv/', cv_views.BlogListView.as_view(), name='cv_blog_list'),
    path('cv/<int:pk>/', cv_views.BlogDetailView.as_view(), name='cv_blog_detail'),
    path('cv/create/', cv_views.BlogCreateView.as_view(), name='cv_blog_create'),
    path('cv/<int:pk>/update/', cv_views.BlogUpdateView.as_view(), name='cv_blog_update'),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),


]
