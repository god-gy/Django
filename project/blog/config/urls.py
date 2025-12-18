from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, reverse
from django.views import View
from django.views.generic import TemplateView, RedirectView

from blog import views
from member import views as member_views


class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(View):
    def get(self, request):
        return render(request, 'test_get.html')
    def post(self, request):
        return render(request, 'test_post.html')

# def test_view(request):
#     if request.method == 'POST':
#         ...
#     if request.method == 'GET':
#         ...

urlpatterns = [
    # blog
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/update/', views.blog_update, name='blog_update'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('about/', AboutView.as_view(), name='about'),
    path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # path('redirect2/', lambda req : redirect(reverse('about')),name='redirect2'),
    path('test/', TestView.as_view(), name='test'),
]
