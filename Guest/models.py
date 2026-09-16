from django.db import models
from Admin.models import *
# Create your models here.

class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_contact=models.CharField(max_length=20)
    user_address=models.CharField(max_length=100)
    user_photo=models.FileField(upload_to="Assets/User/Photo")
    user_proof=models.FileField(upload_to="Assets/User/Photo")
    user_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    user_status=models.IntegerField(default=0)



class tbl_company(models.Model):
    company_name=models.CharField(max_length=50)
    company_email=models.CharField(max_length=50)
    company_contact=models.CharField(max_length=20)
    company_address=models.CharField(max_length=100)
    company_logo=models.FileField(upload_to="Assets/User/Photo")
    company_proof=models.FileField(upload_to="Assets/User/Photo")
    company_status=models.IntegerField(default=0)
    company_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    brand=models.ForeignKey(tbl_brand, on_delete=models.CASCADE)

class tbl_experience(models.Model):
    experience_range = models.CharField(max_length=50)

class tbl_serviceprovider(models.Model):
    serviceprovider_name=models.CharField(max_length=50)
    serviceprovider_email=models.CharField(max_length=50)
    serviceprovider_contact=models.CharField(max_length=50)
    serviceprovider_address=models.CharField(max_length=100)
    serviceprovider_photo=models.FileField(upload_to="Assets/User/Photo")
    serviceprovider_proof=models.FileField(upload_to="Assets/User/Photo")
    serviceprovider_password=models.CharField(max_length=30)
    serviceprovider_status=models.IntegerField(default=0)
    place=models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    experience = models.ForeignKey(tbl_experience, on_delete=models.CASCADE, null=True, blank=True)



class tbl_shop(models.Model):
    shop_name=models.CharField(max_length=50)
    shop_email=models.CharField(max_length=100)
    shop_contact=models.CharField(max_length=25)
    shop_address=models.CharField(max_length=200)
    shop_photo=models.FileField(upload_to="Assets/User/Photo")
    shop_proof=models.FileField(upload_to="Assets/User/Photo")
    shop_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    shop_status=models.IntegerField(default=0)



    





