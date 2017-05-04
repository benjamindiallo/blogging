from django.db import models
from django.contrib.auth.models import User
from blogging.core.models import TimestampedModel


class Post(TimestampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
