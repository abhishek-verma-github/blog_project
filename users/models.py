from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageChops
from django.contrib.auth import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')  # , primary_key=True)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            #
            # left = 155
            # top = 65
            # right = 360
            # bottom = 270
            width, height = img.size

            if width > height:
                delta = width - height
                left = int(delta / 2)
                upper = 0
                right = height + left
                lower = height
            else:
                delta = height - width
                left = 0
                upper = int(delta / 2)
                right = width
                lower = width + upper

            img.thumbnail(output_size)
            img1 = img.crop((left, upper, right, lower))
            img.save(self.image.path)
