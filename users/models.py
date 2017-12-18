from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class FollowedShows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_name = models.TextField()
    show_id = models.IntegerField()
    air_time = models.TimeField()
    air_days = models.TextField()
    summary = models.TextField()
    network = models.CharField(max_length=255)


class UnwatchedEpisode(models.Model):
    followed_show = models.ForeignKey(FollowedShows, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    episode_id = models.IntegerField()
    episode_name = models.TextField()
    season = models.IntegerField()
    episode_number = models.IntegerField()
    air_time = models.TimeField()
    air_date = models.DateField()
    air_stamp = models.DateTimeField()
    summary = models.TextField()

    class Meta:
        ordering = ["season", "episode_number"]
        unique_together = (('followed_show', 'episode_id'),)
