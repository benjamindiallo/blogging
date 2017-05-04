from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blogging.posts.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=300, blank=True)
    follows = models.ManyToManyField('self',
                                     related_name='followed_by',
                                     symmetrical=False,
                                     blank=True
                                     )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def follow(self, user_to_follow):
        self.follows.add(user_to_follow)

    def unfollow(self, user_to_unfollow):
        self.follows.remove(user_to_unfollow)

    @property
    def feed(self):
        followings = self.follows.all().values('id')
        followings_ids = [following['id'] for following in followings]
        return Post.objects.filter(user_id__in=followings_ids)\
                           .order_by('-create_at')

    @property
    def posts(self):
        return Post.objects.filter(user=self.user)

    @property
    def followers(self):
        return self.followed_by.all()

    @property
    def followings(self):
        return self.follows.all()
