from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField()
    quantity = models.IntegerField()
    sku = models.CharField()
    weight = models.FloatField()
    cost =  models.FloatField()
    price =  models.FloatField()
    category = models.CharField()

    def __str__(self):
        return self.name
