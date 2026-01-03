from django.db import models
from django.contrib.auth.models import User 
from PIL import Image

MAX_AVATAR_SIZE = 300

class Profile(models.Model):
    STATUS_CHOICES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('busy', 'Busy'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > MAX_AVATAR_SIZE or img.width > MAX_AVATAR_SIZE:
            output_size = (MAX_AVATAR_SIZE, MAX_AVATAR_SIZE)
            img.thumbnail(output_size)
            img.save(self.image.path)