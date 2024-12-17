from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 文章模型
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="作者", default=2)
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True, verbose_name="点赞用户")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        """返回文章的点赞数"""
        return self.likes.count()

# 评论模型
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="所属文章")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="评论者")
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="评论时间")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="父评论")
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True, verbose_name="点赞用户")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['created_at']

    def __str__(self):
        return f"评论者：{self.author.username}，评论：{self.content[:20]}..."

    def total_likes(self):
        """返回评论的点赞数"""
        return self.likes.count()

    def is_reply(self):
        """判断是否是回复评论"""
        return self.parent is not None

# # 点赞记录模型（可选）
# class LikeRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="点赞用户")
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, verbose_name="文章")
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, verbose_name="评论")
#     created_at = models.DateTimeField(default=timezone.now, verbose_name="点赞时间")

#     class Meta:
#         verbose_name = "点赞记录"
#         verbose_name_plural = "点赞记录"
#         unique_together = [['user', 'article'], ['user', 'comment']]

#     def __str__(self):
#         if self.article:
#             return f"{self.user.username} 点赞了文章 '{self.article.title}'"
#         elif self.comment:
#             return f"{self.user.username} 点赞了评论 '{self.comment.content[:20]}...'"
