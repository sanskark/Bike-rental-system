from django.db import models
from dealer.models import Dealer
from PIL import Image
# Create your models here.

class Bike(models.Model):
    bike_id = models.IntegerField(primary_key=True, auto_created=True)
    owner = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    bike_company = models.CharField(max_length=20, default=None)
    bike_model = models.CharField(max_length=30, default=None)
    reg_number = models.CharField(max_length=10, default='')
    seat_capacity = models.DecimalField(decimal_places=0, max_digits=1, default=2)
    bike_location = models.ForeignKey('bikerental.Location', on_delete=models.CASCADE, default='')
    rent_per_day = models.PositiveIntegerField(default=0,max_length=None)
    driven_kms = models.PositiveIntegerField(default=0, max_length=None)
    is_confirmed = models.BooleanField(default=False)
    is_on_halt = models.BooleanField(default=False)
    pickup_add = models.TextField(default='')
    dropoff_add = models.TextField(default='')
    image = models.ImageField(default=None, upload_to='bike_pics')

    def __str__(self):
        return f'{self.owner.user.username}, {self.bike_model}, {self.bike_location}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        bike_img = Image.open(self.image.path)

        if bike_img.height > 150 or bike_img.width >250:
            output_size = (250, 150)
            bike_img.thumbnail(output_size)
            bike_img.save(self.image.path)

class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True, auto_created=True)
    bike = models.ForeignKey(Bike,on_delete=models.CASCADE, default='')
    customer = models.ForeignKey('customer.Customer',on_delete=models.CASCADE, default='')
    pickup_date = models.DateField(auto_now=False, auto_now_add=False)
    dropoff_date = models.DateField(auto_now=False, auto_now_add=False)
    is_completed = models.BooleanField(default=False)
    total_days = models.PositiveIntegerField(default=0)
    total_rent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.bike}, {self.customer}, {self.pickup_date}, {self.dropoff_date}'