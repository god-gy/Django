from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('signup/', member_views.SignUpView.as_view(), name='signup'),
    path('verify/', member_views.verify_email, name='verify'),
    path('login/', member_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
