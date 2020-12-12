from django.db import models
from Registration.models import UserProfileInfo
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length = 50)

    subcategory = models.CharField(max_length = 50,default="")
    category = models.CharField(max_length = 50,default="")
    price = models.IntegerField()
    image = models.ImageField(upload_to = "shop/images",default="")
    desc = models.CharField(max_length = 300)
    pub_date = models.DateField()


    def __str__(self):
        return self.product_name

#
# class User(models.Model):
#     msg_id = models.AutoField(primary_key = True)
#     name = models.CharField(max_length=10)
#     email = models.EmailField()
#     phone = models.CharField(max_length=10)
#     query = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
# class query(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    order_items = models.CharField(max_length=5000)
    address = models.CharField(max_length=5000)
    city =models.CharField(max_length=5000)
    state = models.CharField(max_length=5000)
    phone = models.CharField(max_length=5000)
    zip_code = models.CharField(max_length=5000)

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key = True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
