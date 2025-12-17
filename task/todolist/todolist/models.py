from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class ToDoList(models.Model):
    title = models.CharField('제목', max_length=50)
    description = models.TextField('설명')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField('시작일')
    end_date = models.DateField('종료일')
    is_complete = models.BooleanField('완료여부', default=False)
    created_at = models.DateTimeField('생성일시', auto_now_add=True)
    modified_at = models.DateTimeField('수정일시', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '할일'
        verbose_name_plural = '할일 목록'
