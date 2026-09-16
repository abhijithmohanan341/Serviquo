from django.db import models
from Admin.models import *
from Guest.models import *


# Create your models here.

class tbl_technician(models.Model):
    technician_name=models.CharField(max_length=50)
    technician_email=models.CharField(max_length=50)
    technician_contact=models.CharField(max_length=20)
    technician_address=models.CharField(max_length=100)
    technician_photo=models.FileField(upload_to="Assets/User/Photo")
    technician_proof=models.FileField(upload_to="Assets/User/Photo")
    technician_status=models.IntegerField(default=0)
    technician_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    company=models.ForeignKey(tbl_company, on_delete=models.CASCADE)