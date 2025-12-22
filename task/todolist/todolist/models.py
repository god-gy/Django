from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.models import TimeStampedModel

User = get_user_model()

class ToDoList(TimeStampedModel):
    title = models.CharField('제목', max_length=50)
    description = models.TextField('설명')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField('시작일')
    end_date = models.DateField('종료일')
    is_complete = models.BooleanField('완료여부', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cbv:detail', kwargs={'todo_pk': self.pk})

    class Meta:
        verbose_name = '할일'
        verbose_name_plural = '할일 목록'

class Comment(TimeStampedModel):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='comments')
    massage = models.CharField('본문', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.todolist.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', )
