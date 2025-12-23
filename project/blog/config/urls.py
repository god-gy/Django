from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV blog
    path('fb/', include('blog.fbv_urls')),

    # CBV blog
    path('', include('blog.urls')),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # summernote
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
