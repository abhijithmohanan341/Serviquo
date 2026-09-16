from django.db import models
from Shop.models import *
from Guest.models import *
from Admin.models import *



class tbl_product(models.Model):
    product_name=models.CharField(max_length=50)
    product_details=models.CharField(max_length=100)
    product_photo=models.FileField(upload_to="Assets/User/Photo")
    product_price=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category, on_delete=models.CASCADE)
    shop=models.ForeignKey(tbl_shop, on_delete=models.CASCADE)



class tbl_stock(models.Model):
    stock_Qty=models.CharField(max_length=50)
    stock_date=models.DateField(auto_now_add=True)
    product=models.ForeignKey(tbl_product, on_delete=models.CASCADE)