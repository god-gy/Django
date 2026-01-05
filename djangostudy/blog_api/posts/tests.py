from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import CustomUser

from .models import Post
from .serializers import PostSerializer


# 모델 필드 값 저장/조회 검증
class PostModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="author", password="pass")

    def test_create_post(self):
        post = Post.objects.create(
            title="Test Title", content="Test Content", author=self.user
        )
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.author.username, "author")


# 유효성 검사 로직 확인
# `serializer.errors`를 이용해 어떤 필드가 실패했는지 명확하게 확인 가능
class PostSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="author", password="pass")
        self.post_data = {
            "title": "Valid Title",
            "content": "Valid Content",
            "author": self.user.id,
        }

    def test_valid_serializer(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_title(self):
        invalid_data = self.post_data.copy()
        invalid_data["title"] = "4444"
        serializer = PostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)


# 실제 요청/응답 시뮬레이션
# reverse()로 URL 하드코딩 방지, force_authenticate()로 인증 처리
class PostAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Existing Post", content="Content", author=self.user
        )

    def test_get_posts(self):
        url = reverse("post-list")  # basename='post' 기준
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post(self):
        url = reverse("post-list")
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
