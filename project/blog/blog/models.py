from django.db import models

# 제목, 본문, 작성자, 작성일자, 수정일자, 카테고리
# 썸네일이미지, 태그 등도 있지만 일단 우린 윗줄만 함

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)

    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    # author = models.ForeignKey() -> 추후에
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blog list'
