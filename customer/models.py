from django.db import models
from bikerental.models import User
from PIL import Image

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.user.username} Customer'

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    mobile_no = models.DecimalField(max_digits=10, decimal_places=0, blank=False, default='1234567890')
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    id_proof = models.ImageField(default='default.jpg', upload_to='id_proof_pics')
    driving_license = models.ImageField(default='default.jpg', upload_to='driving_license_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile_img = Image.open(self.profile_pic.path)
        id_img = Image.open(self.id_proof.path)
        driving_img = Image.open(self.driving_license.path)

        if profile_img.height > 300 or profile_img.width >300:
            output_size = (300, 300)
            profile_img.thumbnail(output_size)
            profile_img.save(self.profile_pic.path)

        if id_img.height > 300 or id_img.width >300:
            output_size = (300, 300)
            id_img.thumbnail(output_size)
            id_img.save(self.id_proof.path)

        if driving_img.height > 300 or driving_img.width >300:
            output_size = (300, 300)
            driving_img.thumbnail(output_size)
            driving_img.save(self.driving_license.path)