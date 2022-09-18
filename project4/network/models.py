from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    liked_posts = models.ManyToManyField("Post", related_name="likers")

    def post_likes(self):
        return self.liked_posts.values_list('id', flat=True)

    def __str__(self):
        return f"{self.username} : {self.email}"


class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("User", related_name="followers", on_delete=models.CASCADE)


class Post(models.Model):
    body = models.CharField(max_length=5000)
    likes = models.IntegerField(default=0)
    poster = models.ForeignKey(User, related_name="user_posts", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now(), null=True)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "poster": self.poster.username,
            "timestamp": self.timestamp
        }