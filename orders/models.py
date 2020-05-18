from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Menu_Pizza(models.Model):
    name = models.CharField(max_length=100)
    small = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    large = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Small ==== ${self.small} | Large ====  ${self.large}"


class Menu_Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Menu_Sub(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    large = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Small ==== ${self.small} | Large ====  ${self.large}"


class Menu_Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Price ==== ${self.price}"


class Menu_Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Price ==== ${self.price}"


class Menu_Dinner_Platter(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    large = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Small ==== ${self.small} | Large ====  ${self.large}"


class Menu_Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Price ==== ${self.price}"


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_order = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField(max_length=64, default="Initiated")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user} | Status: {self.status} | Total: ${self.total_order} | Date: {self.date}"


class All_Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    order_item = models.CharField(max_length=64)
    extras = models.CharField(max_length=512)
    item_price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user} | Order ID: {self.order_id} | Item: {self.order_item} | Extras: {self.extras} | Price = {self.item_price}"
