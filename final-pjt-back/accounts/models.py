from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    profile_image = ProcessedImageField(
        blank=True,
        default='media/default.png',
        upload_to='profile_images/%Y/%m/%d/',
        processors=[ResizeToFill(200,200)],
        format='JPEG',
        options={'quality': 100}
        )
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')