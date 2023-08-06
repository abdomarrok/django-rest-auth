from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone_number = models.CharField(max_length=15)
    identity_piece = models.ImageField(upload_to='identity_images/')
    identity_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username