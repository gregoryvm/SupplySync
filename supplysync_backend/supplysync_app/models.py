from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    sku = models.CharField(max_length=200)
    weight = models.FloatField()
    cost =  models.FloatField()
    price =  models.FloatField()
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name
