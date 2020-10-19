from django.contrib import admin
from shop.models import Product,Order,OrderUpdate,User
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(User)
