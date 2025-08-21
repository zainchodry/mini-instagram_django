from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.user.username
            slug = slugify(base)
            counter = 0
            unique = slug
            while Profile.objects.filter(slug=unique).exists():
                counter += 1
                unique = f"{slug}-{counter}"
            self.slug = unique
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} Profile"


    def followers_count(self):
        return self.followers.count()


    def following_count(self):
        return self.following.count()