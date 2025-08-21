from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User



def post_image_upload_path(instance, filename):

    return f"posts/{instance.author.username}/{filename}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=post_image_upload_path)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post({self.author}, {self.created_at:%Y-%m-%d %H:%M})"

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"

