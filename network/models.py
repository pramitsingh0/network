from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint


class User(AbstractUser):
    pass
class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    likers = models.ManyToManyField('User', related_name="liked_posts", default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "likes": self.likers.count(),
            "datetime": self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
        }

    def __str__(self):
        datetime = self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
        return f"Post: {self.id} by {self.author} on {datetime}"

class UserFollowing(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"User {self.user_id} follows {self.following_user_id}"
    class Meta:
        UniqueConstraint(fields=['user_id', 'following_user_id'], name="user_following")