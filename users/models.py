from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(User):
    class Meta:
        proxy = True

    def is_following(self, show_id):
        """Return FollowedShows object if show_id matches else None"""
        try:
            return self.followedshows_set.get(show_id=show_id)
        except FollowedShows.DoesNotExist:
            return None


class FollowedShows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_name = models.TextField()
    show_id = models.IntegerField()
    air_time = models.TimeField()
    air_days = models.TextField()
    summary = models.TextField()
    network = models.CharField(max_length=255)
