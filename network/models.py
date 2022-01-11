from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    likers = models.ManyToManyField('User', related_name="liked_posts", default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __serialize__(self):
        return {
            "id": self.id,
            "author": self.author,
            "body": self.body,
            "likes": self.likes.count(),
            "datetime": self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
        }

    def __str__(self):
        datetime = self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
        return f"Post: {self.id} by {self.author} on {datetime}"