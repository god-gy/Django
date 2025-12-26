from django.contrib import admin
from django.urls import path

from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('signup/', member_views.SignUpView.as_view(), name='signup'),
]
