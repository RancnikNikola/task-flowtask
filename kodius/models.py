from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    last_supported_year = models.IntegerField(null=True)
    chain_change_price = models.FloatField(null=True)
    oil_and_oil_filter_change_price = models.FloatField(null=True)
    air_filter_change_price = models.FloatField(null=True)
    brake_fluid_change_price = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, blank=True, null=True)
    model_year = models.IntegerField(null=True)
    mileage = models.IntegerField(null=True)
    choose_date = models.DateField(null=True)

    chain_change_price = models.BooleanField(null=True, default=False)
    oil_and_oil_filter_change_price = models.BooleanField(null=True, default=False)
    air_filter_change_price = models.BooleanField(null=True, default=False)
    brake_fluid_change_price = models.BooleanField(null=True, default=False)

    order_status = models.BooleanField(null=True, default=True)

    def get_absolute_url(self):
        return reverse('order_details', kwargs={'pk': self.pk})
