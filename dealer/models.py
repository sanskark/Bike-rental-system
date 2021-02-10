from django.db import models
from bikerental.models import User
from PIL import Image
# Create your models here.

class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0, blank=False, default='1234567890')

    def __str__(self):
        return f'{self.user.username} Dealer'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class DealerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='dealer_profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile_img = Image.open(self.profile_pic.path)

        if profile_img.height > 300 or profile_img.width >300:
            output_size = (300, 300)
            profile_img.thumbnail(output_size)
            profile_img.save(self.profile_pic.path)

