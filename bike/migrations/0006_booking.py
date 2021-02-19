# Generated by Django 3.1.5 on 2021-02-18 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('bike', '0005_auto_20210204_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('pickup_date', models.DateField()),
                ('dropoff_date', models.DateField()),
                ('bike_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bike.bike')),
                ('customer_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]