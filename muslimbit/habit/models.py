from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/",null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"