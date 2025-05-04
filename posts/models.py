from django.db import models
from users.models import User

class Post(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

