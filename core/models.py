from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=150)
    document = models.CharField(max_length=14)
    rg = models.CharField(max_length=12)
    birthday = models.DateField()
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Addresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return '%s - %s' % (self.customer.name, self.street)
