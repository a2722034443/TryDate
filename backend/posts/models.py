from django.db import models
from django.conf import settings


class Post(models.Model):
    class PostStatus(models.TextChoices):
        ACTIVE = 'active', '正常'
        HIDDEN = 'hidden', '隐藏'
        DELETED = 'deleted', '已删除'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    is_anonymous = models.BooleanField(default=False)
    content = models.CharField(max_length=200)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = '动态'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.nickname}: {self.content[:30]}'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = '点赞'

