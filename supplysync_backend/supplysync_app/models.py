from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200,unique=True)
    category = models.CharField(max_length=200,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    quantity = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    cost =  models.FloatField(null=True)
    price =  models.FloatField(null=True)
    
    #class Meta:
    #    constraints = [
    #        models.UniqueConstraint(
    #            fields=('sku','user'),
    #            name = "unique sku by user"
    #        )
    #    ]

    
    def __str__(self):
        return self.name

