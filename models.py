from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField()
    picture = models.CharField(default='')
    year = models.CharField(blank=True)
    likeUsers = models.ManyToManyField(User, related_name="like", blank=True, null=True)
    dislikeUsers = models.ManyToManyField(User, related_name="dislike", blank=True, null=True)
    #Point is the calculation of the audience's preference to each movie, calculated by minus the likeUsers by dislikeUsers
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.title
