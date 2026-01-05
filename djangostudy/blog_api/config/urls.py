from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from comments.views import CommentViewSet  # CommentViewSet 임포트
from posts.views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")  # 기존
router.register(
    r"comments", CommentViewSet, basename="comment"
)  # 새 추가, basename 지정 베스트 프랙티스

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),  # 세션 1에서 추가된 부분 유지
    path("api/", include(router.urls)),  # router URL 통합
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
